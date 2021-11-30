from .car import Car

class Sink:
    def __init__(self):
        self.queue = []


    def moveCarsTo(self, newCar):
        if newCar is not None:
            self.queue.append(newCar)
        return None

    def __str__(self):
        totalTime = 0
        for car in self.queue:
            totalTime += car.getTotalTime()
        l = len(self.queue)
        if l == 0:
            return '0'
        return str(totalTime/l) + "  Cars: " + str(l)