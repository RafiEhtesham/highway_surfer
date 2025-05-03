from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def drawTrain(train_pos, num_cars=3):
    """
    Draws a train with a locomotive and a specified number of cars.
    :param train_pos: Tuple (x, y, z) specifying the position of the train.
    :param num_cars: Number of cars to attach to the locomotive.
    """
    x, y, z = train_pos

    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(1.5, 1.5, 1.5)  # Scale the entire train for better visibility
    glRotatef(90, 0, 0, 1)  # Rotate 90 degrees on the Z-axis

    # Draw locomotive
    glPushMatrix()
    glColor3f(0.8, 0.1, 0.1)  # Red color for the locomotive
    glScalef(2, 1, 1)  # Scale to make it rectangular
    glutSolidCube(100)  # Locomotive body
    glPopMatrix()

    # Draw chimney on the locomotive
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)  # Dark gray for the chimney
    glTranslatef(50, 0, 60)  # Position on top of the locomotive
    gluCylinder(gluNewQuadric(), 10, 10, 40, 10, 10)  # Chimney
    glPopMatrix()

    # Draw train cars
    for i in range(num_cars):
        glPushMatrix()
        glColor3f(0.1, 0.1, 0.8)  # Blue color for the cars
        glTranslatef(-150 * (i + 1), 0, 0)  # Position each car behind the locomotive
        glScalef(2, 1, 1)  # Scale to make it rectangular
        glutSolidCube(100)  # Train car body
        glPopMatrix()

    glPopMatrix()

def drawTrainObstacle(train_pos, num_cars=1):
    """
    Wrapper function to draw a train obstacle.
    :param train_pos: Tuple (x, y, z) specifying the position of the train.
    :param num_cars: Number of cars to attach to the locomotive.
    """
    drawTrain(train_pos, num_cars)

