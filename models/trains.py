from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# Import grid constants
GRID_LENGTH = 1800  # Same as in main.py
GRID_WIDTH = 600    # Width of the grid

class TrainCarriage:
    def __init__(self, train_type, position_offset=0, color_variation=0):
        """
        Initialize a train carriage with specific attributes
        
        Args:
            train_type: 0=regular, 1=tunnel, 2=ramp
            position_offset: Position offset from the lead carriage
            color_variation: Slight color variation for multi-carriage trains
        """
        self.train_type = train_type
        self.position_offset = position_offset
        self.color_variation = color_variation
        
        # Dimensions based on type - adjusted to fit lanes (lane width = 400)
        self.width = 180  # Fits within lane
        self.length = 220
        self.height = 180
        
        if train_type == 0:  # Regular train
            self.base_color = (0.9, 0.3, 0.3)  # Bright red
        elif train_type == 1:  # Tunnel train
            self.base_color = (0.3, 0.3, 0.9)  # Bright blue
            self.height = 240  # Taller for tunnel
        else:  # Ramp train
            self.base_color = (0.3, 0.9, 0.3)  # Bright green
        
        # Apply color variation
        r, g, b = self.base_color
        variation = 0.1 * color_variation
        self.color = (
            max(0, min(1, r - variation)),
            max(0, min(1, g - variation)),
            max(0, min(1, b - variation))
        )
        
    def draw(self, x, y, z):
        """Draw the train carriage based on its type"""
        y = y + self.position_offset
        
        glPushMatrix()
        glTranslatef(x, y, z)
        
        if self.train_type == 0:
            self._draw_regular_carriage()
        elif self.train_type == 1:
            self._draw_tunnel_carriage()
        else:
            self._draw_ramp_carriage()
            
        glPopMatrix()
    
    def _draw_regular_carriage(self):
        """Draw a regular subway train carriage inspired by Subway Surfers"""
        r, g, b = self.color
        
        # Main body (sleek and rounded)
        glColor3f(r, g, b)
        self._draw_rounded_box(-self.width/2, 0, -self.length/2, 
                              self.width, self.height, self.length)
        
        # Windows (large, reflective)
        window_height = self.height * 0.5
        window_y = self.height * 0.55
        window_width = self.width * 0.85
        window_spacing = self.length / 3
        
        glColor3f(0.2, 0.4, 0.5)  # Reflective blue-gray for windows
        for i in range(2):
            window_z = -self.length/4 + window_spacing*i
            self._draw_box(-window_width/2, window_y, window_z,
                          window_width, window_height, window_spacing/2, depth=3)
        
        # Doors (double doors in the middle)
        door_width = self.width * 0.3
        door_height = self.height * 0.7
        door_y = self.height * 0.35
        
        glColor3f(r*0.7, g*0.7, b*0.7)  # Slightly darker than body
        self._draw_box(-door_width, door_y, -self.length/8,
                      door_width*2, door_height, self.length/4, depth=2)
        
        # Graffiti-style details
        glColor3f(0.9, 0.9, 0.1)  # Yellow graffiti
        graffiti_width = self.width * 0.4
        graffiti_height = self.height * 0.2
        self._draw_box(-graffiti_width/2, self.height*0.3, -self.length/3,
                      graffiti_width, graffiti_height, self.length/6, depth=1)
        
        # Headlights (front)
        glColor3f(1.0, 1.0, 0.8)  # Bright white-yellow
        headlight_size = 20
        glPushMatrix()
        glTranslatef(-self.width/4, self.height/4, -self.length/2 - 2)
        glutSolidSphere(headlight_size, 10, 10)
        glTranslatef(self.width/2, 0, 0)
        glutSolidSphere(headlight_size, 10, 10)
        glPopMatrix()
        
        # Roof details
        glColor3f(0.3, 0.3, 0.3)  # Dark gray
        roof_height = self.height * 0.1
        self._draw_box(-self.width/2 + 5, self.height, -self.length/2 + 5,
                      self.width - 10, roof_height, self.length - 10)
        
        # Undercarriage
        glColor3f(0.2, 0.2, 0.2)  # Dark gray
        rail_height = 15
        self._draw_box(-self.width/2, 0, -self.length/2,
                      self.width, rail_height, self.length)
        
        # Connectors
        glColor3f(0.4, 0.4, 0.4)  # Gray
        self._draw_box(-self.width/4, self.height/4, -self.length/2 - 10,
                      self.width/2, self.height/2, 10)
        self._draw_box(-self.width/4, self.height/4, self.length/2,
                      self.width/2, self.height/2, 10)
    
    def _draw_tunnel_carriage(self):
        """Draw a tunnel train carriage inspired by Subway Surfers"""
        r, g, b = self.color
        
        # Main body
        glColor3f(r, g, b)
        self._draw_rounded_box(-self.width/2, 0, -self.length/2, 
                              self.width, self.height, self.length)
        
        # Tunnel opening (large and circular)
        glColor3f(0.1, 0.1, 0.1)  # Dark interior
        tunnel_height = self.height * 0.8
        tunnel_width = self.width * 0.9
        
        glPushMatrix()
        glTranslatef(0, tunnel_height/2, -self.length/2 - 2)
        self._draw_tunnel_opening(tunnel_width, tunnel_height)
        glPopMatrix()
        
        # Side details
        glColor3f(r*0.7, g*0.7, b*0.7)  # Slightly darker
        stripe_height = self.height * 0.2
        self._draw_box(-self.width/2, self.height*0.4, -self.length/2,
                      self.width, stripe_height, self.length, depth=2)
        
        # Roof vent
        glColor3f(0.3, 0.3, 0.3)  # Dark gray
        vent_size = 30
        glPushMatrix()
        glTranslatef(0, self.height, 0)
        self._draw_box(-vent_size/2, 0, -vent_size/2,
                      vent_size, 10, vent_size)
        glPopMatrix()
        
        # Undercarriage
        glColor3f(0.2, 0.2, 0.2)  # Dark gray
        rail_height = 15
        self._draw_box(-self.width/2, 0, -self.length/2,
                      self.width, rail_height, self.length)
        
        # Back connector
        glColor3f(0.4, 0.4, 0.4)  # Gray
        self._draw_box(-self.width/4, self.height/4, self.length/2,
                      self.width/2, self.height/2, 10)
    
    def _draw_ramp_carriage(self):
        """Draw a ramp train carriage inspired by Subway Surfers"""
        r, g, b = self.color
        
        # Base part
        base_length = self.length * 0.5  # Adjusted for better proportion
        glColor3f(r, g, b)
        self._draw_rounded_box(-self.width/2, 0, -self.length/2, 
                              self.width, self.height * 0.8, base_length)
        
        # Ramp part
        ramp_length = self.length - base_length
        ramp_height = self.height * 0.8
        ramp_start_z = -self.length/2 + base_length
        
        # Main ramp surface
        glBegin(GL_QUADS)
        glColor3f(r*1.1, g*1.1, b*1.1)
        glVertex3f(-self.width/2, ramp_height, ramp_start_z)
        glVertex3f(self.width/2, ramp_height, ramp_start_z)
        glVertex3f(self.width/2, 0, self.length/2)
        glVertex3f(-self.width/2, 0, self.length/2)
        glEnd()
        
        # Sides
        glColor3f(r*0.9, g*0.9, b*0.9)
        glBegin(GL_TRIANGLES)
        # Left side
        glVertex3f(-self.width/2, 0, self.length/2)
        glVertex3f(-self.width/2, 0, ramp_start_z)
        glVertex3f(-self.width/2, ramp_height, ramp_start_z)
        # Right side
        glVertex3f(self.width/2, 0, self.length/2)
        glVertex3f(self.width/2, 0, ramp_start_z)
        glVertex3f(self.width/2, ramp_height, ramp_start_z)
        glEnd()
        
        # Safety stripes
        stripe_width = 25  # Increased for visibility
        stripe_count = 5
        stripe_spacing = ramp_length / stripe_count
        
        glBegin(GL_QUADS)
        for i in range(stripe_count):
            if i % 2 == 0:
                glColor3f(1.0, 0.0, 0.0)  # Red
            else:
                glColor3f(1.0, 1.0, 1.0)  # White
            stripe_z = ramp_start_z + i * stripe_spacing
            stripe_y_start = ramp_height - (i * stripe_spacing * ramp_height / ramp_length)
            stripe_y_end = ramp_height - ((i + 1) * stripe_spacing * ramp_height / ramp_length)
            
            glVertex3f(-self.width/2 + stripe_width, stripe_y_start, stripe_z)
            glVertex3f(-self.width/2 + stripe_width, stripe_y_end, stripe_z + stripe_spacing)
            glVertex3f(-self.width/2 + stripe_width*2, stripe_y_end, stripe_z + stripe_spacing)
            glVertex3f(-self.width/2 + stripe_width*2, stripe_y_start, stripe_z)
            
            glVertex3f(self.width/2 - stripe_width*2, stripe_y_start, stripe_z)
            glVertex3f(self.width/2 - stripe_width*2, stripe_y_end, stripe_z + stripe_spacing)
            glVertex3f(self.width/2 - stripe_width, stripe_y_end, stripe_z + stripe_spacing)
            glVertex3f(self.width/2 - stripe_width, stripe_y_start, stripe_z)
        glEnd()
        
        # Base details (windows)
        window_height = self.height * 0.3
        window_y = self.height * 0.5
        window_width = self.width * 0.6
        
        glColor3f(0.2, 0.4, 0.5)  # Reflective blue-gray
        self._draw_box(-window_width/2, window_y, -self.length/4,
                      window_width, window_height, self.length/4, depth=3)
        
        # Front connector
        glColor3f(0.4, 0.4, 0.4)  # Gray
        self._draw_box(-self.width/4, self.height/4, -self.length/2 - 10,
                      self.width/2, self.height/2, 10)
    
    def _draw_box(self, x, y, z, width, height, length, depth=0):
        """Helper function to draw a box"""
        if depth == 0:
            glBegin(GL_QUADS)
            glVertex3f(x, y, z + length)
            glVertex3f(x + width, y, z + length)
            glVertex3f(x + width, y + height, z + length)
            glVertex3f(x, y + height, z + length)
            glVertex3f(x, y, z)
            glVertex3f(x, y + height, z)
            glVertex3f(x + width, y + height, z)
            glVertex3f(x + width, y, z)
            glVertex3f(x, y, z)
            glVertex3f(x, y, z + length)
            glVertex3f(x, y + height, z + length)
            glVertex3f(x, y + height, z)
            glVertex3f(x + width, y, z)
            glVertex3f(x + width, y + height, z)
            glVertex3f(x + width, y + height, z + length)
            glVertex3f(x + width, y, z + length)
            glVertex3f(x, y + height, z)
            glVertex3f(x, y + height, z + length)
            glVertex3f(x + width, y + height, z + length)
            glVertex3f(x + width, y + height, z)
            glVertex3f(x, y, z)
            glVertex3f(x + width, y, z)
            glVertex3f(x + width, y, z + length)
            glVertex3f(x, y, z + length)
            glEnd()
        else:
            glBegin(GL_QUADS)
            glVertex3f(x, y, z)
            glVertex3f(x + width, y, z)
            glVertex3f(x + width, y + height, z)
            glVertex3f(x, y + height, z)
            glColor3f(0.1, 0.1, 0.1)
            glVertex3f(x + depth, y + depth, z - depth)
            glVertex3f(x + width - depth, y + depth, z - depth)
            glVertex3f(x + width - depth, y + height - depth, z - depth)
            glVertex3f(x + depth, y + height - depth, z - depth)
            glEnd()
    
    def _draw_rounded_box(self, x, y, z, width, height, length):
        """Helper function to draw a box with rounded corners"""
        self._draw_box(x + 10, y, z + 10, width - 20, height, length - 20)
        
        corner_radius = 10
        detail_level = 8
        
        glBegin(GL_QUAD_STRIP)
        for i in range(detail_level + 1):
            angle = (i / detail_level) * math.pi / 2
            dx = corner_radius * math.cos(angle)
            dz = corner_radius * math.sin(angle)
            glVertex3f(x + corner_radius - dx, y, z + length - corner_radius + dz)
            glVertex3f(x + corner_radius - dx, y + height, z + length - corner_radius + dz)
            if i == detail_level:
                glVertex3f(x + width - corner_radius + dx, y, z + length - corner_radius + dz)
                glVertex3f(x + width - corner_radius + dx, y + height, z + length - corner_radius + dz)
        glEnd()
        
        glBegin(GL_QUAD_STRIP)
        for i in range(detail_level + 1):
            angle = (i / detail_level) * math.pi / 2 + math.pi / 2
            dx = corner_radius * math.cos(angle)
            dz = corner_radius * math.sin(angle)
            glVertex3f(x + width - corner_radius + dx, y, z + corner_radius - dz)
            glVertex3f(x + width - corner_radius + dx, y + height, z + corner_radius - dz)
            if i == detail_level:
                glVertex3f(x + corner_radius - dx, y, z + corner_radius - dz)
                glVertex3f(x + corner_radius - dx, y + height, z + corner_radius - dz)
        glEnd()
    
    def _draw_tunnel_opening(self, width, height):
        """Draw a tunnel opening with a circular shape"""
        detail_level = 16
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(detail_level + 1):
            angle = (i / detail_level) * 2 * math.pi
            dx = width/2 * math.cos(angle)
            dy = height/2 * math.sin(angle)
            glVertex3f(dx, dy, 0)
        glEnd()
        glColor3f(0.05, 0.05, 0.05)
        glBegin(GL_QUAD_STRIP)
        for i in range(detail_level + 1):
            angle = (i / detail_level) * 2 * math.pi
            dx = width/2 * math.cos(angle)
            dy = height/2 * math.sin(angle)
            glVertex3f(dx, dy, 0)
            glVertex3f(dx * 0.7, dy * 0.7, -20)
        glEnd()

