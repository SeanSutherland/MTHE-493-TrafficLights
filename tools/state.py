from .road import Road
from .light import Light
from .car import Car
from .sink import Sink
import time
import random as r
from numpy import random as p
import math

CAPACITY = 250
LAMBDA_EW = 0.4
LAMBDA_NS = 0.1


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


def generateLights(roads, mySink, d):
    traffic_lights = []
    sq = int(math.sqrt(d))
    if d == 1:
        incoming = [roads[0]["N"], roads[0]["S"], roads[0]["E"], roads[0]["W"]]
        outgoing = [mySink, mySink, mySink, mySink]
        traffic_lights.append(Light(incoming, outgoing))
    else:
        for i in range(sq):
            incoming = [roads[i]["N"], roads[i]
                        ["S"], roads[i]["E"], roads[i]["W"]]
            if i == 0:
                outgoing = [roads[sq]["N"], mySink, roads[i+1]["E"], mySink]
            elif i == sq-1:
                outgoing = [roads[i+sq]["N"], mySink, mySink, roads[i-1]["W"]]
            else:
                outgoing = [roads[i+sq]["N"], mySink,
                            roads[i+1]["E"], roads[i-1]["W"]]
            traffic_lights.append(Light(incoming, outgoing))

        for i in range(sq, d-sq):
            incoming = [roads[i]["N"], roads[i]
                        ["S"], roads[i]["E"], roads[i]["W"]]
            if i % sq == 0:
                outgoing = [roads[i+sq]["N"], roads[i-sq]
                            ["S"], roads[i+1]["E"], mySink]
            elif i + 1 % sq == 0:
                outgoing = [roads[i+sq]["N"], roads[i-sq]
                            ["S"], mySink, roads[i-1]["W"]]
            else:
                outgoing = [roads[i+sq]["N"], roads[i-sq]
                            ["S"], roads[i+1]["E"], roads[i-1]["W"]]
            traffic_lights.append(Light(incoming, outgoing))

        for i in range(d-sq, d):
            incoming = [roads[i]["N"], roads[i]
                        ["S"], roads[i]["E"], roads[i]["W"]]
            if i == d-sq:
                outgoing = [mySink, roads[i-sq]["E"], roads[i+1]["E"], mySink]
            elif i == d-1:
                outgoing = [mySink, roads[i-sq]["E"], mySink, roads[i-1]["W"]]
            else:
                outgoing = [mySink, roads[i-sq]["E"],
                            roads[i+1]["E"], roads[i-1]["W"]]
            traffic_lights.append(Light(incoming, outgoing))

    return traffic_lights


def poisson(lam):
    return p.poisson(lam, 1)[0]


class State:
    def __init__(self, d):
        self.mySink = Sink()
        self.dimension = d
        self.sq = int(math.sqrt(d))
        self.roads = generateRoads(d)
        self.traffic_lights = generateLights(self.roads, self.mySink, d)
        self.newCars()
        self.lastCarsAdded = [[0, 0], [0, 0], [0, 0], [0, 0]]

    def newCars(self):
        self.lastCarsAdded = [[0, 0], [0, 0], [0, 0], [0, 0]]

        if self.getTotalCars() > CAPACITY:
            return

        for i in range(self.dimension):
            numberOfCarsAdded = [0, 0, 0, 0]
            if i == 0:
                numberOfCarsAdded[0] = poisson(LAMBDA_NS)
                numberOfCarsAdded[2] = poisson(LAMBDA_EW)
            elif i == self.sq-1:
                numberOfCarsAdded[0] = poisson(LAMBDA_NS)
                numberOfCarsAdded[3] = poisson(LAMBDA_EW)
            elif i == self.dimension - self.sq:
                numberOfCarsAdded[1] = poisson(LAMBDA_NS)
                numberOfCarsAdded[2] = poisson(LAMBDA_EW)
            elif i == self.dimension - 1:
                numberOfCarsAdded[1] = poisson(LAMBDA_NS)
                numberOfCarsAdded[3] = poisson(LAMBDA_EW)
            elif i < self.sq:
                numberOfCarsAdded[0] = poisson(LAMBDA_NS)
            elif i >= self.dimension - self.sq:
                numberOfCarsAdded[1] = poisson(LAMBDA_NS)
            elif i % self.sq == 0:
                numberOfCarsAdded[2] = poisson(LAMBDA_EW)
            elif i + 1 % self.sq == 0:
                numberOfCarsAdded[3] = poisson(LAMBDA_EW)
            else:
                continue

            direction = ["N", "S", "E", "W"]
            for j in range(4):
                while numberOfCarsAdded[j] > 0:
                    self.roads[i][direction[j]].moveCarsTo(
                        Car(i, direction[j], self.dimension))
                    numberOfCarsAdded[j] -= 1

    def getTotalCars(self):
        sum = 0
        for light in self.traffic_lights:
            sum += (light.getTotals()[0]+light.getTotals()[1])
        return sum
    # Get current state of the traffic lights for Q - learning

    def getState(self):
        state = []
        for light in self.traffic_lights:
            state.append(light.getTotals())
        return state

    def getSpecificState(self, index):
        return self.traffic_lights[index].getTotals()

    def updateControl(self, control, indices):
        for i in range(len(control)):
            self.traffic_lights[indices[i]].changeLight(control[i])

    def updateState(self, num_updates):
        for j in range(num_updates):
            # Add new cars at each timestep
            self.newCars()

            # Update cars at each light
            for light in self.traffic_lights:
                light.updateCars()

    def __str__(self):
        for light in self.traffic_lights:
            print(light)
