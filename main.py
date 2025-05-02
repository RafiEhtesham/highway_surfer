from OpenGL.GL import *
from OpenGL.GLUT import *  # Import all GLUT functions
from OpenGL.GLU import *
from models.player import drawPlayer   # Import all models from models.py
from models.barrier import drawbarrier1  # Import all models from barrier.py
from models.barrier import drawbarrier2  # Import all models from barrier.py
from models.text import draw_text  # Import all models from text.py
from math import cos, sin, radians  # Import math functions for angle calculations
import time
from models.trains import TrainManager

# Camera-related variables
camera_pos = (0, 350, 250)
look_at = (0, 150, 0)  # Target point for the camera to look at (looking further ahead)

player_pos = (0, 0, 0)  # Player position
player_track = 1  # 0=left, 1=center, 2=right

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
is_forced_landing = False  # Flag to track if the player is forced to land

# Moving related variables
is_moving = False  # Flag to track if the player is moving left or right
move_start_time = None  # Start time of the movement
move_duration = 0.2  # Duration of the left/right movement in seconds
move_target_x = None  # Target X position for the movement

# Sliding related variables
is_sliding = False  # Flag to track if the player is sliding
slide_start_time = None  # Start time of the slide
slide_duration = 0.5  # Duration of the slide in seconds
slide_rotation_angle = 0  # Current rotation angle during the slide
max_slide_rotation = 90  # Maximum rotation angle during the slide
sliding_speed = 5 # Speed of the slide rotation


# Train manager instance
train_manager = None

def init_game():
    """Initialize game and train manager"""
    global train_manager
    train_manager = TrainManager(base_speed=8.0)  # Initialize train manager
    print("Game and train manager initialized successfully")

def draw_shapes():

    global GRID_WIDTH, player_pos, is_sliding, slide_rotation_angle

    drawbarrier1((0, -200, 0), GRID_WIDTH, lane_index=1)  # Draw the barrier at the player's position

    #drawbarrier2((0, -200, 0), GRID_WIDTH, lane_index=1)  # Right lane

    drawPlayer(player_pos, is_sliding, slide_rotation_angle)
    
    # Draw the trains
    if train_manager:
        train_manager.update_and_draw()

def updateDeltaTime():
    """Updates the delta time based on the current and last frame times."""
    global last_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

def keyboardListener(key, x, y):
    """Handles keyboard inputs for player movement, jumping, and speed control."""
    global is_jumping, jump_start_time, is_moving, move_start_time, move_target_x, player_track, is_sliding, slide_start_time, slide_rotation_angle, is_forced_landing
    

    # Move left (A key)
    if key == b'd' and not is_moving and player_track > 0:
        player_track -= 1
        is_moving = True
        move_start_time = time.time()
        move_target_x = (player_track - 1) * 400  # Adjusted to align with lane centers: -400, 0, 400

    # Move right (D key)
    if key == b'a' and not is_moving and player_track < 2:
        player_track += 1
        is_moving = True
        move_start_time = time.time()
        move_target_x = (player_track - 1) * 400  # Adjusted to align with lane centers: -400, 0, 400

    # Jump (W key)
    if key == b'w' and not is_jumping:
        is_jumping = True
        jump_start_time = time.time()  # Record the start time of the jump
        if is_sliding:
            # End the slide if jumping
            is_sliding = False
            slide_rotation_angle = 0  # Reset rotation angle

    # Slide (S key)
    if key == b's' and not is_sliding:
        if is_jumping:
            # Trigger a smooth forced landing
            is_forced_landing = True
        else:
            is_sliding = True
            slide_start_time = time.time()  # Record the start time of the slide
    
    # Speed control keys
    if key == b'+' or key == b'=':
        if train_manager:
            train_manager.set_speed(train_manager.base_speed + 1.0)
            print(f"Train speed increased to {train_manager.base_speed:.1f}")
    
    if key == b'-':
        if train_manager and train_manager.base_speed > 1.0:
            train_manager.set_speed(train_manager.base_speed - 1.0)
            print(f"Train speed decreased to {train_manager.base_speed:.1f}")

