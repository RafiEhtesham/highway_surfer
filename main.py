from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from models.player import drawPlayer
from models.barrier import drawbarrier1, drawbarrier2
from models.text import draw_text
from models.trains import drawTrainObstacle
from math import cos, sin, radians
from models.ui import draw_ui
import time
import random

game_started = False
show_start_menu = True

# Camera-related variables
camera_pos = (0, 350, 250)
look_at = (0, 0, 0)

player_pos = (0, 0, 0)

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

# Add a global flag to track whether the game is paused
is_paused = False
# Sliding related variables
is_sliding = False
slide_start_time = None
slide_duration = 0.7
slide_rotation_angle = 0
max_slide_rotation = 90
sliding_speed = 5

# Game-related variables

obstacles = []
obstacle_speed = 400
obstacle_spawn_interval = 1
last_obstacle_spawn_time = time.time()
score = 0
high_score = 0
game_over = False
game_speed = 1.0

# First-person mode variables
is_first_person = False
default_camera_pos = camera_pos
default_look_at = look_at

rail_tracks = []

# Add a global variable to control rail track speed
rail_speed_multiplier = 2

# Boost-related variables
is_boosting = False
boost_start_time = None
boost_duration = 2.0
boost_multiplier = 2.0
original_obstacle_spawn_interval = obstacle_spawn_interval

def draw_shapes():

    global GRID_WIDTH, player_pos, is_sliding, slide_rotation_angle   

    drawPlayer(player_pos, is_sliding, slide_rotation_angle)

