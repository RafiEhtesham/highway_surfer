from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
    Draws a leftward-facing restart button at the leftmost end of the white UI bar.
    """
    # Arrow position and dimensions
    center_x = -0.9  # Shifted slightly to the right
    center_y = 0.95   # Vertically aligned with the white bar
    shaft_length = 0.05  # Length of the horizontal shaft
    tip_size = 0.03      # Size of the arrow tip

    glColor3f(1, 0, 0)  # Set color to red

    print(f"Drawing restart button at center: ({center_x}, {center_y})")  # Debug: Print arrow center

    # Draw the horizontal shaft of the arrow
    midpoint_line(center_x + shaft_length, center_y, center_x - shaft_length, center_y)

    # Draw the upper tip of the arrow
    midpoint_line(center_x - shaft_length, center_y, center_x - shaft_length + tip_size, center_y + tip_size)

    # Draw the lower tip of the arrow
    midpoint_line(center_x - shaft_length, center_y, center_x - shaft_length + tip_size, center_y - tip_size)

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