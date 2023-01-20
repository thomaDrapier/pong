import pygame
from game import Game
import neat
import pickle

screen_width = 800
screen_height = 500

class PongGame():
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.game = Game(screen_width, screen_height)
    def run_PongGame(self):
        self.game.draw_game()

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        

        run = True
        self.game.ball.new_ball(self.screen_width, self.screen_height)
        while run:
            distance_rightPaddle_ball = self.game.right_paddle.x - self.game.ball.x
            output2 = net.activate((self.game.right_paddle.y, self.game.ball.y, distance_rightPaddle_ball))
            decision2 = output2.index(max(output2))
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.right_paddle.move('up')
            elif decision2 == 2:
                self.game.right_paddle.move('down')
            
            self.game.collision_detection()
            self.game.ball.run_ball()
            self.game.move_paddles()
            self.game.win()
            self.game.game_event_detection()
            self.game.draw_game()


    
    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        
        run = True
        self.game.ball.new_ball(self.screen_width, self.screen_height)
        while run:
            distance_leftPaddle_ball = self.game.ball.x - self.game.left_paddle.x + self.game.left_paddle.width
            distance_rightPaddle_ball = self.game.right_paddle.x - self.game.ball.x
            
            output1 = net1.activate((self.game.left_paddle.y, self.game.ball.y, distance_leftPaddle_ball))
            decision1 = output1.index(max(output1))
            if decision1 == 0:
                pass
            elif decision1 == 1:
                self.game.left_paddle.move('up')
            elif decision1 == 2:
                self.game.left_paddle.move('down')
            
            output2 = net2.activate((self.game.right_paddle.y, self.game.ball.y, distance_rightPaddle_ball))
            decision2 = output2.index(max(output2))
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.right_paddle.move('up')
            elif decision2 == 2:
                self.game.right_paddle.move('down')
            
            self.game.collision_detection()
            self.game.ball.run_ball()
            self.game.move_paddles()
            self.game.win()
            if self.game.game_info['left_paddle_score'] == 1 or self.game.game_info['right_paddle_score'] == 1 or self.game.game_info['left_paddle_kick'] > 40:
                self.set_fitness(genome1, genome2)
                break
            self.game.game_event_detection()
            self.game.draw_game()
    
    def set_fitness(self, genome1, genome2):
        genome1.fitness += self.game.game_info['left_paddle_kick']
        genome2.fitness += self.game.game_info['right_paddle_kick']



def eval_genomes(genomes, config):
    screen_width = 800
    screen_height = 500
    for i, (id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1 :
            break
        genome1.fitness = 0
        for i, (id2, genome2) in enumerate(genomes):
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            pong = PongGame(screen_width, screen_height)
            pong.train_ai(genome1, genome2, config)

    


PongGame(screen_width, screen_height).game.draw_game()

def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 3)
    return winner


if __name__ == '__main__':
    config  = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "neat.txt")
    run_neat(config)
    
    # output = open('ai.pickle', 'wb')
    # pickle.dump(run_neat(config), output)
    # output.close()

    # input = open('ai.pickle', 'rb')
    # PongGame(screen_width, screen_height).test_ai(pickle.load(input), config)
    # input.close()

    

