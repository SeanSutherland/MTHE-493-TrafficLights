from tools.state import State
from tools.q_learn import Q_Agent
#from tools.g import GUI
import time
import math
import numpy as np

SKIP_FIRST_ITERATIONS = 1000
DIMS = 4

# Basic logic controller


def controlState(state):
    action = []
    for light in state:
        if light[2] == 0:
            if light[0] < light[1]-3:
                action.append(1)
            else:
                action.append(0)
        else:
            if light[1] < light[0]-3:
                action.append(0)
            else:
                action.append(1)
    return action

q_agent = Q_Agent(4, 4, 4, False)
policy = np.load('decentralized_policy.npy')

state = State(DIMS)
# Length of square
agent_length = int(math.sqrt(q_agent.num_lights // q_agent.num_agents))
# Assign lights to different agents
nrows = agent_length
ncols = agent_length
agent_lights = (np.arange(0, q_agent.num_lights)
            .reshape(int(math.sqrt(q_agent.num_lights)) // nrows, nrows, -1, ncols)
            .swapaxes(1, 2)
            .reshape(-1, nrows, ncols))

# List of states for each Q agent
agent_states = []
for agent in range(q_agent.num_agents):
    # Check if global state
    if q_agent.global_state:
        curr_state = state.getState()
    else:
        # Local state, only assign curr_state to subset of whole state
        curr_state = [ state.getSpecificState(index) for index in agent_lights[agent].flatten() ]

    curr_state = q_agent.quantizeState(curr_state)
    curr_state = q_agent.stateToIdx(curr_state)
    agent_states.append(curr_state)

d = 0
# Run simulation
while True:
    if d >= SKIP_FIRST_ITERATIONS:
        time.sleep(1)
    else:
        d += 1

    # Update state based on control choice from previous state
    q_agent.updateControlandState(state, agent_states, agent_lights, policy)
    s = state.getState()
    for i in range(int(math.sqrt(DIMS)-1), -1, -1):
        for j in range(int(math.sqrt(DIMS)-1), -1, -1):
            print(s[int(i*math.sqrt(DIMS) + j)], end="  ")
        print(" ")
    print("\n\n")

'''
q_agent = Q_Agent(4, 4, 4, False)
#q_agent.trainTable()
policy = q_agent.trainTableDynamic()
'''