class Train:
    def __init__(self, train_type, track_position=0, z_position=-20):
        """
        Initialize a train with specific attributes
        
        Args:
            train_type: 0=regular, 1=tunnel, 2=ramp
            track_position: 0=left, 1=center, 2=right
            z_position: Position along z-axis (negative is into the screen)
        """
        self.train_type = train_type
        self.track_position = track_position
        self.z_position = z_position
        self.speed = 0.2
        
        self.carriages = []
        carriage_spacing = 250
        
        if train_type == 0:  # Regular train
            num_carriages = random.randint(3, 5)
            for i in range(num_carriages):
                position_offset = (num_carriages - 1 - i) * carriage_spacing
                color_variation = i * 0.05
                carriage = TrainCarriage(0, position_offset, color_variation)
                self.carriages.append(carriage)
                
        elif train_type == 1:  # Tunnel train
            num_regular = random.randint(2, 3)
            total_carriages = 1 + num_regular
            # Tunnel carriage at front
            self.carriages.append(TrainCarriage(1, (total_carriages - 1) * carriage_spacing, 0))
            for i in range(num_regular):
                position_offset = (total_carriages - 2 - i) * carriage_spacing
                color_variation = i * 0.05
                carriage = TrainCarriage(0, position_offset, color_variation)
                self.carriages.append(carriage)
                
        else:  # Ramp train
            num_regular = random.randint(3, 5)
            total_carriages = 1 + num_regular
            # Ramp carriage at front
            self.carriages.append(TrainCarriage(2, (total_carriages - 1) * carriage_spacing, 0))
            for i in range(num_regular):
                position_offset = (total_carriages - 2 - i) * carriage_spacing
                color_variation = i * 0.05
                carriage = TrainCarriage(0, position_offset, color_variation)
                self.carriages.append(carriage)
    
    def update(self):
        """Update train position"""
        self.z_position += self.speed
    
    def is_visible(self):
        """Check if train is in visible range"""
        last_carriage_offset = 0
        if self.carriages:
            last_carriage_offset = self.carriages[-1].position_offset
        front_z = self.z_position + last_carriage_offset  # Since offsets are positive for front
        back_z = self.z_position
        return (front_z > -2000 and front_z < 800) or (back_z > -2000 and back_z < 800)
    
    def get_position(self):
        """Get the train's current position"""
        x = (self.track_position - 1) * 400  # Centers at -400, 0, 400
        return x, self.z_position, 0
    
    def draw(self):
        """Draw the train with all its carriages"""
        x, y, z = self.get_position()
        for carriage in self.carriages:
            carriage.draw(x, y, z)

