from OpenGL.GL import *
from OpenGL.GLUT import *  # Import all GLUT functions
from OpenGL.GLU import *
from models.player import drawPlayer   # Import all models from models.py
from models.barrier import drawbarrier1  # Import all models from barrier.py
from models.barrier import drawbarrier2  # Import all models from barrier.py
from models.text import draw_text  # Import all models from text.py
from math import cos, sin, radians  # Import math functions for angle calculations
from models.ui import draw_ui  # Import all models from ui.py
import time



# Camera-related variables
camera_pos = (0, 350, 250)
look_at = (0, 0, 0)  # Target point for the camera to look at

player_pos = (0, 0, 0)  # Player position

fovY = 90  # Field of view
GRID_LENGTH = 1800  # Length of the grid (longer)
GRID_WIDTH = 600  # Width of the grid (shorter)

last_time = time.time()  # Initialize last_time for delta time calculation
delta_time = 0  # Time difference between frames

# Jumping related variables
is_jumping = False  # Flag to track if the player is jumping
jump_start_time = None  # Start time of the jump
jump_duration = 0.7  # Duration of the jump in seconds
jump_height = 200  # Maximum height of the jump

# Moving related variables
is_moving = False  # Flag to track if the player is moving left or right
move_start_time = None  # Start time of the movement
move_duration = 0.2  # Duration of the left/right movement in seconds
move_target_x = None  # Target X position for the movement

# Add a global flag to track whether the game is paused
is_paused = False

def draw_shapes():

    global GRID_WIDTH, player_pos 

    drawbarrier1((0, -200, 0), GRID_WIDTH, lane_index=1)  # Draw the barrier at the player's position

    #drawbarrier2((0, -200, 0), GRID_WIDTH, lane_index=1)  # Right lane

    drawPlayer(player_pos)

    


def updateDeltaTime():
    """
    Updates the delta time based on the current and last frame times.
    """
    global last_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global is_jumping, jump_start_time, is_moving, move_start_time, move_target_x

    # Move left (A key)
    if key == b'a' and not is_moving:
        x, y, z = player_pos
        target_x = x + 400
        if abs(target_x) < GRID_WIDTH:
            is_moving = True
            move_start_time = time.time()
            move_target_x = target_x

    # Move right (D key)
    if key == b'd' and not is_moving:
        x, y, z = player_pos
        target_x = x - 400
        if abs(target_x) < GRID_WIDTH:
            is_moving = True
            move_start_time = time.time()
            move_target_x = target_x

    # Jump (W key)
    if key == b'w' and not is_jumping:
        is_jumping = True
        jump_start_time = time.time()  # Record the start time of the jump

def updatePlayerMovement():
    """
    Updates the player's position during left/right movement.
    """
    global player_pos, is_moving, move_start_time, move_target_x

    if not is_moving:
        return  # No movement in progress

    elapsed_time = time.time() - move_start_time
    if elapsed_time >= move_duration:
        # End the movement and snap to the target position
        x, y, z = player_pos
        player_pos = (move_target_x, y, z)
        is_moving = False
    else:
        # Interpolate the X position based on elapsed time
        t = elapsed_time / move_duration  # Normalized time (0 to 1)
        start_x, y, z = player_pos
        x = start_x + t * (move_target_x - start_x)
        player_pos = (x, y, z)

def updatePlayerJump():
    """
    Updates the player's position during a jump.
    """
    global player_pos, is_jumping, jump_start_time

    if not is_jumping:
        return  # No jump in progress

    elapsed_time = time.time() - jump_start_time
    if elapsed_time >= jump_duration:
        # End the jump and reset the player's vertical position
        x, y, z = player_pos
        player_pos = (x, y, 0)
        is_jumping = False
    else:
        # Calculate the vertical position using a parabolic trajectory
        t = elapsed_time / jump_duration  # Normalized time (0 to 1)
        height = jump_height * (1 - (2 * t - 1) ** 2)  # Parabolic equation
        x, y, z = player_pos
        player_pos = (x, y, height)

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos

    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += 50  # Small angle decrement for smooth movement

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= 50  # Small angle increment for smooth movement

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        angle = -10  # Angle decrement for rotation to the left
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y  # Update camera position

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        angle = 10  # Angle increment for rotation
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y

    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for toggling pause/play and other interactions.
    """
    global is_paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse coordinates to normalized device coordinates
        mouse_x = (x / 600) * 2 - 1  # Assuming window width is 600
        mouse_y = -((y / 900) * 2 - 1)  # Assuming window height is 900

        # Check if the click is within the pause/play button area
        center_x = 0  # Center of the pause/play button
        center_y = 0.95  # Vertically aligned with the white bar
        button_width = 0.06  # Width of the button (matches play button width)
        button_height = 0.07  # Height of the button (matches play button height)

        if (center_x - button_width / 2 <= mouse_x <= center_x + button_width / 2 and
                center_y - button_height / 2 <= mouse_y <= center_y + button_height / 2):
            is_paused = not is_paused  # Toggle the pause state
            print(f"Pause state toggled: {'Paused' if is_paused else 'Playing'}")

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.5, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    look_at_x, look_at_y, look_at_z = look_at
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              look_at_x, look_at_y, look_at_z,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)
    


def idle():
    """
    Idle function that runs continuously:
    - Updates delta time for smooth movement.
    - Updates player position for smooth lane transitions and jumps.
    - Triggers screen redraw for real-time updates.
    """
    updateDeltaTime()  # Update delta time
    updatePlayerMovement()  # Update the player's left/right movement
    updatePlayerJump()  # Update the player's jump
    glutPostRedisplay()  # Ensure the screen updates with the latest changes


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 600, 900)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    # glPointSize(20)
    # glBegin(GL_POINTS)
    # glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # glEnd()

    # Draw the road with 3 lanes
    glBegin(GL_QUADS)
    
    # Road base (dark gray)
    glColor3f(0.2, 0.2, 0.2)
    glVertex3f(-GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_WIDTH, -GRID_LENGTH, 0)

    # Lane dividers (white lines)
    glColor3f(1, 1, 1)
    lane_width = GRID_WIDTH / 3  # Divide the road into 3 lanes
    for i in range(-1, 2):  # Draw 2 lane dividers
        if i != 0:  # Skip the center lane    
            x = i * lane_width
            glVertex3f(x - 1, GRID_LENGTH, 0.1)  # Slightly above the road surface
            glVertex3f(x + 1, GRID_LENGTH, 0.1)
            glVertex3f(x + 1, -GRID_LENGTH, 0.1)
            glVertex3f(x - 1, -GRID_LENGTH, 0.1)

    glEnd()

    # Display game info text at a fixed screen position
    #draw_text(10, 770, f"A Random Fixed Position Text")
    #draw_text(10, 740, f"See how the position and variable change?: ")

    # Switch to orthographic projection for UI rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)  # Ensure this matches the coordinate system in draw_restart_arrow
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Call the draw_ui function to render the white bar at the top
    draw_ui(is_paused)  # Pass the pause/play state to draw_ui

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(600, 900)  # Window size
    glutInitWindowPosition(100, 20)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()

