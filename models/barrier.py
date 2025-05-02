from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def drawbarrier1(barrier_pos, g_width, lane_index=1):
    x, y, z = barrier_pos
    # Adjust x based on lane_index: 0=left, 1=center, 2=right
    if lane_index == 0:  # left
        x -= 400
    elif lane_index == 2:  # right
        x += 400
    # else lane_index == 1, center, x unchanged
    glPushMatrix()
    glTranslatef(x, y, z)
    lane_width = g_width / 3
    stand_x_pos = lane_width - 10
    stand_height = 200
    cuboid_height = 50
    cuboid_z_pos = stand_height + (cuboid_height / 2)
    stand_thickness = 0.2 * 50
    # Left stand
    glPushMatrix()
    glColor3f(0.9, 0.7, 0.5)
    glTranslatef(-stand_x_pos, 0, stand_height / 2)
    glScalef(0.2, 0.2, 4)
    glutSolidCube(50)
    glPopMatrix()
    # Right stand
    glPushMatrix()
    glTranslatef(stand_x_pos, 0, stand_height / 2)
    glScalef(0.2, 0.2, 4)
    glutSolidCube(50)
    glPopMatrix()
    # Diagonal red-white striped cuboid
    extended_height_scale = 3
    cube_size = 50
    half_extended = (cube_size * extended_height_scale) / 2
    cuboid_half_length = (stand_x_pos - 5)
    z_pos = stand_height + cube_size / 2 - (half_extended - cube_size / 2)
    stripe_count = 10
    stripe_width = (cuboid_half_length * 2) / stripe_count
    stripe_thickness = 0.5
    diagonal_angle = 20
    for i in range(stripe_count):
        color = (1, 0, 0) if i % 2 == 0 else (1, 1, 1)
        x_offset = -cuboid_half_length + (i + 0.5) * stripe_width
        glPushMatrix()
        glColor3f(*color)
        glTranslatef(x_offset, 0, z_pos)
        glRotatef(diagonal_angle, 0, 0, 1)
        glScalef(stripe_width / cube_size, stripe_thickness, extended_height_scale)
        glutSolidCube(cube_size)
        glPopMatrix()
    glPopMatrix()

def drawbarrier2(barrier_pos, g_width, lane_index=0):
    x, y, z = barrier_pos
    # Adjust x based on lane_index: 0=left, 1=center, 2=right
    if lane_index == 0:  # left
        x -= 400
    elif lane_index == 2:  # right
        x += 400
    # else lane_index == 1, center, x unchanged
    glPushMatrix()
    glTranslatef(x, y, z)
    lane_width = g_width / 3
    stand_x_pos = lane_width - 10
    stand_height = 200
    cuboid_height = 50
    cuboid_z_pos = 0
    extended_height_scale = 3
    cube_size = 50
    half_extended = (cube_size * extended_height_scale) / 2
    cuboid_half_length = (stand_x_pos - 5)
    z_pos = 30
    stripe_count = 10
    stripe_width = (cuboid_half_length * 2) / stripe_count
    stripe_thickness = 0.5
    diagonal_angle = 20
    for i in range(stripe_count):
        color = (1, 0, 0) if i % 2 == 0 else (1, 1, 1)
        x_offset = -cuboid_half_length + (i + 0.5) * stripe_width
        glPushMatrix()
        glColor3f(*color)
        glTranslatef(x_offset, 0, z_pos)
        glRotatef(diagonal_angle, 0, 0, 1)
        glScalef(stripe_width / cube_size, stripe_thickness, 1)
        glutSolidCube(cube_size)
        glPopMatrix()
    glPopMatrix()