from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from models.player import drawPlayer
from models.barrier import drawbarrier1, drawbarrier2
from models.text import draw_text
from math import cos, sin, radians
import time
from models.trains import TrainManager
import random

# Camera-related variables
camera_pos = (0, 350, 250)
look_at = (0, 150, 0)

player_pos = (0, 0, 0)
player_track = 1  # 0=left, 1=center, 2=right

fovY = 90
GRID_LENGTH = 1800
GRID_WIDTH = 600

last_time = time.time()
delta_time = 0

# Jumping related variables
is_jumping = False
jump_start_time = None
jump_duration = 0.7
jump_height = 200
is_forced_landing = False

# Moving related variables
is_moving = False
move_start_time = None
move_duration = 0.2
move_target_x = None

# Sliding related variables
is_sliding = False
slide_start_time = None
slide_duration = 0.5
slide_rotation_angle = 0
max_slide_rotation = 90
sliding_speed = 5

# Barrier related variables
barrier_speed = 0.0  # Will be set to train_manager.base_speed
barriers = []

# Train manager instance
train_manager = None

def init_game():
    """Initialize game, train manager, and barriers"""
    global train_manager, barriers, barrier_speed
    train_manager = TrainManager(base_speed=700.0)  # Adjusted base speed
    barrier_speed = train_manager.base_speed
    
    # Initialize barriers with greater spacing to prevent initial collisions
    barrier_spacing = 3000  # Increased from 2000 to 3000
    barrier_positions = []
    
    # Start barriers at varying positions to avoid clustering
    for i in range(3):  # Create 3 initial barriers
        y_pos = -1800 - (i * barrier_spacing)
        lane = random.randint(0, 2)
        barrier_type = random.choice([1, 2])
        barrier_positions.append((y_pos, lane, barrier_type))
    
    barriers = barrier_positions
    print("Game, train manager, and barriers initialized successfully")

def draw_shapes():
    global GRID_WIDTH, player_pos, is_sliding, slide_rotation_angle
    # Draw moving barriers
    for y_pos, lane_index, barrier_type in barriers:
        if barrier_type == 1:
            drawbarrier1((0, y_pos, 0), GRID_WIDTH, lane_index)
        else:
            drawbarrier2((0, y_pos, 0), GRID_WIDTH, lane_index)
    drawPlayer(player_pos, is_sliding, slide_rotation_angle)
    if train_manager:
        train_manager.draw()

def updateDeltaTime():
    global last_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

def keyboardListener(key, x, y):
    global is_jumping, jump_start_time, is_moving, move_start_time, move_target_x, player_track, is_sliding, slide_start_time, slide_rotation_angle, is_forced_landing, barrier_speed
    # Move left (A key)
    if key == b'a' and not is_moving and player_track > 0:
        print("Pressed A: Moving left")
        player_track -= 1
        is_moving = True
        move_start_time = time.time()
        move_target_x = (player_track - 1) * 400  # -400, 0, 400
    # Move right (D key)
    if key == b'd' and not is_moving and player_track < 2:
        print("Pressed D: Moving right")
        player_track += 1
        is_moving = True
        move_start_time = time.time()
        move_target_x = (player_track - 1) * 400
    # Jump (W key)
    if key == b'w' and not is_jumping:
        print("Pressed W: Jumping")
        is_jumping = True
        jump_start_time = time.time()
        if is_sliding:
            is_sliding = False
            slide_rotation_angle = 0
    # Slide (S key)
    if key == b's' and not is_sliding:
        print("Pressed S: Sliding or landing")
        if is_jumping:
            is_forced_landing = True
        else:
            is_sliding = True
            slide_start_time = time.time()
    # Speed control keys
    if key == b'+' or key == b'=':
        if train_manager:
            train_manager.set_speed(train_manager.base_speed + 1.0)
            barrier_speed = train_manager.base_speed
            print(f"Train speed increased to {train_manager.base_speed:.1f}")
    if key == b'-':
        if train_manager and train_manager.base_speed > 1.0:
            train_manager.set_speed(train_manager.base_speed - 1.0)
            barrier_speed = train_manager.base_speed
            print(f"Train speed decreased to {train_manager.base_speed:.1f}")

def updatePlayerMovement():
    global player_pos, is_moving, move_start_time, move_target_x
    if not is_moving:
        return
    elapsed_time = time.time() - move_start_time
    if elapsed_time >= move_duration:
        x, y, z = player_pos
        player_pos = (move_target_x, y, z)
        is_moving = False
    else:
        t = elapsed_time / move_duration
        start_x = player_pos[0]
        x = start_x + t * (move_target_x - start_x)
        player_pos = (x, player_pos[1], player_pos[2])

