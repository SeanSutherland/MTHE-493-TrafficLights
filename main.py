from tools.state import State
from tools.q_learn import Q_Agent
from tools.g import GUI
from tools.state_control import Controller
import time
import math


SKIP_FIRST_ITERATIONS = 0
DIMS = 4
SIMULATION = True
# q_agent = Q_Agent(4,4)
# q_agent.trainTable()

if SIMULATION:
    g = GUI()

state = State(DIMS)
controller = Controller(4,4)
d = 0
#Run simulation
while True:
    if d >= SKIP_FIRST_ITERATIONS:
        time.sleep(1)
    else:
        d+=1
    
    # Update state based on control choice from previous state
    action = controller.getAction(state.getState())
    state.updateState(action)

    # Update visualization with new state
    if SIMULATION:
        g.update(state.getRoadStates(), state.getLightStates(), state.mySink.getStuff(),state.getState(),action, state.getLastCars())

    print(state.mySink)