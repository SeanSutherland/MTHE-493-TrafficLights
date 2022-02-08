import random as r
import math


class Car:

    direction = {
        "N": 0,
        "S": 1,
        "E": 2,
        "W": 3
    }

    def __init__(self, source, sourceDirection, d):
        self.source = source
        self.dimension = d
        self.sq = int(math.sqrt(d))
        self.path = [sourceDirection]
        self.locations = [source]
        self.generatePath()
        self.time = {}
        self.path.pop(0)

    def generatePath(self):
        opts = ["N", "S", "E", "E", "E", "E", "W", "W", "W", "W"]
        removed = 0

        if self.source % self.sq == 0:
            removed += 1
            opts.remove("W")

        elif self.source + 1 % self.sq == 0:
            removed += 1
            opts.remove("E")

        if self.source < self.sq:
            removed += 1
            opts.remove("S")
            if removed == 1:
                removed += 1
                opts.remove(r.choice(["E", "W"]))
        elif self.source >= self.sq*(self.sq-1):
            removed += 1
            opts.remove("N")
            if removed == 1:
                removed += 1
                opts.remove(r.choice(["E", "W"]))

        if removed == 1:
            opts.remove(r.choice(["N", "S"]))

        next_2 = 0
        while next_2 != self.dimension:
            next_1, next_2 = getRandomTurn(
                self.locations[-1], opts, self.dimension, self.sq)
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
        try:
            self.time[4-len(self.path)] += 1
        except:
            self.time[4-len(self.path)] = 1

    def getTime(self):
        return self.time[4-len(self.path)]

    def getTotalTime(self):
        return sum(self.time)

    def __str__(self):
        a = sum(self.time)
        if a > 0:
            return str(a)
        return ""


def getRandomTurn(location, opts, d, sq):

    direction = r.choice(opts)
    nextLocal = d

    if direction == "N":
        nextLocal = location + sq
    elif direction == "S":
        nextLocal = location - sq
    elif direction == "E":
        if location + 1 % sq != 0:
            nextLocal = location + 1
    elif direction == "W":
        if location % sq != 0:
            nextLocal = location - 1

    if nextLocal >= d or nextLocal < 0:
        nextLocal = d

    return[direction, nextLocal]
