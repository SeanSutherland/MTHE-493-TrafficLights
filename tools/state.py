from .road import Road
from .light import Light
from .car import Car
from .sink import Sink
import time
import random as r
from numpy import random as p
import math


def generateRoads(d):
    roads = {}
    for i in range(d):
        lights = {"N": Road(),
            "S": Road(),
            "E": Road(),
            "W": Road(),
        }
        roads[i] = lights
    return roads

def generateLights(roads, mySink,d):
    traffic_lights = []
    sq = int(math.sqrt(d))
    for i in range(sq):
        incoming = [roads[i]["N"],roads[i]["S"],roads[i]["E"],roads[i]["W"]]
        if i == 0:
            outgoing = [roads[sq]["N"],mySink,roads[i+1]["E"],mySink]
        elif i == sq-1:
            outgoing = [roads[i+sq]["N"], mySink ,mySink, roads[i-1]["W"]]
        else:
            outgoing = [roads[i+sq]["N"], mySink ,roads[i+1]["E"], roads[i-1]["W"]]
        traffic_lights.append(Light(incoming, outgoing))

    for i in range(sq,d-sq):
        incoming = [roads[i]["N"],roads[i]["S"],roads[i]["E"],roads[i]["W"]]
        if i % sq == 0: 
            outgoing = [roads[i+sq]["N"], roads[i-sq]["S"] ,roads[i+1]["E"], mySink]
        elif i + 1 % sq == 0:
            outgoing = [roads[i+sq]["N"], roads[i-sq]["S"] ,mySink, roads[i-1]["W"]]
        else:
            outgoing = [roads[i+sq]["N"], roads[i-sq]["S"] ,roads[i+1]["E"], roads[i-1]["W"]]
        traffic_lights.append(Light(incoming, outgoing))

    for i in range(d-sq, d):
        incoming = [roads[i]["N"],roads[i]["S"],roads[i]["E"],roads[i]["W"]]
        if i == d-sq:
            outgoing = [mySink,roads[i-sq]["E"],roads[i+1]["E"],mySink]
        elif i == d-1:
            outgoing = [mySink,roads[i-sq]["E"],mySink,roads[i-1]["W"]]
        else:
            outgoing = [mySink, roads[i-sq]["E"] ,roads[i+1]["E"], roads[i-1]["W"]]
        traffic_lights.append(Light(incoming, outgoing))

    return traffic_lights


class State:
    def __init__(self,d):
        self.mySink = Sink()
        self.dimension = d
        self.sq = int(math.sqrt(d))
        self.roads = generateRoads(d)
        self.traffic_lights = generateLights(self.roads, self.mySink,d)
        self.newCars()
        self.lastCarsAdded = [[0,0],[0,0],[0,0],[0,0]]


    def newCars(self):
        self.lastCarsAdded = [[0,0],[0,0],[0,0],[0,0]]
        # State arrivals Poisson(1) distributed
        lam = 0.3
        numberOfCarsAdded = p.poisson(lam,1)[0]

        
        for i in range(self.dimension):
            numberOfCarsAdded = p.poisson(lam,1)[0]
            count = 0
            while count < numberOfCarsAdded:
                direction = "0"
                if i < self.sq:
                    if i == 0:
                        direction = r.choice(["E","N"])
                    elif i == self.sq-1:
                        direction = r.choice(["W","N"])
                    else:
                        direction = "N"
                elif i >= self.dimension - self.sq:
                    if i == self.dimension - self.sq:
                        direction = r.choice(["E","S"])
                    elif i == self.dimension-1:
                        direction = r.choice(["W","S"])
                    else:
                        direction = "S"
                elif i % self.sq == 0:
                    direction = "E"
                elif i +1% self.sq == 0:
                    direction = "W"

                if direction != "0":
                    self.roads[i][direction].moveCarsTo(Car(i, direction,self.dimension))
                    count += 1
                else: 
                    break

    
    # Get current state of the traffic lights for Q - learning
    def getState(self):
        state = []
        for light in self.traffic_lights:
            state.append(light.getTotals())
        return state

    # Update the state based on Q - learning control
    def updateState(self, control):
        i = 0
        for light in control:
            self.traffic_lights[i].changeLight(light)
            i += 1

        # Add new cars at each timestep
        self.newCars()

        # Update cars at each light
        for light in self.traffic_lights:
            light.updateCars()

    def __str__(self):        
        for light in self.traffic_lights:
            print(light)
    
    def getLastCars(self):
        i = 0
        for light in self.traffic_lights:
            t = light.getCarsLeaving()
            self.lastCarsAdded[i][0] += t[0]
            self.lastCarsAdded[i][1] += t[1]
            i += 1
        return str(self.lastCarsAdded)
    
    def getRoadStates(self):

        newList = {
        0: {
            "N": 0,
            "S": 0,
            "E": 0,
            "W": 0,
        },
        1:{
            "N": 0,
            "S": 0,
            "E": 0,
            "W": 0,
        },
        2:{
            "N": 0,
            "S": 0,
            "E": 0,
            "W": 0,
        },
        3:{
            "N": 0,
            "S": 0,
            "E": 0,
            "W": 0,
        }
    }
        for intersection in self.roads.keys():
            for road in self.roads[intersection].keys():
                newList[intersection][road] = self.roads[intersection][road].getNumberOfCars()
        return newList
    
    def getLightStates(self):
        newList = []
        for intersection in self.traffic_lights:
            if intersection.time < 3:
                newList.append(2)
            else:
                newList.append(intersection.status)
        return newList

