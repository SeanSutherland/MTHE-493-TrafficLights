import random as r
import math

class Car:

    direction = {
        "N":0,
        "S":1,
        "E":2,
        "W":3
    }

    def __init__(self, source):
        self.source = source
        self.path = self.generatePath()
        self.time = [0,0,0,0]
        self.location = source
        #self.location = self.path[0]

    def generatePath(self):
        if self.source == 0:
            path = [r.choice([self.direction["N"], self.direction["E"]])]
        elif self.source == 1:
            path = [r.choice([self.direction["N"], self.direction["W"]])]
        elif self.source == 2:
            path = [r.choice([self.direction["S"], self.direction["W"]])]
        elif self.source == 3:
            path = [r.choice([self.direction["S"], self.direction["E"]])]

        while len(path) < 3:
            next = r.randint(0,3)
            while abs(next-path[-1])==1 and (next+path[-1] == 5 or next+path[-1] == 1):
                next = r.randint(0,3)
            path.append(next)

        return path

    def getNext(self):
        return self.path.pop(0)

    def addTime(self):
        self.time[4-len(self.path)] += 1

    def getTime(self):
        return self.time[4-len(self.path)]

    def getRandomTurn(location, direction, length):
        if location == 0:
            if length == 3:
                
        elif location == 1:

        elif location == 2:

        elif location == 3:


    def __str__(self):
        a  = sum(self.time)
        if a > 0:
            return str(a)
        return ""