from tools.road import Road
from tools.light import Light
from tools.car import Car
from tools.sink import Sink
import time
import random as r

mySink = Sink()

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

def newCars():
    numberOfCarsAdded = r.randint(0,5)
    count = 0
    while count < numberOfCarsAdded:
        count += 1
        light = r.randint(0,3)
        if light == 0:
            direction = r.choice(["E","N"])
        elif light == 1:
            direction = r.choice(["W","N"])
        elif light == 2:
            direction = r.choice(["S","W"])
        elif light == 3:
            direction = r.choice(["E","S"])
        roads[light][direction].moveCarsTo(Car(0))

def sim(): 
    print("*******")
    print(traffic_lights[0])
    print(traffic_lights[1])
    print(traffic_lights[2])
    print(traffic_lights[3])

newCars()
while True:
    time.sleep(1)
    newCars()
    traffic_lights[0].updateCars()
    traffic_lights[1].updateCars()
    traffic_lights[2].updateCars()
    traffic_lights[3].updateCars()
    sim()
