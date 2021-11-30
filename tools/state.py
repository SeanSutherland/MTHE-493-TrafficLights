from .road import Road
from .light import Light
from .car import Car
from .sink import Sink
import time
import random as r
from numpy import random as p


def generateRoads():
    roads = {
        0: {
            "N": Road(),
            "S": Road(),
            "E": Road(),
            "W": Road(),
        },
        1:{
            "N": Road(),
            "S": Road(),
            "E": Road(), 
            "W": Road(), 
        },
        2:{
            "N":Road(),
            "S":Road(),
            "E":Road(),
            "W":Road(),
        },
        3:{
            "N":Road(),
            "S":Road(),
            "E":Road(),
            "W":Road(),
        }
    }
    return roads

def generateLights(roads, mySink):

    traffic_lights = [Light(
        [roads[0]["N"],roads[0]["S"],roads[0]["E"],roads[0]["W"]],
        [roads[3]["N"], mySink ,roads[1]["E"], mySink]
    ), Light(
        [roads[1]["N"],roads[1]["S"],roads[1]["E"],roads[1]["W"]],
        [roads[2]["N"], mySink ,mySink, roads[0]["W"]]
    ), Light(
        [roads[2]["N"],roads[2]["S"],roads[2]["E"],roads[2]["W"]],
        [mySink, roads[1]["S"] ,mySink, roads[3]["W"]]
    ), Light(
        [roads[3]["N"],roads[3]["S"],roads[3]["E"],roads[3]["W"]],
        [mySink, roads[0]["S"] ,roads[2]["E"], mySink]
    )]
    return traffic_lights


class State:
    def __init__(self):
        self.mySink = Sink()
        self.roads = generateRoads()
        self.traffic_lights = generateLights(self.roads, self.mySink)
        self.newCars()

    def newCars(self):
        numberOfCarsAdded = p.poisson(1,1)[0]
        count = 0
        while count < numberOfCarsAdded:
            count += 1
            light = r.choice([0,0,0,0,1,2,3,3,3])
            if light == 0:
                direction = r.choice(["E","N"])
            elif light == 1:
                direction = r.choice(["W","N"])
            elif light == 2:
                direction = r.choice(["S","W"])
            elif light == 3:
                direction = r.choice(["E","S"])
            self.roads[light][direction].moveCarsTo(Car(light, direction))

    def __str__(self):
        print("*******")
        print(self.traffic_lights[0])
        print(self.traffic_lights[1])
        print(self.traffic_lights[2])
        print(self.traffic_lights[3])

    def getState(self):
        state = []
        for light in self.traffic_lights:
            state.append(light.getTotals())
        return state

    def updateState(self, control):
        i = 0
        for light in control:
            self.traffic_lights[i].changeLight(light)
            i += 1

        self.newCars()
        self.traffic_lights[0].updateCars()
        self.traffic_lights[1].updateCars()
        self.traffic_lights[2].updateCars()
        self.traffic_lights[3].updateCars()

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