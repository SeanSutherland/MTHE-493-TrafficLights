from graphics import *
import time

class GUI():
    def __init__(self):
        self.cars = []
        self.roads = {
                0: {
                    "N": Text(Point(130, 450), '0 cars'),
                    "S": Text(Point(70, 250), '0 cars'),
                    "E": Text(Point(50, 420), '0 cars'),
                    "W": Text(Point(250, 380), '0 cars'),
                },
                1:{
                    "N": Text(Point(430, 450), '0 cars'),
                    "S": Text(Point(370, 250), '0 cars'),
                    "E": Text(Point(250, 420), '0 cars'), 
                    "W": Text(Point(450, 380), '0 cars'), 
                },
                2:{
                    "N":Text(Point(430, 250), '0 cars'),
                    "S":Text(Point(370, 50), '0 cars'),
                    "E":Text(Point(250, 120), '0 cars'),
                    "W":Text(Point(450, 80), '0 cars'),
                },
                3:{
                    "N":Text(Point(130, 250), '0 cars'),
                    "S":Text(Point(70, 50), '0 cars'),
                    "E":Text(Point(50, 120), '0 cars'),
                    "W":Text(Point(250, 80), '0 cars'),
                }
            }

        # Initialize window
        self.win = GraphWin(width = 500, height=500)

        
        self.text = Text(Point(250, 250), 'Cars out: 0\nAvg_wait: 0s')
        self.text.draw(self.win).setFill('black')

        # X - right
        Line(Point(50, 105), Point(450, 105)).draw(self.win).setFill('red')
        Line(Point(450, 405), Point(50, 405)).draw(self.win).setFill('red')
        # X - left
        Line(Point(50, 95), Point(450, 95)).draw(self.win).setFill('blue')
        Line(Point(450, 395), Point(50, 395)).draw(self.win).setFill('blue')
        # Y - up
        Line(Point(405, 50), Point(405, 450)).draw(self.win).setFill('red')
        Line(Point(105, 450), Point(105, 50)).draw(self.win).setFill('red')
        # Y - down
        Line(Point(395, 50), Point(395, 450)).draw(self.win).setFill('blue')
        Line(Point(95, 450), Point(95, 50)).draw(self.win).setFill('blue')


        for intersection in self.roads.values():
            for road in intersection.values():
                road.draw(self.win)


        # Lights
        Circle(Point(100, 100), 25).draw(self.win).setFill('white')
        Circle(Point(400, 100), 25).draw(self.win).setFill('white')
        Circle(Point(400, 400), 25).draw(self.win).setFill('white')
        Circle(Point(100, 400), 25).draw(self.win).setFill('white')

        self.directions = []

        for a in [[100,400],[400,400],[400,100],[100,100]]:
                self.directions.append([Oval(Point(a[0]-5, a[1]-20), Point(a[0]+5, a[1]+20)),Oval(Point(a[0]-20, a[1]-5), Point(a[0]+20, a[1]+5))])

        for a in self.directions:
            a[0].draw(self.win).setFill('green')
            a[1].draw(self.win).setFill('red')

    def update(self, roads, lights, sink):
        a = [[100,400],[400,400],[400,100],[100,100]]
        self.text.setText('Cars out: ' + str(sink[0]) + '\nAvg_wait: ' + str(sink[1]) + 's')

        for car in self.cars:
            car.move(600,0)
        self.cars = []

        for intersection in roads.keys():
            for road in roads[intersection].keys():
                pos = [a[intersection][0],a[intersection][1]]
                change = [0,0]
                if road == "N":
                    pos[0] += 5
                    pos[1] += 30
                    change[1] = 10
                elif road == "S":
                    pos[0] -= 5
                    pos[1] -= 30
                    change[1] = -10
                elif road == "E":
                    pos[0] -= 30
                    pos[1] += 5
                    change[0] = -10
                elif road == "W":
                    pos[0] += 30
                    pos[1] -= 5
                    change[0] = 10


                for i in range(roads[intersection][road]):
                    self.cars.append(Circle(Point(pos[0], pos[1]), 5))
                    pos[0] += change[0]
                    pos[1] += change[1]

                    
                self.roads[intersection][road].setText(str(roads[intersection][road]) + " cars")

        for car in self.cars:
            car.draw(self.win).setFill('black')
                

        i = 0 
        for l in lights:
            if l == 0:
                self.directions[i][1].setFill('red')
                self.directions[i][0].setFill('green')
            elif l == 1: 
                self.directions[i][0].setFill('red')
                self.directions[i][1].setFill('green')
            else: 
                self.directions[i][0].setFill('red')
                self.directions[i][1].setFill('red')
            i += 1
