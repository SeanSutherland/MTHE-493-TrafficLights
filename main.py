from tools.state import State
from tools.g import GUI
import time

SIMULATION = True
SKIP_FIRST_HUNDRED_ITERATIONS = True

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

if SIMULATION:
    g = GUI()

state = State()

d = 0
# Run simulation
while True:
    if SKIP_FIRST_HUNDRED_ITERATIONS:
        if d > 100:
            time.sleep(1)
        else:
            d+=1
    else: 
        time.sleep(1)
    
    # Update state based on control choice from previous state
    state.updateState(controlState(state.getState()))

    # Update visualization with new state
    g.update(state.getRoadStates(), state.getLightStates(), state.mySink.getStuff())
