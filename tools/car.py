class Car:

    direction = {
        "N":0,
        "S":1,
        "E":2,
        "W":3
    }

    def __init__(self):
        self.path = generatePath()
        self.time = []
        #self.location = self.path[0]

    def generatePath(self):
        return [2,0,3,0]

    def getNext(self):
        return self.path.pop(0)