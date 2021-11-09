from tools.road import Road
from tools.light import Light
from tools.car import Car
from tools.sink import Sink
import time

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
    roads[0],
    [roads[3]["N"], mySink ,roads[1]["E"], mySink]
), Light(
    roads[1],
    [roads[2]["N"], mySink ,mySink, roads[0]["W"]]
), Light(
    roads[2],
    [mySink, roads[1]["S"] ,mySink, roads[3]["W"]]
), Light(
    roads[3],
    [mySink, roads[0]["S"] ,roads[2]["E"], mySink]
)]

def newCars():
    roads[0]["E"].moveCarsTo(Car())

while True:
    time.sleep(1)
    traffic_lights[0].updateCars()
    traffic_lights[1].updateCars()
    traffic_lights[2].updateCars()
    traffic_lights[3].updateCars()
    print(roads)
