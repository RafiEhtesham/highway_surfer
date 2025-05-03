from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from models.player import drawPlayer
from models.barriercopy import drawbarrier1, drawbarrier2
from models.text import draw_text
from math import cos, sin, radians
import time
from models.traincopy import TrainManager
import random

# Camera-related variables
camera_pos = (0, 350, 250)
look_at = (0, 150, 0)

player_pos = [0, 0, 0]  # [x, y, z]
player_track = 1  # 0=left, 1=center, 2=right

fovY = 90
GRID_LENGTH = 1800
GRID_WIDTH = 600

last_time = time.time()
delta_time = 0

# Jumping related variables
is_jumping = False
jump_start_time = 0
jump_duration = 0.7
jump_height = 200
is_forced_landing = False

# Moving related variables
is_moving = False
move_start_time = 0
move_duration = 0.2
move_target_x = 0

# Sliding related variables
is_sliding = False
slide_start_time = 0
slide_duration = 0.5
slide_rotation_angle = 0
max_slide_rotation = 90
sliding_speed = 5

# Barrier related variables
barrier_speed = 0.0
barriers = []

# Train manager instance
train_manager = None

# Game state variables
game_over = False
game_over_time = 0
game_over_message = ""
restart_cooldown = 2.0

def init_game():
    """Initialize game, train manager, and barriers"""
    global train_manager, barriers, barrier_speed, game_over, game_over_time, game_over_message, player_pos, player_track
    game_over = False
    game_over_time = 0
    game_over_message = ""
    player_pos = [0, 0, 0]
    player_track = 1
    train_manager = TrainManager(base_speed=700.0)
    barrier_speed = train_manager.base_speed
    barriers.clear()
    barrier_spacing = 3000
    for i in range(3):
        y_pos = -1800 - (i * barrier_spacing)
        lane = random.randint(0, 2)
        barrier_type = random.choice([1, 2])
        barriers.append([y_pos, lane, barrier_type])
    print("Game initialized")

def draw_shapes():
    """Draw barriers, player, and trains"""
    for y_pos, lane_index, barrier_type in barriers:
        if barrier_type == 1:
            drawbarrier1((0, y_pos, 0), GRID_WIDTH, lane_index)
        else:
            drawbarrier2((0, y_pos, 0), GRID_WIDTH, lane_index)
    drawPlayer(player_pos, is_sliding, slide_rotation_angle)
    if train_manager:
        train_manager.draw()

def updateDeltaTime():
    """Update delta time for frame timing"""
    global last_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

def keyboardListener(key, x, y):
    """Handle keyboard input"""
    global is_jumping, jump_start_time, is_moving, move_start_time, move_target_x, player_track, is_sliding, slide_start_time, slide_rotation_angle, is_forced_landing, barrier_speed
    if game_over:
        if key == b' ' and time.time() - game_over_time > restart_cooldown:
            init_game()
        return
    if key == b'a' and not is_moving and player_track > 0:
        player_track -= 1
        is_moving = True
        move_start_time = time.time()
        move_target_x = (player_track - 1) * 400
    elif key == b'd' and not is_moving and player_track < 2:
        player_track += 1
        is_moving = True
        move_start_time = time.time()
        move_target_x = (player_track - 1) * 400
    elif key == b'w' and not is_jumping:
        is_jumping = True
        jump_start_time = time.time()
        if is_sliding:
            is_sliding = False
            slide_rotation_angle = 0
    elif key == b's' and not is_sliding:
        if is_jumping:
            is_forced_landing = True
        else:
            is_sliding = True
            slide_start_time = time.time()
    elif key == b'+' or key == b'=':
        if train_manager:
            train_manager.set_speed(train_manager.base_speed + 1.0)
            barrier_speed = train_manager.base_speed
    elif key == b'-' and train_manager and train_manager.base_speed > 1.0:
        train_manager.set_speed(train_manager.base_speed - 1.0)
        barrier_speed = train_manager.base_speed

def updatePlayerMovement():
    """Update player horizontal movement"""
    global player_pos, is_moving, move_start_time, move_target_x
    if not is_moving or game_over:
        return
    elapsed = time.time() - move_start_time
    if elapsed >= move_duration:
        player_pos[0] = move_target_x
        is_moving = False
    else:
        t = elapsed / move_duration
        player_pos[0] = player_pos[0] + t * (move_target_x - player_pos[0])

def updatePlayerJump():
    """Update player jumping mechanics"""
    global player_pos, is_jumping, jump_start_time, is_forced_landing
    if not is_jumping or game_over:
        return
    elapsed = time.time() - jump_start_time
    if elapsed >= jump_duration or is_forced_landing:
        t = elapsed / jump_duration if is_forced_landing else 0
        player_pos[2] *= (1 - t)
        if player_pos[2] <= 0.1:
            player_pos[2] = 0
            is_jumping = False
            is_forced_landing = False
    else:
        t = elapsed / jump_duration
        player_pos[2] = jump_height * (1 - (2 * t - 1) ** 2)

