from .road import Road
import math

class Light:

    light_status = {"North-South" : 0, "East-West":1}

    def __init__(self, incomingRoads, outgoingRoads):
        self.status = self.light_status["North-South"]
        self.incomingRoads = incomingRoads
        self.outgoingRoads = outgoingRoads
        self.red = False
        self.time = 0


    def updateCars(self):
        self.time += 1
        if self.red and self.time < 5:
            return

        for roads in self.incomingRoads:
            roads.timeStep()

        if self.time >= 10:
            self.time = 0
            self.status = abs(self.status - 1)
        
        if self.status == self.light_status["North-South"]:

            carS = self.incomingRoads[1].moveCarsFrom()
            carN = self.incomingRoads[0].moveCarsFrom()
            if carS != None:
                self.outgoingRoads[carS.getNext()].moveCarsTo(carS)
            if carN != None:
                self.outgoingRoads[carN.getNext()].moveCarsTo(carN)

        elif self.status == self.light_status["East-West"]:
            
            carW = self.incomingRoads[3].moveCarsFrom()
            carE = self.incomingRoads[2].moveCarsFrom()
            if carW != None:
                self.outgoingRoads[carW.getNext()].moveCarsTo(carW)
            if carE != None:
                self.outgoingRoads[carE.getNext()].moveCarsTo(carE)

    def __str__(self):
        a = "   " + str(self.incomingRoads[1]) + "   \n"
        a += str(self.incomingRoads[2]) + "     " + str(self.incomingRoads[3]) + "\n"
        a += "   " + str(self.incomingRoads[0]) + "   \n"
        
        return a


