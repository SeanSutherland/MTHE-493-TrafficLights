import random as r
import math

class Car:

    direction = {
        "N":0,
        "S":1,
        "E":2,
        "W":3
    }

    def __init__(self, source, sourceDirection):
        self.source = source
        self.path = [sourceDirection]
        self.locations = [source]
        self.generatePath()
        self.time = [0,0,0,0,0]
        self.path.pop(0)

    def generatePath(self):
        l = r.choice([3,3,3,4,4,4,5])

        while len(self.path) < l:
            next_1, next_2 = getRandomTurn(self.locations[-1], self.path[-1], len(self.path), l)
            self.path.append(next_1)
            self.locations.append(next_2)

    def getNext(self):
        try:
            return self.direction[self.path.pop(0)]
        except:
            print(self.path)
            print(self.locations)
            return

    def addTime(self):
        self.time[4-len(self.path)] += 1

    def getTime(self):
        return self.time[4-len(self.path)]

    def getTotalTime(self):
        return sum(self.time)

    def __str__(self):
        a  = sum(self.time)
        if a > 0:
            return str(a)
        return ""

def getRandomTurn(location, previousDirection, length, l):
    if location == 0:
        if length == l-1:
            return [r.choice(["W", "S"]),5]
        elif previousDirection == "S":
            return ["E", 1]
        elif previousDirection == "W":
            return ["N", 3]
        else:
            opt = [["N",3],["E",1]]
        return r.choice(opt)

    elif location == 1:
        if length == l-1:
            return [r.choice(["E", "S"]),5]
        elif previousDirection == "S":
            return ["W", 0]
        elif previousDirection == "E":
            return ["N", 2]
        else:
            opt = [["N",2],["W",0]]
        return r.choice(opt)

    elif location == 2:
        if length == l-1:
            return [r.choice(["N", "E"]),5]
        elif previousDirection == "N":
            return ["W", 3]
        elif previousDirection == "E":
            return ["S", 1]
        else:
            opt = [["S",1],["W",3]]
        return r.choice(opt)

    elif location == 3:
        if length == l-1:
            return [r.choice(["W", "N"]),5]
        elif previousDirection == "W":
            return ["S", 0]
        elif previousDirection == "N":
            return ["E", 2]
        else:
            opt = [["S",0],["E",2]]
        return r.choice(opt)



   
