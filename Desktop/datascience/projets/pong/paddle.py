import pygame

WHITE  = (255, 255, 255)

class Paddle():

    COLOR = WHITE
    VELOCITY = 5

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self,a):
        if a == "up":
            if self.y < 0 :
                pass
            else :
                self.y -= self.VELOCITY
        else :
            if self.y + self.height > 500:
                pass
            else :
                self.y += self.VELOCITY
