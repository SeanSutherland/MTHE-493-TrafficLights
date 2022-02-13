from tools.state import State
from tools.g import GUI
import time
import math

SKIP_FIRST_ITERATIONS = 1000
DIMS = 16

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


state = State(DIMS)

d = 0
# Run simulation
while True:
    if d >= SKIP_FIRST_ITERATIONS:
        time.sleep(1)
    else:
        d += 1

    # Update state based on control choice from previous state
    control = controlState(state.getState())
    state.updateState(control)
    s = state.getState()
    for i in range(int(math.sqrt(DIMS)-1), -1, -1):
        for j in range(int(math.sqrt(DIMS)-1), -1, -1):
            print(s[int(i*math.sqrt(DIMS) + j)], end="  ")
        print(" ")
    print("\n\n")

    # print(state.mySink)
