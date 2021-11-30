import numpy as np
from tools.state import State

class Q_Agent:
    # Initializes the Q-table with zero values. If there is quantization,
    # num_bins is the number of quantization bins
    # If there is no quantization, num_bins is the road capacity across each intersection
    def __init__(self, num_lights, num_bins):
        # Dims are (2^num_lights) X (num_bins ^ num_counters)
        n_actions = 2 ** num_lights

        # Here, I'm not including the lights as part of the observable space
        # If later we assume there is some time cost to changing lights,
        # it would be important for the controller to know the current lights

        # Since there are 2 counters for each light (NS and EW), the obs space size is
        # exponential in 2 * num_lights
        n_obs = num_bins ** (2 * num_lights)
        # Initialize Q-table
        self.table = np.zeros((n_obs, n_actions))

        # Need this to calculate the state index later
        self.num_bins = num_bins

        # HYPERPARAMETERS
        # Number of episodes
        self.n_episodes = 10000
        # Max iterations / episode
        self.max_iter = 1000
        # Always start by exploring (prob is 1)
        self.p_explore = 1
        # Rate at which exploration rate decays
        self.decay_explore = 0.001
        # Min explore prob
        self.min_p_explore = 0.01
        # Discount factor
        self.gamma = 0.99
        # Learning rate
        self.lr = 0.1

    def updateTable(self, curr_state, action, cost, next_state):
        self.table[curr_state, action] = (1-self.lr) * self.table[curr_state, action] + self.lr*(cost + 
                                            self.gamma*min(self.table[next_state,:]))
    
    # Gets an action, either random or learned
    def getAction(self, curr_state):
        # With prob p_explore, pick a random action
        if np.random.uniform(0,1) < self.p_explore:
            idx = np.random.uniform(0, self.table.shape[1])
        # Else, pick learned action
        else:
            idx = np.argmin(self.table[curr_state,:])

        # idx is a number whose binary rep. corresponds to light states
        idx = bin(idx)
        action = [int(i) for i in str(idx)]
        return action

    # Converts the state returned by the simulation into an index for the q-table
    # State returned by sim is in the form: [[#NS, #EW, D_0], [#NS, #EW, D_1], ... , [#NS, #EW, D_n]]
    def stateToIdx(self, state):
        # Treat direction of last light as least significant digit, 
        # #NS of first light as most-significant
        idx = 0
        # Significance of current digit
        sig = 1
        for light in state:
            idx += light[2] * sig
            # 2 possible values for direction, so significance of 2
            sig *= 2
            idx += light[1] * sig
            # num_bins possible values for #NS and #EW
            sig *= self.num_bins
            idx += light[0] * sig
            sig *= self.num_bins
        return idx

    # Trains table on simulation
    def trainTable(self):
        # Keep track of progress
        cost_per_episode = []

        for e in range(self.n_episodes):
            # Initialize episode
            state = State()
            curr_state = self.stateToIdx(state.getState())
            
            # Cost for this episode
            episode_cost = 0

            # Iterate through simulation
            for i in range(self.max_iter):
                # Get action for this iteration
                action = self.getAction(curr_state)

                # Update simulation
                state.updateState(action)
                curr_state = state.getState()
                cost = 0
                for s in curr_state:
                    cost += (s[0] + s[1])
                episode_cost += cost
            
            # At the end of each episode, update p_explore
            self.p_explore = max(self.min_p_explore, self.p_explore*np.exp(-self.decay_explore))
            cost_per_episode.append(episode_cost)