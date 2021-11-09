from .road import Road
import math

class Light:

    light_status = {"North-South" : 0, "East-West":1}

    def __init__(self, incomingRoads, outgoingRoads):
        self.status = self.light_status["North-South"]
        self.incomingRoads = incomingRoads
        self.outgoingRoads = outgoingRoads
        self.red = True
        self.time = 0


    def updateCars(self):
        self.time += 1
        if self.red and self.time < 5:
            return

        if self.time >= 30:
            self.time = 0
            self.status = math.abs(self.status - 1)
        
        if self.status == self.light_status["North-South"]:

            carS = self.incomingRoads["S"].moveCarsFrom()
            carN = self.incomingRoads["N"].moveCarsFrom()
            if carS != None:
                self.outgoingRoads[carS.getNext()].moveCarsTo(carS)
            if carN != None:
                self.outgoingRoads[carN.getNext()].moveCarsTo(carN)

        elif self.status == light_status["East-West"]:
            
            carW = self.incomingRoads["W"].moveCarsFrom()
            carE = self.incomingRoads["E"].moveCarsFrom()
            if carW != None:
                self.outgoingRoads[carW.getNext()].moveCarsTo(carW)
            if carE != None:
                self.outgoingRoads[carE.getNext()].moveCarsTo(carE)


