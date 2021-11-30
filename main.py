from tools.state import State
from tools.g import GUI
import time

state = State()

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


g = GUI()
d = 0
while True:
    if d > 100:
        time.sleep(1)
    else:
        d+=1
    
    state.updateState(controlState(state.getState()))
    g.update(state.getRoadStates(), state.getLightStates(), state.mySink.getStuff())
