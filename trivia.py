import random
import pygame

class Game: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Trivia Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.active = False
        self.gameover = False
        pass
    def generate_questions(self):
        pass
    def draw_starting_screen(self):
        pass
    def draw_gameover_screen(self):
        pass
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if not self.active and not self.gameover:
                
            self.clock.tick(60)
        pass

if __name__ == "__main__":
    game = Game()  
    game.run()
