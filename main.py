from OpenGL.GL import *
from OpenGL.GLUT import *  # Import all GLUT functions
from OpenGL.GLU import *
from models.player import drawPlayer   # Import all models from models.py
from models.barrier import drawbarrier1  # Import all models from barrier.py
from models.barrier import drawbarrier2  # Import all models from barrier.py
from models.text import draw_text  # Import all models from text.py
from math import cos, sin, radians  # Import math functions for angle calculations
import time
import random  # Import random module for obstacle generation

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
is_forced_landing = False  # Flag to track if the player is forced to land

# Moving related variables
is_moving = False  # Flag to track if the player is moving left or right
move_start_time = None  # Start time of the movement
move_duration = 0.2  # Duration of the left/right movement in seconds
move_target_x = None  # Target X position for the movement

# Sliding related variables
is_sliding = False  # Flag to track if the player is sliding
slide_start_time = None  # Start time of the slide
slide_duration = 0.7  # Duration of the slide in seconds
slide_rotation_angle = 0  # Current rotation angle during the slide
max_slide_rotation = 90  # Maximum rotation angle during the slide
sliding_speed = 5 # Speed of the slide rotation

# Game-related variables
obstacles = []  # List to store active obstacles
obstacle_speed = 300  # Speed at which obstacles move backward
obstacle_spawn_interval = 1  # Time interval (in seconds) to spawn new obstacles
last_obstacle_spawn_time = time.time()  # Time when the last obstacle was spawned
score = 0  # Player's score
game_over = False  # Flag to track if the game is over

def draw_shapes():

    global GRID_WIDTH, player_pos, is_sliding, slide_rotation_angle   

    # drawbarrier1((0, -200, 0), GRID_WIDTH)  # Draw the barrier at the player's position

    # drawbarrier2((0, -200, 0), GRID_WIDTH)  # Right lane
    
    drawPlayer(player_pos, is_sliding, slide_rotation_angle)

def spawnObstacle():
    """
    Spawns a new obstacle at a random lane and randomly selects its type.
    """
    global obstacles
    lane_index = random.choice([-1, 0, 1])  # Randomly choose a lane (-1, 0, 1)
    obstacle_type = random.choice(["barrier1", "barrier2"])  # Randomly choose obstacle type
    obstacle_pos = (lane_index * GRID_WIDTH / 1.5, -GRID_LENGTH, 0)  # Position at the far end (front)
    obstacles.append((obstacle_pos, obstacle_type))  # Add the obstacle with its type to the list

def updateObstacles():
    """
    Updates the positions of obstacles and removes those that go off-screen.
    """
    global obstacles, score, game_over

    new_obstacles = []
    for obstacle, obstacle_type in obstacles:
        x, y, z = obstacle
        y += obstacle_speed * delta_time  # Move the obstacle toward the player
        if y < GRID_LENGTH:  # Keep obstacles within the screen
            new_obstacles.append(((x, y, z), obstacle_type))
        else:
            score += 1  # Increment score for dodging the obstacle

    obstacles = new_obstacles

    # Check for collisions
    for obstacle, obstacle_type in obstacles:
        if abs(obstacle[0] - player_pos[0]) < GRID_WIDTH / 6 and abs(obstacle[1] - player_pos[1]) < 50:
            if obstacle_type == "barrier1" and not is_sliding:
                # Collision with barrier1 if not sliding
                game_over = True
                print(f"[DEBUG] Collision with barrier1! Game Over. Final Score: {score}")
            elif obstacle_type == "barrier2" and not is_jumping:
                # Collision with barrier2 if not jumping
                game_over = True
                print(f"[DEBUG] Collision with barrier2! Game Over. Final Score: {score}")

def drawObstacles():
    """
    Draws all active obstacles on the screen.
    """
    for obstacle, obstacle_type in obstacles:
        if obstacle_type == "barrier1":
            drawbarrier1(obstacle, GRID_WIDTH)  # Use drawbarrier1 for obstacles
        elif obstacle_type == "barrier2":
            drawbarrier2(obstacle, GRID_WIDTH)  # Use drawbarrier2 for obstacles

