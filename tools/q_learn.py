from .state import State
import numpy as np
import matplotlib.pyplot as plt
import math

class Q_Agent:
    # Initializes the Q-table with zero values. If there is quantization,
    # num_bins is the number of quantization bins
    # If there is no quantization, num_bins is the road capacity across each intersection
    def __init__(self, num_lights, num_bins, num_agents=1, global_state=True):
        # If num_agents > 1, decentralized case. Assume agents uniformly distributed around state space
        # If global_state is False, then use local states for Q agents
        # Dims are (2^num_lights) X (num_bins ^ num_counters)
        n_actions = 2 ** (num_lights // num_agents)

        self.num_lights = num_lights
        self.global_state = global_state
        self.num_agents = num_agents

        # Here, I'm not including the lights as part of the observable space
        # If later we assume there is some time cost to changing lights,
        # it would be important for the controller to know the current lights

        # Since there are 2 counters for each light (NS and EW), the obs space size is
        # exponential in 2 * num_lights
        if global_state:
            n_obs = num_bins ** (2 * num_lights)
        # If local state, shrink Q table accordingly
        else:
            n_obs = num_bins ** (2 * num_lights // num_agents)

        # Initialize Q-table with high cost
        self.table = np.full((num_agents,n_obs,n_actions), 100, dtype=np.float32)

        # Need this to calculate the state index later
        self.num_bins = num_bins

        # HYPERPARAMETERS
        # Number of episodes
        self.n_episodes = 10
        # Max iterations / episode
        self.max_iter = 10000
        # Chance of choosing a random action
        self.p_explore = 0.25
        # Discount factor
        self.gamma = 0.99
        # Inertia, used in dynamic learning
        self.inertia = 0.1
        # Learning rate (this is on a per state-action pair basis)
        # Create array of each time state (x,u) is visited
        self.lr = np.full((num_agents,n_obs,n_actions), 1, dtype=np.uint32)

    # Update table and learning rate
    def updateTable(self, agent, curr_state, action, cost, next_state):
        # Learning rate is inversely dependent on 
        # number of times this state-action pair has been seen
        rate = 1 / self.lr[agent,curr_state,action]
        new_q = (1-rate) * self.table[agent,curr_state,action] + rate*(cost + 
                                            self.gamma*min(self.table[agent,next_state,:]))
        self.lr[agent,curr_state,action] += 1
        self.table[agent,curr_state,action] = new_q
    
    # Gets an action, either random or learned
    def getAction(self, agent, curr_state):
        # With prob p_explore, pick a random action
        if np.random.uniform(0,1) < self.p_explore:
            idx = np.random.randint(0, self.table.shape[2])
        # Else, pick learned action
        else:
            idx = np.argmin(self.table[agent,curr_state,:])

        # idx is a number whose binary rep. corresponds to light states
        action = format(idx, '0' + str(self.num_lights //  self.num_agents) + 'b')
        action = [int(i) for i in action]
        return idx, action

    # Gets an action, either random or from a fixed policy
    def getActionFromPolicy(self, agent, curr_state, policy):
        # With prob p_explore, pick a random action
        if np.random.uniform(0,1) < self.p_explore:
            idx = np.random.randint(0, self.table.shape[2])
        # Else, pick action from policy
        else:
            idx = policy[agent,curr_state]

        # idx is a number whose binary rep. corresponds to light states
        action = format(idx, '0' + str(self.num_lights //  self.num_agents) + 'b')
        action = [int(i) for i in action]
        return idx, action

    # Converts the state returned by the simulation into an index for the q-table
    # State returned by sim is in the form: [[#NS, #EW], [#NS, #EW], ... , [#NS, #EW]]
    def stateToIdx(self, state):
        # Treat #EW of last light as least significant digit, 
        # #NS of first light as most-significant
        idx = 0
        # Significance of current digit
        sig = 1
        for light in reversed(state):
            idx += light[1] * sig
            # num_bins possible values for #NS and #EW
            sig = sig*self.num_bins
            idx += light[0] * sig
            sig = sig*self.num_bins
        return idx

    # Quantizes state into bins
    def quantizeState(self, state):
        #Take bins exponentially increasing
        bins = [2**i for i in range(self.num_bins - 1)]
        bins.insert(0, 0)
        quantized_state = []
        for s in state:
            quantized_light = []
            for road in s[0:2]:
                for b in reversed(bins):
                    if road >= b:
                        quantized_light.append(bins.index(b))
                        break
            quantized_state.append(quantized_light)

        return quantized_state

    # Trains table on simulation
    def trainTable(self):
        # Keep track of progress
        cost_per_episode = []
        # Initialize simulation
        state = State(self.num_lights)
        # List of states for each Q agent
        agent_states = []

        # Length of square
        agent_length = int(math.sqrt(self.num_lights // self.num_agents))
        # Assign lights to different agents
        nrows = agent_length
        ncols = agent_length
        agent_lights = (np.arange(0, self.num_lights)
                    .reshape(int(math.sqrt(self.num_lights)) // nrows, nrows, -1, ncols)
                    .swapaxes(1, 2)
                    .reshape(-1, nrows, ncols))
        print(agent_lights)

        for agent in range(self.num_agents):
            # Check if global state
            if self.global_state:
                curr_state = state.getState()
            else:
                # Local state, only assign curr_state to subset of whole state
                curr_state = [ state.getSpecificState(index) for index in agent_lights[agent].flatten() ]

            curr_state = self.quantizeState(curr_state)
            curr_state = self.stateToIdx(curr_state)
            agent_states.append(curr_state)

        # Split into episodes to get idea of progress
        for e in range(self.n_episodes):
            print(e)
            # Cost for this episode
            episode_cost = 0

            # Iterate through simulation
            for i in range(self.max_iter):
                # Start by getting actions for each agent
                agent_actions = []
                for agent in range(self.num_agents):
                    # Get action for this agent
                    action_idx, action = self.getAction(agent, agent_states[agent])
                    agent_actions.append(action_idx)
                    # Updates lights according to this agent's action
                    state.updateControl(action, agent_lights[agent].flatten())

                # Update simulation (2 steps) according to new lights
                state.updateState(2)

                # Compute cost of action
                cost_state = state.getState()
                cost = 0
                for s in cost_state:
                    cost += (s[0] + s[1])
                episode_cost += cost

                # Get next state for all agents
                for agent in range(self.num_agents):
                    if self.global_state:
                        next_state = state.getState()
                    else:
                        # Local state, only assign next_state to subset of whole state
                        next_state = [ state.getSpecificState(index) for index in agent_lights[agent].flatten() ]
                        
                    next_state = self.quantizeState(next_state)
                    next_state = self.stateToIdx(next_state)

                    # Update Q-table using quantized state and cost
                    self.updateTable(agent, agent_states[agent], agent_actions[agent], cost, next_state)
                    # Update state
                    agent_states[agent] = next_state
            
            # For reporting results
            cost_per_episode.append(episode_cost)
            print(episode_cost / self.max_iter)

        # Granularity of reporting
        x = []
        y = []
        g = 1
        for i in range(int(self.n_episodes / g)):
            print((i+1)*g," : mean cars in system: ",\
                np.mean(cost_per_episode[g*i:g*(i+1)]) / self.max_iter)
            x.append((i+1)*g*self.max_iter)
            y.append(np.mean(cost_per_episode[g*i:g*(i+1)]) / self.max_iter)
        
        fig, ax = plt.subplots()
        plt.ylabel('Mean cars in system')
        plt.xlabel('Number of iterations')
        plt.title('Q-Agent Development')
        ax.plot(x, y)
        plt.show()
        plt.savefig('q_agent.png')

        # Save optimal policy to .npy file
        policy = np.argmin(self.table, axis=2)
        print(policy)
        np.save("policy.npy", policy)


    # This method uses the algorithm described in https://mast.queensu.ca/~yuksel/AYTACLearning2017.pdf
    # The key difference in this algo, which allows it to converge to optimality with stochastic dynamic games,
    # is that rather than immediately update the policy with the best Q-table action, the policies remain constant
    # while the Q-table learns. Only after this "exploration phase" is done does the policy update.
    def trainTableDynamic(self):
        # Start with arbitrary policy for each agent
        policy = np.random.randint(self.table.shape[2], size=(self.table.shape[0], self.table.shape[1]))

        # Keep track of progress
        cost_per_episode = []
        episode_iterations = []
        # Initialize simulation
        state = State(self.num_lights)
        # List of states for each Q agent
        agent_states = []

        # Length of square
        agent_length = int(math.sqrt(self.num_lights // self.num_agents))
        # Assign lights to different agents
        nrows = agent_length
        ncols = agent_length
        agent_lights = (np.arange(0, self.num_lights)
                    .reshape(int(math.sqrt(self.num_lights)) // nrows, nrows, -1, ncols)
                    .swapaxes(1, 2)
                    .reshape(-1, nrows, ncols))
        print(agent_lights)

        for agent in range(self.num_agents):
            # Check if global state
            if self.global_state:
                curr_state = state.getState()
            else:
                # Local state, only assign curr_state to subset of whole state
                curr_state = [ state.getSpecificState(index) for index in agent_lights[agent].flatten() ]

            curr_state = self.quantizeState(curr_state)
            curr_state = self.stateToIdx(curr_state)
            agent_states.append(curr_state)

        # Now each "episode" is an exploration phase
        for e in range(self.n_episodes):
            print(e)
            # Cost for this episode
            episode_cost = 0
            # Iterate through simulation, running longer as it gets closer to convergence
            iterations = max(self.max_iter * e // self.n_episodes, 10000)
            episode_iterations.append(iterations)
            for i in range(iterations):
                # Start by getting actions for each agent
                agent_actions = []
                for agent in range(self.num_agents):
                    # Get action for this agent
                    # NOTE: This action is received from the current "best" policy, not from the Q-table
                    action_idx, action = self.getActionFromPolicy(agent, agent_states[agent], policy)
                    agent_actions.append(action_idx)
                    # Updates lights according to this agent's action
                    state.updateControl(action, agent_lights[agent].flatten())

                # Update simulation (2 steps) according to new lights
                state.updateState(2)
                
                # Compute cost of action
                cost_state = state.getState()
                cost = 0
                for s in cost_state:
                    cost += (s[0] + s[1])
                episode_cost += cost

                # Get next state for all agents
                for agent in range(self.num_agents):
                    if self.global_state:
                        next_state = state.getState()
                    else:
                        # Local state, only assign next_state to subset of whole state
                        next_state = [ state.getSpecificState(index) for index in agent_lights[agent].flatten() ]

                    next_state = self.quantizeState(next_state)
                    next_state = self.stateToIdx(next_state)

                    # Update Q-table using quantized state and cost
                    self.updateTable(agent, agent_states[agent], agent_actions[agent], cost, next_state)
                    # Update state
                    agent_states[agent] = next_state

            # For reporting results
            cost_per_episode.append(episode_cost)
            print(episode_cost / iterations)

            # NOTE: now need to check if current policy is not too much worse than the policy we'd get by taking 
            # the argmin of the Q-table. If it's acceptably close, keep it. Otherwise, keep it or switch to
            # to an acceptably close policy with probability given by the inertia
            thresh = 0.5
            almost_best = np.min(self.table, axis=2) + thresh
            print(self.table)
            print(policy)
            for agent in range(self.num_agents):
                # Check if current policy is good enough
                test = [self.table[agent, x, policy[agent, x]] > almost_best[agent, x] for x in range(self.table.shape[1])]
                if np.any(test):
                    print("not good enough")
                    # At least one state thats not good enough
                    if np.random.uniform(0,1) > self.inertia:
                        # Switch to new acceptable policy
                        for x in range(self.table.shape[1]):
                            indices = np.asarray(self.table[agent, x, :] < almost_best[agent, x]).nonzero()
                            choice = np.random.choice(indices[0])
                            policy[agent, x] = choice
                # Else, do nothing (keep same policy)
            print(policy)
                
            # Reset LR after each episode
            self.lr[:,:,:] = 1
            

        # Reporting
        x = []
        y = []
        for i in range(int(self.n_episodes)):
            print((i+1)," : mean cars in system: ",\
                cost_per_episode[i] / episode_iterations[i])
            x.append((i+1)*episode_iterations[i])
            y.append(np.mean(cost_per_episode[i]) / episode_iterations[i])
        
        fig, ax = plt.subplots()
        plt.ylabel('Mean cars in system')
        plt.xlabel('Number of iterations')
        plt.title('Q-Agent Development')
        ax.plot(x, y)
        plt.show()
        plt.savefig('q_agent.png')
        return policy