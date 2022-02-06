from .state import State
import numpy as np
import matplotlib.pyplot as plt

class Q_Agent:
    # Initializes the Q-table with zero values. If there is quantization,
    # num_bins is the number of quantization bins
    # If there is no quantization, num_bins is the road capacity across each intersection
    def __init__(self, num_lights, num_bins):
        # Dims are (2^num_lights) X (num_bins ^ num_counters)
        n_actions = 2 ** num_lights

        self.num_lights = num_lights

        # Here, I'm not including the lights as part of the observable space
        # If later we assume there is some time cost to changing lights,
        # it would be important for the controller to know the current lights

        # Since there are 2 counters for each light (NS and EW), the obs space size is
        # exponential in 2 * num_lights
        n_obs = num_bins ** (2 * num_lights)
        # Initialize Q-table with high cost
        self.table = np.full((n_obs, n_actions),100, dtype=np.uint8)

        # Need this to calculate the state index later
        self.num_bins = num_bins

        # HYPERPARAMETERS
        # Number of episodes
        self.n_episodes = 4000
        # Max iterations / episode
        self.max_iter = 2000
        # Chance of choosing a random action
        self.p_explore = 0.5
        # Discount factor
        self.gamma = 0.99
        # Learning rate (this is on a per state-action pair basis)
        # Create array of each time state (x,u) is visited
        self.lr = np.full((n_obs, n_actions),1, dtype=np.uint32)

    # Update table and learning rate
    def updateTable(self, curr_state, action, cost, next_state):
        # Learning rate is inversely dependent on 
        # number of times this state-action pair has been seen
        rate = 1 / self.lr[curr_state, action]
        new_q = (1-rate) * self.table[curr_state, action] + rate*(cost + 
                                            self.gamma*min(self.table[next_state,:]))
        self.lr[curr_state, action] += 1
        self.table[curr_state, action] = new_q
    
    # Gets an action, either random or learned
    def getAction(self, curr_state):
        # With prob p_explore, pick a random action
        if np.random.uniform(0,1) < self.p_explore:
            idx = np.random.randint(0, self.table.shape[1])
        # Else, pick learned action
        else:
            idx = np.argmin(self.table[curr_state,:])

        # idx is a number whose binary rep. corresponds to light states
        action = format(idx, '04b')
        action = [int(i) for i in action]
        return idx, action

    # Converts the state returned by the simulation into an index for the q-table
    # State returned by sim is in the form: [[#NS, #EW], [#NS, #EW], ... , [#NS, #EW]]
    def stateToIdx(self, state):
        # Treat #EW of last light as leaset significant digit, 
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
        #TODO bake this into the road class
        bins = [0, 2, 4, 8]
        quantized_state = []
        #TODO make this more generic
        for s in state:
            quantized_light = []
            for road in s[0:2]:
                bin = len(bins)
                for b in reversed(bins):
                    if road >= b:
                        quantized_light.append(bin - 1)
                        break
                    bin -= 1
            quantized_state.append([*quantized_light, s[2]])

        return quantized_state

    # Trains table on simulation
    def trainTable(self):
        # Keep track of progress
        cost_per_episode = []
        # Initialize simulation
        state = State(self.num_lights)
        curr_state = state.getState()
        curr_state = self.quantizeState(curr_state)
        curr_state = self.stateToIdx(curr_state)
        # Split into episodes to get idea of progress
        for e in range(self.n_episodes):
            print(e)
            # Cost for this episode
            episode_cost = 0

            # Iterate through simulation
            for i in range(self.max_iter):
                # Get action for this iteration
                action_idx, action = self.getAction(curr_state)

                # Update simulation and get next state
                state.updateState(action)
                next_state = state.getState()

                cost = 0
                for s in next_state:
                    cost += (s[0] + s[1])
                episode_cost += cost

                # Update Q-table using quantized state and cost
                next_state = self.quantizeState(next_state)
                next_state = self.stateToIdx(next_state)
                self.updateTable(curr_state, action_idx, cost, next_state)

                # Update state
                curr_state = next_state
            
            # At the end of each episode, update p_explore
            cost_per_episode.append(episode_cost)

        print(np.min(self.table, axis=0))
        # Granularity of reporting
        x = []
        y = []
        g = 100
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
        policy = np.argmin(self.table, axis=1)
        print(policy)
        np.save("policy.npy", policy)