class TrainManager:
    def __init__(self, base_speed=5.0):
        """Initialize the train manager"""
        self.base_speed = base_speed
        self.trains = []
        self.last_spawn_time = time.time()
        self.spawn_interval = 2.0
        
        self._spawn_train()
    
    def update_and_draw(self):
        """Update and draw all trains"""
        current_time = time.time()
        
        if current_time - self.last_spawn_time > self.spawn_interval:
            self._spawn_train()
            self.last_spawn_time = current_time
            self.spawn_interval = 2.0 + random.random() * 2.0
        
        visible_trains = []
        for train in self.trains:
            train.speed = self.base_speed * 0.1
            train.update()
            if train.is_visible():
                train.draw()
                visible_trains.append(train)
            elif train.z_position > 1000:
                pass
            else:
                visible_trains.append(train)
        
        self.trains = visible_trains
    
    def _spawn_train(self):
        """Spawn a new train"""
        train_type = random.randint(0, 2)
        track_position = random.randint(0, 2)
        z_position = -GRID_LENGTH
        
        for train in self.trains:
            if (train.track_position == track_position and 
                abs(train.z_position - z_position) < 1000):
                track_position = (track_position + 1) % 3
                break
        
        new_train = Train(train_type, track_position, z_position)
        self.trains.append(new_train)
        
    def set_speed(self, speed):
        """Set the base speed for all trains"""
        self.base_speed = max(1.0, speed)