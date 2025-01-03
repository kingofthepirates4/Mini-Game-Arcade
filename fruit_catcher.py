import pygame
import random

'''
This is a fruit-catching game where fruits and vegetables fall from the sky, and you control a cart to catch them. 
You earn points for each item caught before they hit the ground. 
'''

# Class for Falling Items (Fruits/Vegetables)
class FallingItem:
    def __init__(self, image, points, x, y):
        """
        Initialize the falling item.
        :param image: The image of the item.
        :param points: The points awarded for catching this item.
        :param x: Initial horizontal position.
        :param y: Initial vertical position.
        """
        self.image = image  # The fruit/vegetable image
        self.rect = self.image.get_rect(topleft=(x, y))  # The position of the item
        self.points = points  # Points value for this item

    def move(self, speed, height):
        """
        Move the item downward and reset if it goes off-screen.
        :param speed: How fast the item falls.
        :param height: The screen height.
        """
        self.rect.y += speed  # Move downward
        if self.rect.y > height:  # If it falls off the screen
            self.rect.y = 900  
            

    def draw(self, screen):
        """Draw the item on the screen."""
        screen.blit(self.image, self.rect)


# Class for the Catcher (Basket/Cart)
class Catcher:
    def __init__(self, image, x, y):
        """
        Initialize the catcher.
        :param image: The image of the catcher.
        :param x: Initial horizontal position.
        :param y: Initial vertical position.
        """
        self.image = pygame.transform.scale(image, (300, 300))  # Full cart image
        self.rect = self.image.get_rect(center=(x, y))  # Full cart rectangle

    @property
    def hitbox(self):
        """
        Define a smaller hitbox for the catcher.
        This will be used for collision detection.
        """
        padding = 50  # Shrinks the rectangle by 50 pixels on each side
        return self.rect.inflate(-padding, -padding)  # Shrinks both width and height by padding

    def move(self, mouse_x, screen_width):
        """
        Move the catcher to follow the mouse horizontally.
        :param mouse_x: The current horizontal position of the mouse.
        :param screen_width: The width of the screen (to prevent going off-screen).
        """
        self.rect.x = mouse_x - self.rect.width // 2  # Center the catcher under the mouse
        # Keeps the catcher within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, screen):
        """Draw the catcher on the screen."""
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.width, self.height = 1200, 800  # Screen dimensions
        self.screen = pygame.display.set_mode((self.width, self.height))  # Game window
        pygame.display.set_caption("Fruit Catcher")  # Window title
        self.clock = pygame.time.Clock()  # Control the frame rate
        # Loads the background image
        self.background = pygame.image.load("assets/street.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.farmer = pygame.image.load("assets/farmer.png")
        self.farmer = pygame.transform.scale(self.farmer, (700, 800))
        # Loads the catcher image
        catcher_image = pygame.image.load("assets/cart.png")
        self.catcher = Catcher(catcher_image, self.width // 2, self.height - 70)

        # Loads fruit/vegetable images
        self.items_data = [
            {"name": "apple", "image": pygame.image.load("assets/apple.png"), "points": 3},
            {"name": "banana", "image": pygame.image.load("assets/banana.png"), "points": 5},
            {"name": "carrot", "image": pygame.image.load("assets/carrot.png"), "points": 4},
            {"name": "blueberries", "image": pygame.image.load("assets/blueberries.png"), "points": 6},
            {"name": "potato", "image": pygame.image.load("assets/potato.png"), "points": 2},
            {"name": "grapes", "image": pygame.image.load("assets/grapes.png"), "points": 7},
        ]
        for item in self.items_data:
            item["image"] = pygame.transform.scale(item["image"], (80, 80))

        # Initialize falling items and timers
        self.falling_items = []  # An empty list of falling items
        self.spawn_interval = 2000  #
        self.last_spawn_time = pygame.time.get_ticks()  # Records the time when the game starts

        # Initialize score, font, and timer
        self.score = 0
        self.large_font = pygame.font.Font(None, 72)
        self.smaller_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 48)
        self.timer_duration = 25  # Game duration in seconds
        self.start_time = None  # Timer for the game

        self.active = False
        self.game_over = False

    def spawn_fruit(self):
        """Spawn a new fruit/vegetable every 2 seconds."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            new_item_data = random.choice(self.items_data)
            new_item = FallingItem(
                new_item_data["image"],
                new_item_data["points"],
                random.randint(0, self.width - 80),
                -30
            )
            self.falling_items.append(new_item)
            self.last_spawn_time = current_time

    def check_collision(self):
        """Check for collisions between the catcher and falling items."""
        for item in self.falling_items:
            if self.catcher.hitbox.colliderect(item.rect):  # Use the smaller hitbox
                self.score += item.points  # Add the item's points to the score
                item.rect.y = -900  # Reset the item to the top
                item.rect.x = random.randint(0, self.width - item.rect.width)  # Randomize position

    def draw_score(self):
        """Draw the current score and timer on the screen."""
        # Displays the score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Top-left corner

        # Displays the timer
        if self.start_time:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Time in seconds
            remaining_time = max(self.timer_duration - elapsed_time, 0)
            timer_text = self.font.render(f"Time Left: {remaining_time}s", True, (255, 255, 255))
            self.screen.blit(timer_text, (10, 50))  # Below the score
            if remaining_time <= 0:
                self.game_over = True  # End the game when timer runs out

    def draw_intro(self):
        """Draw the intro screen with the white box, reasonable text, and Help button."""
        box_width, box_height = 570, 250
        box_x, box_y = (self.width - box_width) // 2 - 200, (self.height - box_height) // 2 - 60
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        # The white box
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect, 3)

        # Intro text
        intro_text = (
            "Hello there! It's a busy day at the market.\n"
            "The fruit seller needs your help to catch\n"
            "fruits and vegetables and earn the most coins!"
        )
        lines = intro_text.split("\n")
        y_offset = box_y + 50
        for line in lines:
            text_surface = self.smaller_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.width // 2 - 200, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30

        # Help button
        button_width, button_height = 200, 50
        button_x, button_y = (self.width - button_width) // 2 - 200, box_y + box_height - 70
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)

        button_text = self.font.render("Help", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        return button_rect

    def draw_game_over(self):
        """Draw the game over screen."""
        self.screen.fill((0, 0, 0))  
        self.screen.blit(self.background, (0, 0))
        game_over_text = self.large_font.render("Game Over!", True, (255, 255, 255))
        score_text = self.font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Click anywhere to restart.", True, (200, 200, 200))
        self.screen.blit(game_over_text, (self.width // 2 - 150, self.height // 2 - 100))
        self.screen.blit(score_text, (self.width // 2 - 150, self.height // 2))
        self.screen.blit(restart_text, (self.width // 2 - 220, self.height // 2 + 100))

    def run(self):
        """Run the game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if not self.active and not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    button_rect = self.draw_intro()
                    if button_rect.collidepoint(mouse_pos):
                        self.active = True
                        self.start_time = pygame.time.get_ticks()  # Start the timer
                elif self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    self.__init__()  # Restart the game

            if self.active and not self.game_over:
                # spawn fruits every 2 seconds
                self.spawn_fruit()

                # Game logic
                mouse_x, _ = pygame.mouse.get_pos()
                self.catcher.move(mouse_x, self.width)
                for item in self.falling_items:
                    item.move(8, self.height)
                self.check_collision()

                # Draws the game screen
                self.screen.blit(self.background, (0, 0))
                self.catcher.draw(self.screen)
                for item in self.falling_items:
                    item.draw(self.screen)
                self.draw_score()
            elif self.game_over:
                self.draw_game_over()
            else:
                # Intro screen
                self.screen.blit(self.background, (0, 0))
                self.draw_intro()
                self.screen.blit(self.farmer, (500, 70))

            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()



# Run the Game
if __name__ == "__main__":
    game = Game()  
    game.run()  
