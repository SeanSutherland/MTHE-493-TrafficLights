import numpy as np

class Q_Agent:
    # Initializes the Q-table with zero values. If there is quantization,
    # num_bins is the number of quantization bins
    # If there is no quantization, num_bins is the road capacity
    def __init__(self, num_lights, num_roads, num_bins):
        # Dims are (2^num_lights) X (num_bins ^ num_roads)
        n_actions = 2 ** num_lights

        # Here, I'm not including the lights as part of the observable space
        # If later we assume there is some time cost to changing lights,
        # it would be important for the controller to know the current lights
        n_obs = num_bins ** num_roads
        # Initialize Q-table
        self.table = np.zeros((n_obs, n_actions))

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

    def updateTable(self, curr_state, action, reward, next_state):
        self.table[curr_state, action] = (1-self.lr) * self.table[curr_state, action] + self.lr*(reward + 
                                            self.gamma*max(self.table[next_state,:]))
    
    # Gets an action, either random or learned
    def getAction(self, curr_state):
        # With prob p_explore, pick a random action
        if np.random.uniform(0,1) < self.p_explore:
            idx = np.random.uniform(0, self.table.shape[1])
        # Else, pick learned action
        else:
            idx = np.argmax(self.table[curr_state,:])

        # idx is a number whose binary rep. corresponds to light states
        idx = bin(idx)
        action = [int(i) for i in str(idx)]
        return action

    # Trains table on simulation. The sim param needs to provide reset() 
    # and update() methods
    def trainTable(self, sim):
        # Keep track of progress
        rewards_per_episode = []

        for e in range(self.n_episodes):
            # Initialize episode
            # TODO Need way to reset simulation
            # TODO Figure out how to convert state to an index
            curr_state = sim.reset()
            
            # Rewards for this episode
            episode_reward = 0

            # Iterate through simulation
            for i in range(self.max_iter):
                # Get action for this iteration
                action = self.getAction(curr_state)

                # Update simulation
                # TODO Need an update() method for the simulation
                # Think it would just be changing the light states to those
                # in action and calling updateCars(), and returning new car numbers
                next_state, reward = sim.update(action)
                episode_reward += reward
                curr_state = next_state
            
            # At the end of each episode, update p_explore
            self.p_explore = max(self.min_p_explore, self.p_explore*np.exp(-self.decay_explore))
            rewards_per_episode.append(episode_reward)