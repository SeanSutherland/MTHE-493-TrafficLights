
import numpy as np
class Controller:
    def __init__(self,num_lights,num_bins):
        self.num_lights = num_lights
        self.table=np.load('2x2.npy')
        self.num_bins = num_bins
    
    def getAction(self, curr_state):      
        curr_state = self.quantizeState(curr_state)
        curr_state = self.stateToIdx(curr_state)
        idx = np.argmin(self.table[curr_state,:])
        
        # idx is a number whose binary rep. corresponds to light states
        action = format(idx, '04b')
        action = [int(i) for i in action]
        return action

    def stateToIdx(self, state):
        # Treat direction of last light as least significant digit, 
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
        max_cars = 9
        bin_sizes = [1, 2, 3, 4]
        bins = [0, 3, 6, 10]
        quantized_state = []
        #TODO make this more generic
        for s in state:
            quantized_light = []
            for road in s[0:2]:
                bin = len(bins)
                for b in reversed(bins):
                    #TODO Remove this once there is a simulation limit on number of cars
                    # For now just put into biggest bin
                    if road > max_cars:
                        quantized_light.append(len(bins) - 1)
                        break
                    #TODO Prettify this
                    if road == 0:
                        quantized_light.append(0)
                        break
                    if road >= b:
                        quantized_light.append(bin)
                        break
                    bin -= 1
            quantized_state.append([*quantized_light, s[2]])

        return quantized_state
    
    