def updatePlayerMovement():
    """Updates the player's position during left/right movement."""
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
        start_x = player_pos[0]  # Use the current position as the start
        x = start_x + t * (move_target_x - start_x)
        player_pos = (x, player_pos[1], player_pos[2])

def updatePlayerJump():
    """
    Updates the player's position during a jump.
    """
    global player_pos, is_jumping, jump_start_time, is_forced_landing, jump_duration, jump_height

    if not is_jumping:
        return  # No jump in progress

    elapsed_time = time.time() - jump_start_time
    if elapsed_time >= jump_duration or is_forced_landing:
        # Smoothly return to the ground if forced landing is triggered
        x, y, z = player_pos
        descent_time = elapsed_time / jump_duration if is_forced_landing else 0
        player_pos = (x, y, z * (1 - descent_time))
        if z <= 0.1:  # Close enough to the ground
            player_pos = (x, y, 0)
            is_jumping = False
            is_forced_landing = False
    else:
        # Calculate the vertical position using a parabolic trajectory
        t = elapsed_time / jump_duration  # Normalized time (0 to 1)
        height = jump_height * (1 - (2 * t - 1) ** 2)  # Parabolic equation
        x, y, z = player_pos
        player_pos = (x, y, height)

def updatePlayerSlide():
    """
    Updates the player's state during a slide.
    """
    global is_sliding, slide_start_time, slide_rotation_angle, sliding_speed

    if not is_sliding:
        return  # No slide in progress

    elapsed_time = time.time() - slide_start_time
    if elapsed_time >= slide_duration:
        # End the slide and reset the player's rotation
        is_sliding = False
        slide_rotation_angle = 0  # Reset rotation angle
    else:
        # Gradually increase the rotation angle during the slide
        t = elapsed_time / slide_duration  # Normalized time (0 to 1)
        new_slide_rotation_angle = t * max_slide_rotation * sliding_speed
        slide_rotation_angle = min(new_slide_rotation_angle, max_slide_rotation)

def specialKeyListener(key, x, y):
    """Handles special key inputs (arrow keys) for adjusting the camera angle and height."""
    global camera_pos

    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += 50  # Small angle decrement for smooth movement

    # Move camera down (DOWN arrow key)
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
    """Handles mouse inputs (currently unused)."""
    pass

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
    - Updates player position for smooth lane transitions, jumps, and slides.
    - Triggers screen redraw for real-time updates.
    """
    updateDeltaTime()  # Update delta time
    updatePlayerMovement()  # Update the player's left/right movement
    updatePlayerJump()  # Update the player's jump
    updatePlayerSlide()  # Update the player's slide
    glutPostRedisplay()  # Ensure the screen updates with the latest changes


def showScreen():
    """Display function to render the game scene."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 600, 900)

    setupCamera()

    # Draw the road with 3 lanes
    glBegin(GL_QUADS)
    
    # Road base (dark gray)
    glColor3f(0.2, 0.2, 0.2)
    glVertex3f(-GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_WIDTH, -GRID_LENGTH, 0)
    
    glEnd()

    # Lane dividers (white lines)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    lane_width = GRID_WIDTH / 3  # Divide the road into 3 lanes
    for i in range(-1, 2):  # Draw 2 lane dividers
        if i != 0:  # Skip the center lane    
            x = i * lane_width * 2  # Adjust to place dividers correctly
            glVertex3f(x - 5, GRID_LENGTH, 0.1)  # Slightly above the road surface
            glVertex3f(x + 5, GRID_LENGTH, 0.1)
            glVertex3f(x + 5, -GRID_LENGTH, 0.1)
            glVertex3f(x - 5, -GRID_LENGTH, 0.1)
    glEnd()

    # Display game info text at a fixed screen position
    if train_manager:
        draw_text(10, 770, f"Train Speed: {train_manager.base_speed:.1f}")
        draw_text(10, 740, f"Use + and - keys to adjust train speed")
    
    # Draw player and other game objects
    draw_shapes()

    # Swap buffers for smooth rendering
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 900)
    glutInitWindowPosition(100, 20)
    wind = glutCreateWindow(b"3D OpenGL Train Game")

    # Initialize the game
    init_game()
    
    # Set up depth testing
    glEnable(GL_DEPTH_TEST)

    # Register callbacks
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()