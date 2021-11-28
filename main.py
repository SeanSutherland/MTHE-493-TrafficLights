from tools.road import Road
from tools.light import Light
from tools.car import Car
from tools.sink import Sink
from tools.state import State
import time
import random as r

state = State()

def controlState(state):
    action = []
    for light in state:
        if light[2] == 0:
            if light[0] < light[1]-2:
                action.append(1)
            else:
                action.append(0)
        else:   
            if light[1] < light[0]-2:
                action.append(0)
            else:
                action.append(1)
    return action


while True:
    time.sleep(1)
    state.updateState(controlState(state.getState()))

    # the state is a list of traffic lights for which each light has state [# of cars NS, # of cars EW, 0 if NS | 1 if EW]
    print(state.getState())
    print(state.mySink)
