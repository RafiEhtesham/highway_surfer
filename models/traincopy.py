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
            train_type: 0=regular, 1=tunnel
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
        else:  # Tunnel train
            self.base_color = (0.3, 0.3, 0.9)  # Bright blue
            self.height = 240  # Taller for tunnel
        
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
        else:
            self._draw_tunnel_carriage()
            
        glPopMatrix()
    
    def _draw_regular_carriage(self):
        """Draw a regular subway train carriage with creative enhancements"""
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
        
        # Front window (subway-style)
        glColor3f(0.2, 0.4, 0.5)
        self._draw_box(-self.width/3, self.height*0.6, -self.length/2 - 1,
                       self.width*2/3, self.height*0.3, 1)
        
        # Doors (double doors in the middle)
        door_width = self.width * 0.3
        door_height = self.height * 0.7
        door_y = self.height * 0.35
        
        glColor3f(r*0.7, g*0.7, b*0.7)  # Slightly darker than body
        self._draw_box(-door_width, door_y, -self.length/8,
                      door_width*2, door_height, self.length/4, depth=2)
        
        # Graffiti-style details (triangles, circles, lines)
        glColor3f(0.0, 1.0, 0.0)  # Neon green triangle
        self._draw_triangle(-self.width/4, self.height/2, -self.length/4,
                           self.width/4, self.height/2, -self.length/4,
                           0, self.height*0.75, -self.length/4)
        
        glColor3f(1.0, 0.0, 1.0)  # Magenta circle
        self._draw_circle(0, self.height/2, self.length/4, 50)
        
        glColor3f(1.0, 0.5, 0.0)  # Orange line
        self._draw_line(-self.width/3, self.height/3, -self.length/3,
                       self.width/3, self.height*0.7, self.length/3)
        
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
        
        # Wheels
        glColor3f(0.3, 0.3, 0.3)  # Dark gray
        wheel_radius = 20
        wheel_positions = [
            (-self.width/2 + 30, 0, -self.length/3),
            (self.width/2 - 30, 0, -self.length/3),
            (-self.width/2 + 30, 0, self.length/3),
            (self.width/2 - 30, 0, self.length/3)
        ]
        for pos in wheel_positions:
            glPushMatrix()
            glTranslatef(*pos)
            self._draw_circle(0, 0, 0, wheel_radius)
            glPopMatrix()
        
        # Connectors with rivets
        glColor3f(0.4, 0.4, 0.4)  # Gray
        self._draw_box(-self.width/4, self.height/4, -self.length/2 - 10,
                      self.width/2, self.height/2, 10)
        self._draw_box(-self.width/4, self.height/4, self.length/2,
                      self.width/2, self.height/2, 10)
        
        glColor3f(0.2, 0.2, 0.2)  # Dark gray rivets
        rivet_size = 5
        for i in [-1, 1]:
            for j in [-1, 1]:
                glPushMatrix()
                glTranslatef(i * self.width/4, self.height/4 + j * self.height/4, -self.length/2 - 5)
                glutSolidSphere(rivet_size, 5, 5)
                glPopMatrix()
    
    def _draw_tunnel_carriage(self):
        """Draw a tunnel train carriage with industrial enhancements"""
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
        
        # Warning stripes (yellow and black)
        stripe_width = 20
        num_stripes = 5
        for i in range(num_stripes):
            if i % 2 == 0:
                glColor3f(1.0, 1.0, 0.0)  # Yellow
            else:
                glColor3f(0.0, 0.0, 0.0)  # Black
            self._draw_box(-self.width/2 + i*stripe_width, self.height*0.8, -self.length/2,
                          stripe_width, self.height*0.2, self.length)
        
        # Roof antenna
        glColor3f(0.3, 0.3, 0.3)  # Dark gray
        self._draw_box(-10, self.height, 0, 20, 30, 20)
        
        # Undercarriage
        glColor3f(0.2, 0.2, 0.2)  # Dark gray
        rail_height = 15
        self._draw_box(-self.width/2, 0, -self.length/2,
                      self.width, rail_height, self.length)
        
        # Back connector
        glColor3f(0.4, 0.4, 0.4)  # Gray
        self._draw_box(-self.width/4, self.height/4, self.length/2,
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
            angle = 2 * math.pi * i / detail_level
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
    
    def _draw_triangle(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        """Helper function to draw a triangle"""
        glBegin(GL_TRIANGLES)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        glVertex3f(x3, y3, z3)
        glEnd()
    
    def _draw_circle(self, x, y, z, radius):
        """Helper function to draw a circle"""
        detail_level = 16
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(x, y, z)
        for i in range(detail_level + 1):
            angle = 2 * math.pi * i / detail_level
            dx = radius * math.cos(angle)
            dy = radius * math.sin(angle)
            glVertex3f(x + dx, y + dy, z)
        glEnd()
    
    def _draw_line(self, x1, y1, z1, x2, y2, z2):
        """Helper function to draw a line with thickness"""
        glLineWidth(5.0)
        glBegin(GL_LINES)
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
        glEnd()
        glLineWidth(1.0)

class Train:
    def __init__(self, train_type, track_position=0, z_position=-GRID_LENGTH):
        """
        Initialize a train with specific attributes
        
        Args:
            train_type: 0=regular, 1=tunnel
            track_position: 0=left, 1=center, 2=right
            z_position: Position along y-axis (starts at -GRID_LENGTH)
        """
        self.train_type = train_type
        self.track_position = track_position
        self.z_position = z_position
        self.speed = 0.0  # Speed will be set by TrainManager
        
        self.carriages = []
        # Reduced carriage spacing from 250 to 230
        carriage_spacing = 230
        
        if train_type == 0:  # Regular train
            num_carriages = random.randint(3, 5)
            for i in range(num_carriages):
                position_offset = (num_carriages - 1 - i) * carriage_spacing
                color_variation = i * 0.05
                carriage = TrainCarriage(0, position_offset, color_variation)
                self.carriages.append(carriage)
                
        else:  # Tunnel train
            num_regular = random.randint(2, 3)
            total_carriages = 1 + num_regular
            # Tunnel carriage at front
            self.carriages.append(TrainCarriage(1, (total_carriages - 1) * carriage_spacing, 0))
            for i in range(num_regular):
                position_offset = (total_carriages - 2 - i) * carriage_spacing
                color_variation = i * 0.05
                carriage = TrainCarriage(0, position_offset, color_variation)
                self.carriages.append(carriage)
    
    def update(self, delta_time):
        """Update train position"""
        self.z_position += self.speed * delta_time
    
    def get_position(self):
        """Get the train's current position"""
        x = (self.track_position - 1) * 400  # Centers at -400, 0, 400
        return x, self.z_position, 0
    
    def draw(self):
        """Draw the train with all its carriages"""
        x, y, z = self.get_position()
        for carriage in self.carriages:
            carriage.draw(x, y, z)
    
    def get_length(self):
        """Get the total length of the train"""
        if not self.carriages:
            return 0
        # Length is from front of first carriage to back of last carriage
        return self.carriages[-1].position_offset + self.carriages[-1].length

class TrainManager:
    def __init__(self, base_speed=50.0):
        """Initialize the train manager"""
        self.base_speed = base_speed
        self.trains = []
        self.last_spawn_time = time.time()
        # Decreased spawn interval to make trains more frequent
        self.spawn_interval = 1.5
        
        self._spawn_train()
    
    def update(self, delta_time):
        """Update all trains and spawn new ones if necessary"""
        current_time = time.time()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self._spawn_train()
            self.last_spawn_time = current_time
            # More consistent spawn interval with smaller variation
            self.spawn_interval = 1.5 + random.random() * 1.0
        for train in self.trains:
            train.speed = self.base_speed  # Set speed
            train.update(delta_time)
        # Remove trains that have passed
        self.trains = [train for train in self.trains if train.z_position + (train.carriages[0].position_offset if train.carriages else 0) <= GRID_LENGTH]
    
    def draw(self):
        """Draw all trains"""
        for train in self.trains:
            train.draw()
    
    def _spawn_train(self):
        """Spawn a new train ensuring at least one lane is free"""
        # First, find all currently occupied lanes
        occupied_lanes = set()
        for train in self.trains:
            if train.z_position < 0:  # Check trains behind the player
                occupied_lanes.add(train.track_position)
        
        # Make sure we don't occupy all lanes
        if len(occupied_lanes) >= 2:
            # If 2 lanes are already occupied, we need to pick the free lane
            free_lanes = [lane for lane in range(3) if lane not in occupied_lanes]
            if not free_lanes:  # This shouldn't happen, but just as safety
                return  # Don't spawn a train if all lanes are somehow occupied
        else:
            # Select from all lanes but ensure we keep one free
            all_lanes = list(range(3))
            occupied_after_spawn = list(occupied_lanes)
            
            available_lanes = [lane for lane in all_lanes if lane not in occupied_after_spawn]
            if len(available_lanes) <= 1:
                return  # Don't spawn if only one lane is available
                
            # If we have at least 2 lanes free, we can place a train in one of them
            track_position = random.choice(available_lanes)
            
            # Update occupied lanes to include this new train
            occupied_after_spawn.append(track_position)
            
            # Ensure at least one lane stays free after this spawn
            if len(occupied_after_spawn) >= 3:
                return  # Don't spawn if it would occupy all lanes
            
            train_type = random.randint(0, 1)  # Regular (0) or tunnel (1) trains
            z_position = -GRID_LENGTH  # Spawn at the far end
            new_train = Train(train_type, track_position, z_position)
            self.trains.append(new_train)
    
    def get_occupied_positions(self):
        """Return a list of (lane, start_pos, end_pos) for all train carriages"""
        positions = []
        for train in self.trains:
            lane = train.track_position
            for carriage in train.carriages:
                # Calculate front and back of this carriage
                front_pos = train.z_position + carriage.position_offset - carriage.length/2
                back_pos = train.z_position + carriage.position_offset + carriage.length/2
                positions.append((lane, front_pos, back_pos))
        return positions
        
    def set_speed(self, speed):
        """Set the base speed for all trains"""
        self.base_speed = max(1.0, speed)