def resetGame():
    """
    Resets the game state after a game over.
    """
    global player_pos, obstacles, score, game_over
    player_pos = (0, 0, 0)  # Reset player position
    obstacles = []  # Clear all obstacles
    score = 0  # Reset score
    game_over = False  # Reset game over flag
    print("[DEBUG] Game reset.")

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
    global is_jumping, jump_start_time, is_moving, move_start_time, move_target_x, is_sliding, slide_start_time, slide_rotation_angle, is_forced_landing, game_over

    if game_over and key == b'r':
        resetGame()  # Restart the game
        return

    print(f"[DEBUG] Key pressed: {key}")  # Debug

    # Move left (A key)
    if key == b'a' and not is_moving:
        x, y, z = player_pos
        target_x = x + 400
        if abs(target_x) < GRID_WIDTH:
            is_moving = True
            move_start_time = time.time()
            move_target_x = target_x
            print(f"[DEBUG] Moving left. target_x: {target_x}, player_pos: {player_pos}")  # Debug

    # Move right (D key)
    if key == b'd' and not is_moving:
        x, y, z = player_pos
        target_x = x - 400
        if abs(target_x) < GRID_WIDTH:
            is_moving = True
            move_start_time = time.time()
            move_target_x = target_x
            print(f"[DEBUG] Moving right. target_x: {target_x}, player_pos: {player_pos}")  # Debug

    # Jump (W key)
    if key == b'w' and not is_jumping:
        is_jumping = True
        jump_start_time = time.time()  # Record the start time of the jump
        print(f"[DEBUG] Jump initiated. jump_start_time: {jump_start_time}, player_pos: {player_pos}")  # Debug
        if is_sliding:
            # End the slide if jumping
            is_sliding = False
            slide_rotation_angle = 0  # Reset rotation angle
            print(f"[DEBUG] Slide ended due to jump.")  # Debug

    # Slide (S key)
    if key == b's' and not is_sliding:
        if is_jumping:
            # Trigger a smooth forced landing
            is_forced_landing = True
            print(f"[DEBUG] Forced landing triggered.")  # Debug
        else:
            is_sliding = True
            slide_start_time = time.time()  # Record the start time of the slide
            print(f"[DEBUG] Slide initiated. slide_start_time: {slide_start_time}")  # Debug

def updatePlayerMovement():
    """
    Updates the player's position during left/right movement.
    """
    global player_pos, is_moving, move_start_time, move_target_x

    if not is_moving:
        return  # No movement in progress

    elapsed_time = time.time() - move_start_time
    print(f"[DEBUG] Movement elapsed_time: {elapsed_time}, move_duration: {move_duration}")  # Debug
    if elapsed_time >= move_duration:
        # End the movement and snap to the target position
        x, y, z = player_pos
        player_pos = (move_target_x, y, z)
        is_moving = False
        print(f"[DEBUG] Movement ended. player_pos: {player_pos}")  # Debug
    else:
        # Interpolate the X position based on elapsed time
        t = elapsed_time / move_duration  # Normalized time (0 to 1)
        start_x, y, z = player_pos
        x = start_x + t * (move_target_x - start_x)
        player_pos = (x, y, z)
        print(f"[DEBUG] Moving. player_pos: {player_pos}")  # Debug