def updatePlayerSlide():
    """Update player sliding mechanics"""
    global is_sliding, slide_start_time, slide_rotation_angle
    if not is_sliding or game_over:
        return
    elapsed = time.time() - slide_start_time
    if elapsed >= slide_duration:
        is_sliding = False
        slide_rotation_angle = 0
    else:
        t = elapsed / slide_duration
        slide_rotation_angle = min(t * max_slide_rotation * sliding_speed, max_slide_rotation)

def specialKeyListener(key, x, y):
    """Handle special key input for camera movement"""
    global camera_pos
    if game_over:
        return
    x, y, z = camera_pos
    if key == GLUT_KEY_UP:
        z += 50
    elif key == GLUT_KEY_DOWN:
        z -= 50
    elif key == GLUT_KEY_LEFT:
        angle = -10
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
    elif key == GLUT_KEY_RIGHT:
        angle = 10
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
    camera_pos = (x, y, z)

def setupCamera():
    """Set up the camera perspective"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.5, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*camera_pos, *look_at, 0, 0, 1)

def check_barrier_collision(barrier_y, barrier_lane):
    """Check if barrier would collide with train carriages"""
    if not train_manager:
        return False
    occupied_positions = train_manager.get_occupied_positions()
    safety_buffer = 800
    for lane, front_pos, back_pos in occupied_positions:
        if lane == barrier_lane and (abs(barrier_y - front_pos) < safety_buffer or abs(barrier_y - back_pos) < safety_buffer):
            return True
    return False

def check_player_collision():
    """Check for tight collisions with trains and barriers"""
    if game_over:
        return False, ""
    
    # Player hitbox (tight, based on player.py dimensions)
    player_x, player_y, player_z = player_pos
    player_half_width = 35  # Based on bike width and biker arms
    player_half_length = 100  # Bike body length
    player_height = 115 if is_sliding else 215  # Head height when not sliding, lower when sliding
    
    # Convert player lane to x-coordinate
    player_lane_x = (player_track - 1) * 400

    # Check collisions with trains
    if train_manager:
        for train in train_manager.trains:
            if train.lane == player_track:  # Changed from track_position to lane
                train_x = (train.lane - 1) * 400
                # Simplified collision check using lane alignment
                if (abs(player_x - train_x) < 100 and
                    abs(player_y - train.position) < 500 and
                    player_z < 200):
                    return True, "You were hit by a train!"
    
    # Check collisions with barriers
    for barrier_y, barrier_lane, barrier_type in barriers:
        if barrier_lane != player_track:
            continue
        # Barrier hitbox (tight, based on barriercopy.py)
        barrier_x = (barrier_lane - 1) * 400
        barrier_half_width = (GRID_WIDTH / 3) - 10  # Lane width minus stand offset
        barrier_half_length = 25  # Approximate barrier thickness
        barrier_height = 250 if barrier_type == 1 else 80  # Type 1: tall, Type 2: low
        
        # Check x, y, and z overlap
        if (abs(player_x - barrier_x) < player_half_width + barrier_half_width and
            abs(player_y - barrier_y) < player_half_length + barrier_half_length):
            if barrier_type == 1 and not is_sliding:  # Must slide under tall barrier
                return True, "Crashed into high barrier! Slide (S) to avoid."
            elif barrier_type == 2 and player_z < barrier_height:  # Must jump over low barrier
                return True, "Crashed into low barrier! Jump (W) to avoid."
    
    return False, ""

def idle():
    """Main game loop"""
    global game_over, game_over_time, game_over_message
    updateDeltaTime()
    if not game_over:
        collision, message = check_player_collision()
        if collision:
            game_over = True
            game_over_time = time.time()
            game_over_message = message
        else:
            train_manager.update(delta_time)
            updatePlayerMovement()
            updatePlayerJump()
            updatePlayerSlide()
            for i in range(len(barriers)):
                y, lane, barrier_type = barriers[i]
                y += barrier_speed * delta_time
                if y > GRID_LENGTH:
                    y = -GRID_LENGTH - random.randint(500, 1500)
                    max_attempts = 20
                    attempts = 0
                    new_lane = random.randint(0, 2)
                    while attempts < max_attempts and check_barrier_collision(y, new_lane):
                        new_lane = random.randint(0, 2)
                        attempts += 1
                        if attempts % 5 == 0:
                            y -= 1000
                    lane = new_lane
                    barrier_type = random.choice([1, 2])
                barriers[i] = [y, lane, barrier_type]
    glutPostRedisplay()

def showScreen():
    """Render the game scene"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 600, 900)
    setupCamera()
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)
    glVertex3f(-GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_WIDTH, -GRID_LENGTH, 0)
    glEnd()
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
    if game_over:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(600, 0)
        glVertex2f(600, 900)
        glVertex2f(0, 900)
        glEnd()
        glDisable(GL_BLEND)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 600, 0, 900, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        draw_text(180, 500, "GAME OVER")
        draw_text(150, 450, game_over_message)
        if time.time() - game_over_time > restart_cooldown:
            draw_text(120, 350, "Press SPACE to restart")
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
    glutSwapBuffers()

def main():
    """Initialize and run the game"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 900)
    glutInitWindowPosition(100, 20)
    glutCreateWindow(b"3D OpenGL Train Game")
    init_game()
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()