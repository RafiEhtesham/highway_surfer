from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def drawbarrier1(barrier_pos, g_width):
    x, y, z = barrier_pos
    lane_width = g_width / 3
    stand_x_pos = lane_width - 10

    stand_height = 200  # height of each stand (4 * 50)
    cuboid_height = 50  # height of horizontal cuboid
    cuboid_z_pos = stand_height + (cuboid_height / 2)  # top aligned exactly with stands

    stand_thickness = 0.2 * 50  # stand width after scaling

    # Left stand
    glPushMatrix()
    glColor3f(0.9, 0.7, 0.5)
    glTranslatef(-stand_x_pos, y, stand_height / 2)
    glScalef(0.2, 0.2, 4)
    glutSolidCube(50)
    glPopMatrix()

    # Right stand
    glPushMatrix()
    glTranslatef(stand_x_pos, y, stand_height / 2)
    glScalef(0.2, 0.2, 4)
    glutSolidCube(50)
    glPopMatrix()

    # Diagonal red-white striped cuboid
    extended_height_scale = 3
    cube_size = 50
    half_extended = (cube_size * extended_height_scale) / 2

    cuboid_half_length = (stand_x_pos - 5)
    z_pos = stand_height + cube_size / 2 - (half_extended - cube_size / 2)

    stripe_count = 10  # Number of diagonal stripes
    stripe_width = (cuboid_half_length * 2) / stripe_count
    stripe_thickness = 0.5  # Thin to look like a stripe
    diagonal_angle = 20  # degrees to rotate for diagonal look

    for i in range(stripe_count):
        color = (1, 0, 0) if i % 2 == 0 else (1, 1, 1)  # Alternate red and white
        x_offset = -cuboid_half_length + (i + 0.5) * stripe_width

        glPushMatrix()
        glColor3f(*color)
        glTranslatef(x_offset, y, z_pos)
        glRotatef(diagonal_angle, 0, 0, 1)  # Rotate around Z-axis for diagonal
        glScalef(stripe_width / cube_size, stripe_thickness, extended_height_scale)
        glutSolidCube(cube_size)
        glPopMatrix()



