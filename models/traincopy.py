from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class Train:
    def __init__(self, lane):
        self.lane = lane
        self.position = -1800
        self.speed = 0
        self.carriages = []
        
        for i in range(3):
            self.carriages.append({
                'offset': i * 250,
                'color': (0.8, 0.2, 0.2) if i%2 else (0.7, 0.7, 0.7)
            })

    def update(self, delta_time):
        self.position += self.speed * delta_time

    def draw(self):
        x = (self.lane - 1) * 400
        for carriage in self.carriages:
            glPushMatrix()
            glTranslatef(x, self.position + carriage['offset'], 50)
            glColor3f(*carriage['color'])
            glutSolidCube(200)
            
            # Wheels
            glColor3f(0.1, 0.1, 0.1)
            for wheel_x in [-80, 80]:
                for wheel_z in [-80, 80]:
                    glPushMatrix()
                    glTranslatef(wheel_x, 0, wheel_z)
                    glutSolidCube(40)
                    glPopMatrix()
            glPopMatrix()

class TrainManager:
    def __init__(self, base_speed=700.0):  # Fixed constructor
        self.trains = []
        self.base_speed = base_speed
        self.last_spawn = 0
        
    def update(self, delta_time):
        if glutGet(GLUT_ELAPSED_TIME) - self.last_spawn > 3000:
            self.trains.append(Train(lane=random.randint(0, 2)))
            self.last_spawn = glutGet(GLUT_ELAPSED_TIME)
        
        for train in self.trains:
            train.speed = self.base_speed
            train.update(delta_time)
        self.trains = [t for t in self.trains if t.position < 1800]

    def draw(self):
        for train in self.trains:
            train.draw()

    def set_speed(self, speed):
        self.base_speed = max(100, min(1500, speed))

    def get_occupied_positions(self):
        return [
            (train.lane, train.position - 100, train.position + 750)
            for train in self.trains
        ]