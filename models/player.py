from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def drawPlayer(player_pos, is_sliding, slide_rotation_angle):
    x, y, z = player_pos  # Unpack player position

    glPushMatrix()  # Save the current matrix state
    glTranslatef(x, y, z)  # Move to player position

    if is_sliding:
        # Apply gradual rotation during the slide
        glRotatef(-slide_rotation_angle, 1, 0, 0)  # Rotate on the x-axis
        glRotatef(slide_rotation_angle, 0, 0, 1)  # Rotate on the z-axis

    glPushMatrix()  # Save the current matrix state
    # glColor3f(1, 0, 0)
    # glTranslatef(0, 0, 0)  
    # glutSolidCube(60) # Take cube size as the parameter
    # glTranslatef(0, 0, 100) 
    # glColor3f(0, 1, 0)
    # glutSolidCube(60) 

    # glColor3f(1, 1, 0)
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100) 
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    glTranslatef(0, 100, 0)

    # wheels
    glColor3f(0, 0, 0) # Set color to black
    glTranslatef(0, 0, 0)  # Move to the origin
    glScalef(0.5, 1, 1)  # Scale down the sphere
    gluSphere(gluNewQuadric(), 40, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glTranslatef(0, -200, 0)  # Move to the front wheel position
    gluSphere(gluNewQuadric(), 40, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glTranslatef(0, 100, 0)  # Move back to the origin
    
    
    # body of the bike
    glColor3f(0.5, 0, 0)  # Set color to blue
    glTranslatef(0, 0, 25)
    glScalef(0.5, 1, 0.25)
    glutSolidCube(200)  # Draw the body of the bike
    
    glRotatef(15, 1, 0, 0)  # Rotate the bike to face the correct direction

    #body of the biker
    glColor3f(0.6, 0.3, 0)  # Set color to brown
    glTranslatef(0, 50, 175)  # Move to the position of the biker
    glScalef(5, 1, 4)  # Scale down the biker
    glutSolidCube(50)  # Draw the body of the biker
    glScalef(0.2, 1, 0.25)  # Scale down the biker's body
    glTranslatef(0, 0, -200)  # Move to the position of the biker
    glRotatef(-15, 1, 0, 0)  # Rotate the bike to face the correct direction

    glPopMatrix()  # Restore the previous matrix state

    glPushMatrix()  # Save the current matrix state

    # head of the biker
    glColor3f(1, 0.8, 0.6)  # Set color to skin tone
    glTranslatef(0, -30, 115)  # Move to the position of the head
    glutSolidSphere(20, 10, 10)  # Draw the head

    #legs of the biker
    glColor3f(0, 0, 0.5)  # Set color to dark blue
    
    glTranslatef(35, 50, -90) 
    glScalef(0.25, 0.75, 0.75)  # Scale down the legs
    glRotatef(-45, 1, 0, 0)  # Rotate the legs to face downwards
    glScalef(1, 1, 0.65)  # Scale down the legs
    glutSolidCube(50)
    glTranslatef(-280, 0, 0)  # Move to the position of the other leg
    glutSolidCube(50)

    glPopMatrix()  # Restore the previous matrix state

    glPushMatrix()  # Save the current matrix state

    # left hand of the biker
    glTranslatef(30, 0, 0)  # Move to the position of the biker's hands
    glColor3f(1, 0.8, 0.6)  # Set color to skin tone
    glTranslatef(0, -50, 65)  # Move to the position of the hands
    glRotatef(-60, 1, 0, 0)  # Rotate the hands to face forward
    glScalef(0.25, 0.25, 1.5)  # Scale down the hands
    glRotatef(45, 1, 0, 0)  # Rotate the hands to face forward
    glutSolidCube(50)  # Draw the hands

    glPopMatrix()  # Restore the previous matrix state

    glPushMatrix()  # Save the current matrix state

    # right hand of the biker
    glTranslatef(-30, 0, 0)  # Move to the position of the biker's hands
    glColor3f(1, 0.8, 0.6)  # Set color to skin tone
    glTranslatef(0, -50, 65)  # Move to the position of the hands
    glRotatef(-60, 1, 0, 0)  # Rotate the hands to face forward
    glScalef(0.25, 0.25, 1.5)  # Scale down the hands
    glRotatef(45, 1, 0, 0)  # Rotate the hands to face forward
    glutSolidCube(50)  # Draw the hands

    glPopMatrix()  # Restore the previous matrix state
    glPopMatrix()  # Restore the previous matrix state

