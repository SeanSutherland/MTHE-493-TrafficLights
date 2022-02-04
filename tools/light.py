from .road import Road
from .sink import Sink
import math

class Light:

    light_status = {"North-South" : 0, "East-West":1}

    def __init__(self, incomingRoads, outgoingRoads):
        self.status = self.light_status["North-South"]
        self.incomingRoads = incomingRoads
        self.outgoingRoads = outgoingRoads
        self.red = False
        self.time = 5
        self.carsLeaving = [0,0]
        self.sink = Sink()

    def getTotals(self):
        state = [0,0,0]
        state[0] = self.incomingRoads[0].getNumberOfCars() + self.incomingRoads[1].getNumberOfCars()
        state[1] = self.incomingRoads[2].getNumberOfCars() + self.incomingRoads[3].getNumberOfCars()
        state[2] = self.status
        return state


    def updateCars(self):
        self.time += 1

        for roads in self.incomingRoads:
            roads.timeStep()
        
        #if self.time < 3:
            #return

        if self.status == self.light_status["North-South"]:

            carS = self.incomingRoads[1].moveCarsFrom()
            carN = self.incomingRoads[0].moveCarsFrom()
            if carS != None:
                n = self.outgoingRoads[carS.getNext()]
                n.moveCarsTo(carS)
            if carN != None:
                n = self.outgoingRoads[carN.getNext()]
                n.moveCarsTo(carN)

        elif self.status == self.light_status["East-West"]:
            
            carW = self.incomingRoads[3].moveCarsFrom()
            carE = self.incomingRoads[2].moveCarsFrom()
            if carW != None:
                n = self.outgoingRoads[carW.getNext()]
                n.moveCarsTo(carW)
            if carE != None:
                n = self.outgoingRoads[carE.getNext()]
                n.moveCarsTo(carE)


    def changeLight(self, newState):
        if self.status != newState:
            self.time = 0
        self.status = newState
    
    def getCarsLeaving(self):
        return self.carsLeaving
        


