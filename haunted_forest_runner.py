''' A runner game where the player must jump over tombstones to escape the haunted forest. '''

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

        
        self.heart = pygame.image.load("assets/heart.png")
        self.heart = pygame.transform.scale(self.heart, (50, 50))  

        self.lives = 3 

        
        self.start_time = None  
        self.score_font = pygame.font.Font(None, 36)  

        
        self.background = pygame.image.load("assets/forest.png")
        self.background = pygame.transform.scale(self.background, (1300, 600))
        self.intro_background = pygame.image.load("assets/intro_forest2.png")
        self.intro_background = pygame.transform.scale(self.intro_background, (1300, 600))

        self.bg_x1 = 0
        self.bg_x2 = self.background.get_width()
        self.scroll_speed = 9

        
        self.runner1 = pygame.image.load("assets/runner1.png")
        self.runner1 = pygame.transform.scale(self.runner1, (220, 290))
        self.runner2 = pygame.image.load("assets/runner2.png")
        self.runner2 = pygame.transform.scale(self.runner2, (220, 290))

        self.runner_x, self.runner_y = 60, 270  
        self.current_frame = self.runner1  
        self.frame_time = 250  
        self.last_frame_swap = pygame.time.get_ticks()  

        
        self.is_jumping = False  
        self.jump_speed = -20  
        self.gravity = 1  
        self.ground_level = self.runner_y  

       
        self.obstacles = []  
        self.spawn_time = random.randint(1000, 3000)  # Spawn time between 1 and 3 seconds
        self.last_obstacle_spawn = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if not self.active and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.button_rect.collidepoint(mouse_pos):
                    self.active = True
                    self.start_time = pygame.time.get_ticks()  
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_UP and not self.is_jumping:
                    self.is_jumping = True  

    def update_runner_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_swap >= self.frame_time:
            self.current_frame = self.runner2 if self.current_frame == self.runner1 else self.runner1
            self.last_frame_swap = current_time  

    def update_jump(self):
        if self.is_jumping:
            self.runner_y += self.jump_speed  
            self.jump_speed += self.gravity  

            if self.runner_y >= self.ground_level:
                self.runner_y = self.ground_level  
                self.is_jumping = False  
                self.jump_speed = -20  

    def update_background(self):
        self.bg_x1 -= self.scroll_speed
        self.bg_x2 -= self.scroll_speed

        if self.bg_x1 <= -self.background.get_width():
            self.bg_x1 = self.background.get_width()
        if self.bg_x2 <= -self.background.get_width():
            self.bg_x2 = self.background.get_width()

    def spawn_obstacle(self):
        """Spawn a new tombstone obstacle."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_spawn >= self.spawn_time:
            self.obstacles.append(Obstacle("tombstone", 1300, 460)) 
            self.last_obstacle_spawn = current_time
            self.spawn_time = random.randint(1000, 3000)  

    def update_obstacles(self):
        """Update position and remove off-screen obstacles."""
        for obstacle in self.obstacles:
            obstacle.update_position(self.scroll_speed)
            if obstacle.x < -100:  
                self.obstacles.remove(obstacle)
            if self.check_collision(obstacle):
                self.lives -= 1  
                self.obstacles.remove(obstacle)  
                if self.lives == 0:
                    print("Game Over! No lives left!")
                    self.running = False  

    def check_collision(self, obstacle):
        """Check if the runner collides with an obstacle."""
        runner_rect = pygame.Rect(self.runner_x + 60, self.runner_y + 20, 110, 250)  # Shrunk runner hitbox
        obstacle_rect = pygame.Rect(obstacle.x + 43, obstacle.y + 20, obstacle.width - 80, obstacle.height - 30)
        return runner_rect.colliderect(obstacle_rect)

    def render_hearts(self):
        """Draw the player's remaining hearts."""
        for i in range(self.lives):
            heart_x = 10 + (i * 60)  
            heart_y = 10
            self.screen.blit(self.heart, (heart_x, heart_y))

    def render_score(self):
        """Draw the score based on time survived."""
        if self.start_time:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  
            score_text = self.score_font.render(f"Score: {elapsed_time}s", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 70))

    def render(self):
        """Render all game elements."""
        self.screen.blit(self.background, (self.bg_x1, 0))
        self.screen.blit(self.background, (self.bg_x2, 0))
        self.screen.blit(self.current_frame, (self.runner_x, self.runner_y))

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.render_hearts()  
        self.render_score()  

        pygame.display.update()  

    def intro(self):
        button_width, button_height = 300, 100
        button_x, button_y = 500, 300
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect) 
        self.screen.blit(self.intro_background, (0, 0))  
        pygame.display.update()
        return button_rect

    def show_game_over(self):
        """Show the game over screen with the final score and restart button."""
        
        self.screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 100)
        score_font = pygame.font.Font(None, 60)
        button_font = pygame.font.Font(None, 50)

        
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        score_text = score_font.render(f"Final Score: {self.get_final_score()} seconds", True, (255, 255, 255))
        
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 200))
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 300))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

        
        button_width, button_height = 300, 80
        button_x = (self.screen.get_width() - button_width) // 2
        button_y = 400
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(self.screen, (0, 200, 0), button_rect)  # Green restart button
        button_text = button_font.render("Restart", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        pygame.display.update()  

        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False  
                        self.__init__()  

    def get_final_score(self):
        """Calculate the final score in seconds."""
        if self.start_time:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            return elapsed_time
        return 0

    def run(self):
        while self.running:
            self.handle_events()
            if not self.active and self.lives > 0:
                self.button_rect = self.intro()  
            if self.active:
                self.update_runner_animation()  
                self.update_jump()  
                self.update_background()  
                self.spawn_obstacle()  
                self.update_obstacles()  
                self.render()  
            if self.lives == 0:
                self.active = False
                self.show_game_over()
            self.clock.tick(50)  
        pygame.quit()


class Obstacle:
    def __init__(self, obstacle_type, x, y):
        self.type = obstacle_type
        self.x = x
        self.y = y 

        if self.type == "tombstone":
            self.image = pygame.image.load("assets/tombstone.png")
            self.image = pygame.transform.scale(self.image, (140, 110))
            self.width, self.height = self.image.get_size()

    def update_position(self, speed):
        self.x -= speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


if __name__ == "__main__":
    game = Game()  
    game.run()
