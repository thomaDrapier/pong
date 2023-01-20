import pygame
from paddle import Paddle
from ball import Ball
import numpy as np

screen_width = 800
screen_height = 500

class Game():

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.left_paddle = Paddle(10, screen_height//2, 10, 140)
        self.right_paddle = Paddle(780, screen_height//2, 10, 140)
        self.ball = Ball(screen_width//2, screen_height//2, 10)
        self.pressed = {}
        self.game_info = {
            'left_paddle_score' : 0,
            'left_paddle_kick': 0,
            'right_paddle_score': 0,
            'right_paddle_kick': 0,
        }
    
    def game_event_detection(self):
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    quit()

                elif event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True

                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False
    
    def move_paddles(self):

        if self.pressed.get(pygame.K_a):
                self.left_paddle.move("up")
        elif self.pressed.get(pygame.K_p):
            self.right_paddle.move("up")
        
        if self.pressed.get(pygame.K_q):
            self.left_paddle.move("down")
        elif self.pressed.get(pygame.K_m):
            self.right_paddle.move("down")
    
    def collision_detection(self):
        # collision mur haut
        if self.ball.y - self.ball.radius <= 0:
            self.ball.vel_y *= -1
        # collision mur du bas
        elif self.ball.y + self.ball.radius >= self.screen_height:
            self.ball.vel_y *= -1
        # collision paddle gauche
        elif self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
            if (self.ball.y < self.left_paddle.y + self.left_paddle.height) & (self.ball.y > self.left_paddle.y):
                demi_longeur_paddle = self.left_paddle.height/2
                l = abs((self.left_paddle.y + demi_longeur_paddle) - self.ball.y)
                factor = (l / demi_longeur_paddle)*0.8

                if self.ball.y > self.left_paddle.y + demi_longeur_paddle:
                    self.ball.vel_y = abs(self.ball.VELOCITY * factor)
                else :
                    self.ball.vel_y = -abs(self.ball.VELOCITY * factor)
                    
                self.ball.vel_x = 1*np.sqrt((self.ball.VELOCITY**2)*(1-factor**2))
                self.game_info['left_paddle_kick'] += 1

        # collision paddle droit
        elif self.ball.x + self.ball.radius >= self.right_paddle.x:
            if (self.ball.y < self.right_paddle.y + self.right_paddle.height) & (self.ball.y > self.right_paddle.y):
                demi_longeur_paddle = self.right_paddle.height/2
                l = (self.right_paddle.y + demi_longeur_paddle) - self.ball.y
                factor = (l / demi_longeur_paddle)*0.8
                factor *= -1 if self.ball.y > self.right_paddle.y + demi_longeur_paddle else factor 
    
                if self.ball.y > self.right_paddle.y + demi_longeur_paddle:
                    self.ball.vel_y = abs(self.ball.VELOCITY * factor)
                else :
                    self.ball.vel_y = -abs(self.ball.VELOCITY * factor)
                self.ball.vel_x = -1*np.sqrt((self.ball.VELOCITY**2)*(1-factor**2))
                self.game_info['right_paddle_kick'] += 1
            

    def win(self):
        if self.ball.x < self.left_paddle.x + self.left_paddle.width:
            self.game_info['right_paddle_score'] += 1
            self.ball.new_ball(self.screen_width, self.screen_height)

        if self.ball.x > self.right_paddle.x:
            self.game_info['left_paddle_score'] += 1
            self.ball.new_ball(self.screen_width, self.screen_height)
  


    def draw_game(self):
            clock = pygame.time.Clock()
            # clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.left_paddle.draw(self.screen)
            self.right_paddle.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.update()

            self.collision_detection()
            self.ball.run_ball()
            self.move_paddles()
            self.game_event_detection()
    
    def run(self):
        run = True
        self.ball.new_ball(self.screen_width, self.screen_height)
        while run :
            clock = pygame.time.Clock()
            clock.tick(100)
            self.screen.fill((0, 0, 0))
            self.left_paddle.draw(self.screen)
            self.right_paddle.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.update()

            self.collision_detection()
            self.ball.run_ball()
            self.move_paddles()
            self.win()
            self.game_event_detection()



if __name__ == '__main__':

    game = Game(screen_width, screen_height)
    game.run()



