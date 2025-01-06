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

        
        self.bg_x1 = 0
        self.bg_x2 = self.background.get_width()
        self.scroll_speed = 5  

        
        self.runner1 = pygame.image.load("assets/runner1.png")
        self.runner1 = pygame.transform.scale(self.runner1, (220, 290))
        self.runner2 = pygame.image.load("assets/runner2.png")
        self.runner2 = pygame.transform.scale(self.runner2, (220, 290))  # Match size for animation

    
        self.runner_x, self.runner_y = 60, 270  # Initial position
        self.current_frame = self.runner1  # Start with the first frame
        self.frame_time = 250  # Time in milliseconds between frames
        self.last_frame_swap = pygame.time.get_ticks()  # Time when the last frame was swapped

        
        self.is_jumping = False  # Track if the runner is in the middle of a jump
        self.jump_speed = -20  # Initial jump velocity (upward)
        self.gravity = 1  # Gravity to bring the runner back down
        self.ground_level = self.runner_y  # Y position of the ground

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if not self.active and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    self.active = True
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_UP and not self.is_jumping:
                    self.is_jumping = True  # Start the jump

    def update_runner_animation(self):
        """Update the runner animation to swap frames."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_swap >= self.frame_time:
            # Swaps runner images for animation
            self.current_frame = self.runner2 if self.current_frame == self.runner1 else self.runner1
            self.last_frame_swap = current_time  # Reset the last swap time

    def update_jump(self):
        """Handle the jumping logic for the runner."""
        if self.is_jumping:
            # Move the runner upward initially, then apply gravity
            self.runner_y += self.jump_speed  # Move up by jump speed
            self.jump_speed += self.gravity  # Gravity pulls down

            # If the runner lands back on the ground, stop the jump
            if self.runner_y >= self.ground_level:
                self.runner_y = self.ground_level  # Reset position to ground level
                self.is_jumping = False  # Stop jumping
                self.jump_speed = -20  # Reset jump speed for next jump

    def update_background(self):
        """Update the position of the scrolling background."""
        self.bg_x1 -= self.scroll_speed
        self.bg_x2 -= self.scroll_speed

        # Resets background position when it scrolls off-screen
        if self.bg_x1 <= -self.background.get_width():
            self.bg_x1 = self.background.get_width()
        if self.bg_x2 <= -self.background.get_width():
            self.bg_x2 = self.background.get_width()

    def render(self):
        """Render the game screen with the scrolling background."""
        
        self.screen.blit(self.background, (self.bg_x1, 0))
        self.screen.blit(self.background, (self.bg_x2, 0))

        self.screen.blit(self.current_frame, (self.runner_x, self.runner_y))
        pygame.display.update()  

    def intro(self):
        """Display the intro screen with a button."""
        button_width, button_height = 300, 100
        button_x, button_y = 500, 300
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect) 
        self.screen.blit(self.intro_background, (0, 0))  
        pygame.display.update()
        return button_rect

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            if not self.active:
                self.button_rect = self.intro()  # Show intro screen
            if self.active:
                self.update_runner_animation()  # Update runner animation
                self.update_jump()  # Update runner jump
                self.update_background()  # Update scrolling background
                self.render()  # Render the game screen
            self.clock.tick(50)  # Maintain 60 FPS
        pygame.quit()

if __name__ == "__main__":
    game = Game()  
    game.run()
