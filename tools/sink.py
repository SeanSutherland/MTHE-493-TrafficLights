class Sink:
    def __init__(self):
        self.queue = []


    def moveCarsTo(self, newCar):
        if newCar is not None:
            self.queue.append(newCar)
        return None

    def __str__(self):
        a = ""
        for car in self.queue:
            a += str(car)
        return a