def updatePlayerJump():
    """
    Updates the player's position during a jump.
    """
    global player_pos, is_jumping, jump_start_time, is_forced_landing

    if not is_jumping:
        return  # No jump in progress

    elapsed_time = time.time() - jump_start_time
    print(f"[DEBUG] Jump elapsed_time: {elapsed_time}, jump_duration: {jump_duration}")  # Debug
    if elapsed_time >= jump_duration or is_forced_landing:
        # Smoothly return to the ground if forced landing is triggered
        x, y, z = player_pos
        descent_time = elapsed_time / jump_duration if is_forced_landing else 0
        player_pos = (x, y, z * (1 - descent_time))
        print(f"[DEBUG] Jump landing. player_pos: {player_pos}, is_forced_landing: {is_forced_landing}")  # Debug
        if z <= 10:  # Close enough to the ground
            player_pos = (x, y, 0)
            is_jumping = False
            is_forced_landing = False
            print(f"[DEBUG] Jump ended. player_pos: {player_pos}")  # Debug
    else:
        # Calculate the vertical position using a parabolic trajectory
        t = elapsed_time / jump_duration  # Normalized time (0 to 1)
        height = jump_height * (1 - (2 * t - 1) ** 2)  # Parabolic equation
        x, y, z = player_pos
        player_pos = (x, y, height)
        print(f"[DEBUG] Jumping. player_pos: {player_pos}")  # Debug

def updatePlayerSlide():
    """
    Updates the player's state during a slide.
    """
    global is_sliding, slide_start_time, slide_rotation_angle, sliding_speed

    if not is_sliding:
        return  # No slide in progress

    elapsed_time = time.time() - slide_start_time
    print(f"[DEBUG] Slide elapsed_time: {elapsed_time}, slide_duration: {slide_duration}")  # Debug
    if elapsed_time >= slide_duration:
        # End the slide and reset the player's rotation
        is_sliding = False
        slide_rotation_angle = 0  # Reset rotation angle
        print(f"[DEBUG] Slide ended. slide_rotation_angle: {slide_rotation_angle}")  # Debug
    else:
        # Gradually increase the rotation angle during the slide
        t = elapsed_time / slide_duration  # Normalized time (0 to 1)
        new_slide_rotation_angle = t * max_slide_rotation * sliding_speed
        slide_rotation_angle = min(new_slide_rotation_angle, max_slide_rotation)
        print(f"[DEBUG] Sliding. slide_rotation_angle: {slide_rotation_angle}")  # Debug

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos

    print(f"[DEBUG] Special key pressed: {key}")  # Debug

    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += 50  # Small angle decrement for smooth movement
        print(f"[DEBUG] Camera moved up. camera_pos: {camera_pos}")  # Debug

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= 50  # Small angle increment for smooth movement
        print(f"[DEBUG] Camera moved down. camera_pos: {camera_pos}")  # Debug

    # Move camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        angle = -10  # Angle decrement for rotation to the left
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y  # Update camera position
        print(f"[DEBUG] Camera moved left. camera_pos: {camera_pos}")  # Debug

    # Move camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        angle = 10  # Angle increment for rotation
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
        print(f"[DEBUG] Camera moved right. camera_pos: {camera_pos}")  # Debug

    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

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
    - Spawns and updates obstacles.
    - Triggers screen redraw for real-time updates.
    """
    global last_obstacle_spawn_time

    if game_over:
        return  # Stop updating if the game is over

    updateDeltaTime()  # Update delta time
    updatePlayerMovement()  # Update the player's left/right movement
    updatePlayerJump()  # Update the player's jump
    updatePlayerSlide()  # Update the player's slide
    updateObstacles()  # Update obstacle positions

    # Spawn new obstacles at regular intervals
    if time.time() - last_obstacle_spawn_time > obstacle_spawn_interval:
        spawnObstacle()
        last_obstacle_spawn_time = time.time()

    glutPostRedisplay()  # Ensure the screen updates with the latest changes

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything on the screen.
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 600, 900)  # Set viewport size

    setupCamera()  # Configure camera perspective

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

    # Display game info text
    draw_text(10, 770, f"Score: {score}")
    if game_over:
        draw_text(200, 450, "GAME OVER! Press R to Restart")

    
    drawObstacles()  # Draw dynamic obstacles
    draw_shapes()  # Draw player and static objects
    
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

