class Road:
    def __init__(self):
        self.status = 0
        self.queue = []
        self.numberOfCars = 0

    def moveCarsTo(self, newCar):
        if newCar is not None:
            self.queue.append(newCar)
            self.numberOfCars += 1
        return None

    def moveCarsFrom(self):
        if len(self.queue) > 0   and self.queue[0].getTime() > 0:
            self.numberOfCars -= 1
            return self.queue.pop(0)
        return None

    def timeStep(self):
        for car in self.queue:
            car.addTime()
        return

    def getNumberOfCars(self):
        return self.numberOfCars
    
    def __str__(self):
        return str(len(self.queue))