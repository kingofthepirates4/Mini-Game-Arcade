import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1300, 600))
        pygame.display.set_caption("Haunted Forest Runner")
        self.clock = pygame.time.Clock()
        self.running = True  
        self.active = False
        self.background = pygame.image.load("assets/forest.png")  
        self.background = pygame.transform.scale(self.background, (1300, 600))
        self.intro_background = pygame.image.load("assets/intro_forest2.png")
        self.intro_background = pygame.transform.scale(self.intro_background, (1300, 600))


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            if not self.active and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.button_rect.collidepoint(mouse_pos):
                        self.active = True

    def update(self):
        pass

    def render(self):
        self.screen.blit(self.background, (0, 0))  
        pygame.display.update()  
    def intro(self):
        button_width, button_height = 300, 100
        button_x, button_y = 500, 300
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect)
        self.screen.blit(self.intro_background, (0, 0))
        pygame.display.update()
        return button_rect
    def run(self):
        while self.running:
            self.handle_events()
            if not self.active:
                self.button_rect = self.intro()
            if self.active:
                self.render()
            self.clock.tick(60)  
        pygame.quit()

if __name__ == "__main__":
    game = Game()  
    game.run()
