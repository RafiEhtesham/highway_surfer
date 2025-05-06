from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
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
    glPopMatrix()  # Restore the previous matrix state

def drawbarrier1(barrier_pos, g_width):

    x, y, z = barrier_pos

    # Adjust the x position based on the lane index

    glPushMatrix()  # Save the current matrix state
    glTranslatef(x, y, z)  # Move to the adjusted position

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

    glPopMatrix()  # Restore the previous matrix state

def drawbarrier2(barrier_pos, g_width):
    """
    Draws a barrier at the same level as the player's ground level.
    """
    x, y, z = barrier_pos

    # Set the barrier's z position to the player's ground level
    z = 0

    glPushMatrix()  # Save the current matrix state
    glTranslatef(x, y, z)  # Move to the adjusted position

    lane_width = g_width / 3
    stand_x_pos = lane_width - 10
    stand_height = 200

    cuboid_height = 50  # height of horizontal cuboid
    cuboid_z_pos = 0  # Align the top of the cuboid with the ground level

    # Diagonal red-white striped cuboid
    extended_height_scale = 3
    cube_size = 50
    half_extended = (cube_size * extended_height_scale) / 2

    cuboid_half_length = (stand_x_pos - 5)
    z_pos = 30

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
        glScalef(stripe_width / cube_size, stripe_thickness, 1)
        glutSolidCube(cube_size)
        glPopMatrix()

    glPopMatrix()  # Restore the previous matrix state

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

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

    # Draw train cars (blue compartments) first
    for i in range(num_cars):
        glPushMatrix()
        glColor3f(0.1, 0.1, 0.8)  # Blue color for the cars
        glTranslatef(-200 * (i + 1), 0, 0)  # Position each car behind the locomotive
        glScalef(2, 1, 1)  # Scale to make it rectangular
        glutSolidCube(100)  # Train car body
        glPopMatrix()

    # Draw locomotive (red compartment) after the blue compartments
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

    glPopMatrix()

def drawTrainObstacle(train_pos, num_cars=1):
    """
    Wrapper function to draw a train obstacle.
    :param train_pos: Tuple (x, y, z) specifying the position of the train.
    :param num_cars: Number of cars to attach to the locomotive.
    """
    drawTrain(train_pos, num_cars)

def midpoint_line(x1, y1, x2, y2):
    """
    Draws a line using the midpoint line algorithm.
    """
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    dne = 2 * (dy - dx)
    de = 2 * dy

    x, y = x1, y1

    glPointSize(3.0)  # Increase point size to make the arrow thicker
    glBegin(GL_POINTS)  # Use GL_POINTS for rendering
    while x <= x2:
        orig_x, orig_y = convert_to_original_zone(x, y, zone)
        glVertex2f(orig_x, orig_y)  # Use OpenGL to draw points

        if d > 0:
            y += 0.001  # Use smaller fractional steps for smoother rendering
            d += dne
        else:
            d += de
        x += 0.001  # Use smaller fractional steps for smoother rendering
    glEnd()  # End OpenGL rendering

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx >= 0 and dy >= 0:
        if abs(dy) > abs(dx):
            return 1
        else:
            return 0
    elif dx < 0 and dy >= 0:
        if abs(dy) > abs(dx):
            return 2
        else:
            return 3
    elif dx < 0 and dy < 0:
        if abs(dy) > abs(dx):
            return 5
        else:
            return 4
    elif dx >= 0 and dy < 0:
        if abs(dy) > abs(dx):
            return 6
        else:
            return 7
    return -1  # Invalid zone

def convert_to_zone0(x, y, zone):
    if zone == 1:
        x, y = y, x
    elif zone == 2:
        x, y = y, -x
    elif zone == 3:
        x = -x
    elif zone == 4:
        x, y = -x, -y
    elif zone == 5:
        x, y = -y, -x
    elif zone == 6:
        x, y = -y, x
    elif zone == 7:
        y = -y
    return x, y

