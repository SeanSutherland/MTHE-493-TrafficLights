class Road:
    def __init__(self):
        self.status = 0
        self.queue = []

    def moveCarsTo(self, newCar):
        if newCar is not None:
            self.queue.append(newCar)
        return None

    def moveCarsFrom(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
    
    def __str__(self):
        return len(self.queue)