def drawStartMenu():
    """
    Draws the start menu screen with instructions.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 600, 0, 900, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glBegin(GL_QUADS)
    glColor3f(0.15, 0.15, 0.15)
    glVertex2f(0, 0)
    glVertex2f(600, 0)
    glVertex2f(600, 900)
    glVertex2f(0, 900)
    glEnd()
    
    
    draw_text(370, 600, "HIGHWAY SURFER")
    draw_text(360, 550, "Press SPACE to start")
    draw_text(300, 400, "Use A/D keys to move left/right")
    draw_text(387, 350, "Press W to jump")
    draw_text(387, 300, "Press S to slide")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def spawnObstacle():
    """
    Spawns a new obstacle at a random lane and randomly selects its type.
    """
    global obstacles
    lane_index = random.choice([-1, 0, 1])
    obstacle_type = random.choice(["barrier1", "barrier2", "train"])
    obstacle_pos = (lane_index * GRID_WIDTH / 1.5, -GRID_LENGTH, 0)
    obstacles.append((obstacle_pos, obstacle_type))

def updateObstacles():
    """
    Updates the positions of obstacles and removes those that go off-screen.
    """
    global obstacles, score, game_over, game_speed, obstacle_spawn_interval, is_paused

    if is_paused:
        return

    if score > 100:
        game_speed = 1.5
        obstacle_spawn_interval = 0.9
    if score > 300:
        game_speed = 2
        obstacle_spawn_interval = 0.8
    if score > 500:
        game_speed = 3
        obstacle_spawn_interval = 0.7

    new_obstacles = []
    for obstacle, obstacle_type in obstacles:
        x, y, z = obstacle
        speed = obstacle_speed
        if obstacle_type == "train":
            speed *= 2.5
        y += speed * delta_time * game_speed
        if y > player_pos[1] and y < GRID_LENGTH:
            score += 0.005

        if y < GRID_LENGTH:
            new_obstacles.append(((x, y, z), obstacle_type))

    obstacles = new_obstacles

    for obstacle, obstacle_type in obstacles:
        if obstacle_type == "barrier1" and not is_sliding:
            if abs(obstacle[0] - player_pos[0]) < GRID_WIDTH / 6 and abs(obstacle[1] - player_pos[1]) < 50:
                game_over = True
                print(f"[DEBUG] Collision with barrier1! Game Over. Final Score: {score}") 
        
        elif obstacle_type == "barrier2" and not is_jumping:
            if abs(obstacle[0] - player_pos[0]) < GRID_WIDTH / 6 and abs(obstacle[1] - player_pos[1]) < 50:
                game_over = True
                print(f"[DEBUG] Collision with barrier2! Game Over. Final Score: {score}")

        elif obstacle_type == "train":
            if abs(obstacle[0] - player_pos[0]) < GRID_WIDTH / 6 and abs(obstacle[1] - player_pos[1]) < 300:    
                game_over = True
                print(f"[DEBUG] Collision with train! Game Over. Final Score: {score}")

def drawObstacles():
    """
    Draws all active obstacles on the screen.
    """
    for obstacle, obstacle_type in obstacles:
        if obstacle_type == "train":
            drawTrainObstacle(obstacle)
        elif obstacle_type == "barrier1":
            drawbarrier1(obstacle, GRID_WIDTH)
        elif obstacle_type == "barrier2":
            drawbarrier2(obstacle, GRID_WIDTH)
        
def resetGame():
    """
    Resets the game state after a game over.
    """
    global player_pos, obstacles, score, game_over, high_score
    if score > high_score:
        high_score = int(score)
        print(f"[DEBUG] New high score: {high_score}")

    player_pos = (0, 0, 0)
    obstacles = []
    score = 0
    game_over = False
    print("[DEBUG] Game reset.")

def updateDeltaTime():
    """
    Updates the delta time based on the current and last frame times.
    """
    global last_time, delta_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

def updateBoost():
    """
    Updates the game speed during a boost and reverts it after the boost duration.
    """
    global is_boosting, boost_start_time, game_speed, obstacle_spawn_interval

    if not is_boosting:
        return

    elapsed_time = time.time() - boost_start_time
    if elapsed_time >= boost_duration:
        is_boosting = False
        game_speed /= boost_multiplier
        obstacle_spawn_interval = original_obstacle_spawn_interval
        print(f"[DEBUG] Boost ended. game_speed: {game_speed}, obstacle_spawn_interval: {obstacle_spawn_interval}")
    else:
        print(f"[DEBUG] Boost active. elapsed_time: {elapsed_time}")

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global is_jumping, jump_start_time, is_moving, move_start_time, move_target_x, is_sliding, slide_start_time
    global slide_rotation_angle, is_forced_landing, game_over, is_first_person, camera_pos, look_at
    global game_started, show_start_menu, is_boosting, boost_start_time, game_speed, obstacle_spawn_interval
    
    if show_start_menu and key == b' ':
        show_start_menu = False
        game_started = True
        print("[DEBUG] Game started from menu.")
        return
        
    if not game_started:
        return

    if game_over and key == b'r':
        resetGame()
        return

    print(f"[DEBUG] Key pressed: {key}")

    if key == b'v':
        is_first_person = not is_first_person
        if is_first_person:
            camera_pos = (player_pos[0], player_pos[1] + 50, player_pos[2] + 200)
            look_at = (player_pos[0], -(player_pos[1] + 1000), player_pos[2])
            print(f"[DEBUG] First-person mode activated. camera_pos: {camera_pos}, look_at: {look_at}")
        else:
            camera_pos = default_camera_pos
            look_at = default_look_at
            print(f"[DEBUG] First-person mode deactivated. camera_pos: {camera_pos}, look_at: {look_at}")

    if key == b'a' and not is_moving and not is_paused:
        x, y, z = player_pos
        target_x = x + 400
        if abs(target_x) < GRID_WIDTH:
            is_moving = True
            move_start_time = time.time()
            move_target_x = target_x
            print(f"[DEBUG] Moving left. target_x: {target_x}, player_pos: {player_pos}")

    if key == b'd' and not is_moving and not is_paused:
        x, y, z = player_pos
        target_x = x - 400
        if abs(target_x) < GRID_WIDTH:
            is_moving = True
            move_start_time = time.time()
            move_target_x = target_x
            print(f"[DEBUG] Moving right. target_x: {target_x}, player_pos: {player_pos}")

    if key == b'w' and not is_jumping:
        is_jumping = True
        jump_start_time = time.time()
        print(f"[DEBUG] Jump initiated. jump_start_time: {jump_start_time}, player_pos: {player_pos}")
        if is_sliding:
            is_sliding = False
            slide_rotation_angle = 0
            print(f"[DEBUG] Slide ended due to jump.")

    if key == b's' and not is_sliding:
        if is_jumping:
            is_forced_landing = True
            print(f"[DEBUG] Forced landing triggered.")
        else:
            is_sliding = True
            slide_start_time = time.time()
            print(f"[DEBUG] Slide initiated. slide_start_time: {slide_start_time}")

    if key == b'q' and not is_boosting:  # Q key
        is_boosting = True
        boost_start_time = time.time()
        game_speed *= boost_multiplier
        obstacle_spawn_interval /= boost_multiplier
        print(f"[DEBUG] Boost activated. game_speed: {game_speed}, obstacle_spawn_interval: {obstacle_spawn_interval}")

def updatePlayerMovement():
    """
    Updates the player's position during left/right movement.
    """
    global player_pos, is_moving, move_start_time, move_target_x, camera_pos, look_at

    if not is_moving:
        return

    elapsed_time = time.time() - move_start_time
    print(f"[DEBUG] Movement elapsed_time: {elapsed_time}, move_duration: {move_duration}")
    if elapsed_time >= move_duration:
        x, y, z = player_pos
        player_pos = (move_target_x, y, z)
        is_moving = False
        if is_first_person:
            camera_pos = (player_pos[0], player_pos[1] + 50, player_pos[2] + 200)
            look_at = (player_pos[0], -(player_pos[1] + 1000), player_pos[2])
        print(f"[DEBUG] Movement ended. player_pos: {player_pos}")
    else:
        t = elapsed_time / move_duration
        start_x, y, z = player_pos
        x = start_x + t * (move_target_x - start_x)
        player_pos = (x, y, z)
        if is_first_person:
            camera_pos = (player_pos[0], player_pos[1] + 50, player_pos[2] + 200)
            look_at = (player_pos[0], -(player_pos[1] + 1000), player_pos[2])
        print(f"[DEBUG] Moving. player_pos: {player_pos}")

def updatePlayerJump():
    """
    Updates the player's position during a jump.
    """
    global player_pos, is_jumping, jump_start_time, is_forced_landing, camera_pos

    if not is_jumping:
        return

    elapsed_time = time.time() - jump_start_time
    print(f"[DEBUG] Jump elapsed_time: {elapsed_time}, jump_duration: {jump_duration}")
    if elapsed_time >= jump_duration or is_forced_landing:
        x, y, z = player_pos
        descent_time = elapsed_time / jump_duration if is_forced_landing else 0
        player_pos = (x, y, z * (1 - descent_time))
        print(f"[DEBUG] Jump landing. player_pos: {player_pos}, is_forced_landing: {is_forced_landing}")
        if z <= 10:
            player_pos = (x, y, 0)
            is_jumping = False
            is_forced_landing = False
        if is_first_person:
            camera_pos = (player_pos[0], player_pos[1] + 50, player_pos[2] + 200)
        print(f"[DEBUG] Jump ended. player_pos: {player_pos}")
    else:
        t = elapsed_time / jump_duration
        height = jump_height * (1 - (2 * t - 1) ** 2)
        x, y, z = player_pos
        player_pos = (x, y, height)
        if is_first_person:
            camera_pos = (player_pos[0], player_pos[1] + 50, player_pos[2] + 200)
        print(f"[DEBUG] Jumping. player_pos: {player_pos}")

def updatePlayerSlide():
    """
    Updates the player's state during a slide.
    """
    global is_sliding, slide_start_time, slide_rotation_angle, sliding_speed, camera_pos

    if not is_sliding:
        return

    elapsed_time = time.time() - slide_start_time
    print(f"[DEBUG] Slide elapsed_time: {elapsed_time}, slide_duration: {slide_duration}")
    if elapsed_time >= slide_duration:
        is_sliding = False
        slide_rotation_angle = 0
        if is_first_person:
            target_camera_z = player_pos[2] + 200
            current_camera_x, current_camera_y, current_camera_z = camera_pos
            camera_pos = (current_camera_x, current_camera_y, current_camera_z + (target_camera_z - current_camera_z) * 0.1)
        print(f"[DEBUG] Slide ended. slide_rotation_angle: {slide_rotation_angle}")
    else:
        t = elapsed_time / slide_duration
        new_slide_rotation_angle = t * max_slide_rotation * sliding_speed
        slide_rotation_angle = min(new_slide_rotation_angle, max_slide_rotation)
        if is_first_person:
            target_camera_z = player_pos[2] + 180
            current_camera_x, current_camera_y, current_camera_z = camera_pos
            camera_pos = (current_camera_x, current_camera_y, current_camera_z + (target_camera_z - current_camera_z) * 0.1)
        print(f"[DEBUG] Sliding. slide_rotation_angle: {slide_rotation_angle}")

def drawRailTrack(position):
    """
    Draws a rail track at the specified position.
    """
    x, y, z = position
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(x - GRID_WIDTH / 6, y + 10, z)
    glVertex3f(x + GRID_WIDTH / 6, y + 10, z)
    glVertex3f(x + GRID_WIDTH / 6, y - 10, z)
    glVertex3f(x - GRID_WIDTH / 6, y - 10, z)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(x - GRID_WIDTH / 12, y + 10, z + 1)
    glVertex3f(x - GRID_WIDTH / 12 + 5, y + 10, z + 1)
    glVertex3f(x - GRID_WIDTH / 12 + 5, y - 10, z + 1)
    glVertex3f(x - GRID_WIDTH / 12, y - 10, z + 1)

    glVertex3f(x + GRID_WIDTH / 12 - 5, y + 10, z + 1)
    glVertex3f(x + GRID_WIDTH / 12, y + 10, z + 1)
    glVertex3f(x + GRID_WIDTH / 12, y - 10, z + 1)
    glVertex3f(x + GRID_WIDTH / 12 - 5, y - 10, z + 1)
    glEnd()

def updateRailTracks():
    """
    Updates the positions of the rail tracks and resets them when they go off-screen.
    """
    global rail_tracks

    new_rail_tracks = []
    for track in rail_tracks:
        x, y, z = track
        y += obstacle_speed * delta_time * game_speed * rail_speed_multiplier
        if y < GRID_LENGTH:
            new_rail_tracks.append((x, y, z))
        else:
            new_rail_tracks.append((x, -GRID_LENGTH, z))

    rail_tracks = new_rail_tracks

def initializeRailTracks():
    """
    Initializes the rail tracks for each lane with increased frequency.
    """
    global rail_tracks
    rail_tracks = []
    for i in range(-GRID_LENGTH, GRID_LENGTH, 200):
        rail_tracks.extend([
            (-GRID_WIDTH / 1.5, i, 0),
            (0, i, 0),
            (GRID_WIDTH / 1.5, i, 0)
        ])

def drawRailTracks():
    """
    Draws all rail tracks on the screen.
    """
    for track in rail_tracks:
        drawRailTrack(track)

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos

    print(f"[DEBUG] Special key pressed: {key}")

    x, y, z = camera_pos
    if key == GLUT_KEY_UP:
        z += 50
        print(f"[DEBUG] Camera moved up. camera_pos: {camera_pos}")

    if key == GLUT_KEY_DOWN:
        z -= 50
        print(f"[DEBUG] Camera moved down. camera_pos: {camera_pos}")

    if key == GLUT_KEY_LEFT:
        angle = -10
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
        print(f"[DEBUG] Camera moved left. camera_pos: {camera_pos}")

    if key == GLUT_KEY_RIGHT:
        angle = 10
        new_x = x * cos(radians(angle)) - y * sin(radians(angle))
        new_y = x * sin(radians(angle)) + y * cos(radians(angle))
        x, y = new_x, new_y
        print(f"[DEBUG] Camera moved right. camera_pos: {camera_pos}")

    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for toggling pause/play and restarting the game.
    """
    global is_paused, game_over, player_pos, obstacles, score, game_speed, obstacle_spawn_interval, is_first_person, camera_pos, look_at

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_x = 1 - (x / 600) * 2
        mouse_y = -((y / 900) * 2 - 1)

        restart_center_x = -0.9
        restart_center_y = 0.95
        restart_width = 0.1
        restart_height = 0.1

        if (restart_center_x - restart_width / 2 <= mouse_x <= restart_center_x + restart_width / 2 and
                restart_center_y - restart_height / 2 <= mouse_y <= restart_center_y + restart_height / 2):
            player_pos = (0, 0, 0)
            obstacles = []
            score = 0
            game_speed = 1.0
            obstacle_spawn_interval = 1
            game_over = False
            is_paused = False

            if is_first_person:
                is_first_person = False
                camera_pos = default_camera_pos
                look_at = default_look_at
                print("[DEBUG] Switched back to third-person mode.")

            print("[DEBUG] Game restarted via restart button.")

        center_x = 0
        center_y = 0.95
        button_width = 0.06
        button_height = 0.07

        if (center_x - button_width / 2 <= mouse_x <= center_x + button_width / 2 and
                center_y - button_height / 2 <= mouse_y <= center_y + button_height / 2):
            is_paused = not is_paused
            print(f"Pause state toggled: {'Paused' if is_paused else 'Playing'}")

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.5, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    x, y, z = camera_pos
    look_at_x, look_at_y, look_at_z = look_at
    gluLookAt(x, y, z,
              look_at_x, look_at_y, look_at_z,
              0, 0, 1)
    
