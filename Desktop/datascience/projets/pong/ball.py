import pygame
import numpy as np
WHITE  = (255, 255, 255)

class Ball():
    COLOR = WHITE
    VELOCITY = 5
    
    def __init__(self, x, y, radius):
        self.x  = x
        self.y = y
        self.radius = radius
        self.vel_y = 0
        self.vel_x = 0
        

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)
    
    def run_ball(self):
        self.x += self.vel_x
        self.y += self.vel_y
    
    def new_ball(self, screen_width, screen_height):
        a = np.random.uniform(0, 1)
        self.x = screen_width//2
        self.y = screen_height//2
        self.vel_y = (np.random.choice([1, -1]))*a*self.VELOCITY
        self.vel_x = (np.random.choice([1, -1]))*np.sqrt((self.VELOCITY**2)*(1-a**2))



