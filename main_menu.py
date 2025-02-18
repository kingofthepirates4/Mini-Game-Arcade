import pygame

class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1300, 780))
        pygame.display.set_caption("Main Menu")
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load("assets/arcade.png")
        self.background = pygame.transform.scale(self.background, (1300, 780))

    def draw_menu(self):
        """Draw the main menu screen with game options."""
        self.screen.blit(self.background, (0, 0))

        title_font = pygame.font.Font(None, 100)
        button_font = pygame.font.Font(None, 60)

        # Title text
        title_text = title_font.render("Game Menu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 180))
        self.screen.blit(title_text, title_rect)

        # Game options
        self.game_buttons = []
        games = ["Fruit Catcher", "Runner Game", "Tetris"]
        for i, game_name in enumerate(games):
            button_width, button_height = 400, 80
            button_x = (self.screen.get_width() - button_width) // 2
            button_y = 270 + i * 120
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.game_buttons.append((game_name, button_rect))

            pygame.draw.rect(self.screen, (0, 100 + i * 30, 200), button_rect)
            button_text = button_font.render(game_name, True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        pygame.display.update()

    def run(self):
        """Main menu loop."""
        while self.running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, (game_name, button_rect) in enumerate(self.game_buttons):
                        if button_rect.collidepoint(mouse_pos):
                            if i == 0:
                                return "fruit_catcher"  
                            elif i == 1:
                                return "runner"  
                            elif i == 2:
                                return "tetris"
                            else:
                                return None
            self.clock.tick(60)