def idle():
    """
    Idle function that runs continuously:
    - Updates delta time for smooth movement.
    - Updates player position for smooth lane transitions, jumps, and slides.
    - Spawns and updates obstacles.
    - Triggers screen redraw for real-time updates.
    """
    global last_obstacle_spawn_time

    if show_start_menu:
        glutPostRedisplay()
        return

    updateDeltaTime()

    if game_over or is_paused:
        return

    
    updatePlayerMovement()
    updatePlayerJump()
    updatePlayerSlide()
    updateObstacles()
    updateRailTracks()
    updateBoost()

    if time.time() - last_obstacle_spawn_time > obstacle_spawn_interval:
        spawnObstacle()
        last_obstacle_spawn_time = time.time()

    glutPostRedisplay()

def showScreen():
    
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything on the screen.
    """
    global show_start_menu, game_over, score, high_score
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 600, 900)

    if show_start_menu:
        drawStartMenu()
        glutSwapBuffers()
        return

    setupCamera()

    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)
    glVertex3f(-GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, GRID_LENGTH, 0)
    glVertex3f(GRID_WIDTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_WIDTH, -GRID_LENGTH, 0)

    glColor3f(1, 1, 1)
    lane_width = GRID_WIDTH / 3
    for i in range(-1, 2):
        if i != 0:
            x = i * lane_width
            glVertex3f(x - 1, GRID_LENGTH, 0.1)
            glVertex3f(x + 1, GRID_LENGTH, 0.1)
            glVertex3f(x + 1, -GRID_LENGTH, 0.1)
            glVertex3f(x - 1, -GRID_LENGTH, 0.1)

    glEnd()

    if game_over:
        if score > high_score:
            high_score = int(score)
        draw_text(180, 700, f"GAME OVER! Your Score: {int(score)}. Press R to Restart")
        draw_text(180, 650, f"High Score: {high_score}")
    else:
        draw_text(10, 770, f"Score: {int(score)}")
        draw_text(10, 700, f"High Score: {high_score}")

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    draw_ui(is_paused)

    draw_text(10, 730, f"Score: {int(score)}")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    drawRailTracks()
    drawObstacles()
    draw_shapes()
    
    glutSwapBuffers()

def main():
    initializeRailTracks()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 900)
    glutInitWindowPosition(100, 20)
    wind = glutCreateWindow(b"3D OpenGL Intro")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()