def convert_to_original_zone(x, y, zone):
    if zone == 1:
        x, y = y, x
    elif zone == 2:
        x, y = -y, x
    elif zone == 3:
        x = -x
    elif zone == 4:
        x, y = -x, -y
    elif zone == 5:
        x, y = -y, -x
    elif zone == 6:
        x, y = y, -x
    elif zone == 7:
        y = -y
    return x, y

def draw_restart_arrow():
    """
    Draws a rightward-facing restart button at the rightmost end of the white UI bar.
    """
    # Arrow position and dimensions
    center_x = 0.9  # Positioned at the rightmost end
    center_y = 0.95  # Vertically aligned with the white bar
    shaft_length = 0.05  # Length of the horizontal shaft
    tip_size = 0.03  # Size of the arrow tip

    glColor3f(1, 0, 0)  # Set color to red

    # Draw the horizontal shaft of the arrow
    midpoint_line(center_x - shaft_length, center_y, center_x + shaft_length, center_y)

    # Draw the upper tip of the arrow
    midpoint_line(center_x + shaft_length, center_y, center_x + shaft_length - tip_size, center_y + tip_size)

    # Draw the lower tip of the arrow
    midpoint_line(center_x + shaft_length, center_y, center_x + shaft_length - tip_size, center_y - tip_size)

def draw_pause_button():
    """
    Draws a pause button at the center of the white UI bar.
    """
    center_x = 0  # Center of the screen horizontally
    center_y = 0.95  # Vertically aligned with the white bar
    bar_height = 0.03  # Height of each vertical bar
    bar_spacing = 0.02  # Spacing between the two bars

    glColor3f(0, 0, 1)  # Set color to blue

    # Draw the left vertical bar
    midpoint_line(center_x - bar_spacing, center_y + bar_height, center_x - bar_spacing, center_y - bar_height)

    # Draw the right vertical bar
    midpoint_line(center_x + bar_spacing, center_y + bar_height, center_x + bar_spacing, center_y - bar_height)

def draw_play_button():
    """
    Draws a play button (triangle) at the center of the white UI bar.
    """
    center_x = 0  # Center of the screen horizontally
    center_y = 0.95  # Vertically aligned with the white bar
    triangle_width = 0.06  # Increased width of the triangle
    triangle_height = 0.07  # Increased height of the triangle

    glColor3f(0, 1, 0)  # Set color to green

    # Define the three vertices of the triangle
    left_vertex = (center_x - triangle_width / 2, center_y - triangle_height / 2)
    right_vertex = (center_x + triangle_width / 2, center_y)
    top_vertex = (center_x - triangle_width / 2, center_y + triangle_height / 2)

    # Draw the three edges of the triangle
    midpoint_line(left_vertex[0], left_vertex[1], right_vertex[0], right_vertex[1])
    midpoint_line(right_vertex[0], right_vertex[1], top_vertex[0], top_vertex[1])
    midpoint_line(top_vertex[0], top_vertex[1], left_vertex[0], left_vertex[1])

def draw_ui(is_paused):
    """
    Draws the UI, including the white bar, the restart button, and the pause/play button.
    """
    glPushMatrix()  # Save the current matrix state
    glColor3f(1, 1, 1)  # Set color to white
    glBegin(GL_QUADS)  # Start drawing a rectangle
    glVertex2f(-1.0, 0.9)  # Top-left corner
    glVertex2f(1.0, 0.9)   # Top-right corner
    glVertex2f(1.0, 1.0)   # Bottom-right corner
    glVertex2f(-1.0, 1.0)  # Bottom-left corner
    glEnd()  # End drawing

    # Draw the restart arrow
    draw_restart_arrow()

    # Draw the pause or play button based on the is_paused flag
    if is_paused:
        draw_play_button()
    else:
        draw_pause_button()

    glPopMatrix()  # Restore the previous matrix state

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