def updatePlayerJump():
    global player_pos, is_jumping, jump_start_time, is_forced_landing, jump_duration, jump_height
    if not is_jumping:
        return
    elapsed_time = time.time() - jump_start_time
    if elapsed_time >= jump_duration or is_forced_landing:
        x, y, z = player_pos
        descent_time = elapsed_time / jump_duration if is_forced_landing else 0
        player_pos = (x, y, z * (1 - descent_time))
        if z <= 0.1:
            player_pos = (x, y, 0)
            is_jumping = False
            is_forced_landing = False
    else:
        t = elapsed_time / jump_duration
        height = jump_height * (1 - (2 * t - 1) ** 2)
        x, y, z = player_pos
        player_pos = (x, y, height)

def updatePlayerSlide():
    global is_sliding, slide_start_time, slide_rotation_angle, sliding_speed
    if not is_sliding:
        return
    elapsed_time = time.time() - slide_start_time
    if elapsed_time >= slide_duration:
        is_sliding = False
        slide_rotation_angle = 0
    else:
        t = elapsed_time / slide_duration
        new_slide_rotation_angle = t * max_slide_rotation * sliding_speed
        slide_rotation_angle = min(new_slide_rotation_angle, max_slide_rotation)

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if key == GLUT_KEY_UP:
        z += 50
    if key == GLUT_KEY_DOWN:
        z -= 50
    if key == GLUT_KEY_LEFT:
        angle = -10
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
    if key == GLUT_KEY_RIGHT:
        angle = 10
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    pass

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.5, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = camera_pos
    look_at_x, look_at_y, look_at_z = look_at
    gluLookAt(x, y, z, look_at_x, look_at_y, look_at_z, 0, 0, 1)

def check_barrier_collision(barrier_y, barrier_lane):
    """
    Check if a barrier would collide with any train carriage
    Returns True if there would be a collision
    """
    if not train_manager:
        return False
    
    # Get all occupied positions from the train manager
    occupied_positions = train_manager.get_occupied_positions()
    
    safety_buffer = 800  # Increased from 500 to 800
    
    for lane, front_pos, back_pos in occupied_positions:
        if lane == barrier_lane:
            # Check if barrier is within the safety buffer of any train carriage
            # Using absolute distance calculation to handle both directions
            if abs(barrier_y - front_pos) < safety_buffer or abs(barrier_y - back_pos) < safety_buffer:
                return True
    return False

def idle():
    updateDeltaTime()
    if train_manager:
        train_manager.update(delta_time)
    updatePlayerMovement()
    updatePlayerJump()
    updatePlayerSlide()
    
    # Update barrier positions
    for i in range(len(barriers)):
        y, lane, barrier_type = barriers[i]
        y += barrier_speed * delta_time
        
        # Reset barrier if it's past the view
        if y > GRID_LENGTH:
            # Place barrier well behind the viewing area
            y = -GRID_LENGTH - random.randint(500, 1500)
            
            # Try to find a lane where there's no train with increased safety buffer
            max_attempts = 20  # Increased attempts to find safe lane
            attempts = 0
            new_lane = random.randint(0, 2)
            
            # Try multiple times to find a lane without a collision
            while attempts < max_attempts and check_barrier_collision(y, new_lane):
                new_lane = random.randint(0, 2)
                attempts += 1
                
                # If we've tried many times and still can't find a safe position,
                # move the barrier further back to avoid any trains
                if attempts % 5 == 0:
                    y -= 1000  # Push barrier further back
                
            lane = new_lane
            barrier_type = random.choice([1, 2])
        
        barriers[i] = (y, lane, barrier_type)
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 600, 900)
    setupCamera()
    # Draw the road with 3 lanes
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)
    glVertex3f(-GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_WIDTH, -GRID_LENGTH, 0)
    glEnd()
    # Lane dividers (white lines)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    lane_width = GRID_WIDTH / 3
    for i in range(-1, 2):
        if i != 0:
            x = i * lane_width * 2
            glVertex3f(x - 5, GRID_LENGTH, 0.1)
            glVertex3f(x + 5, GRID_LENGTH, 0.1)
            glVertex3f(x + 5, -GRID_LENGTH, 0.1)
            glVertex3f(x - 5, -GRID_LENGTH, 0.1)
    glEnd()
    if train_manager:
        draw_text(10, 770, f"Train Speed: {train_manager.base_speed:.1f}")
        draw_text(10, 740, f"Use + and - keys to adjust train speed")
    draw_shapes()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 900)
    glutInitWindowPosition(100, 20)
    wind = glutCreateWindow(b"3D OpenGL Train Game")
    init_game()
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()