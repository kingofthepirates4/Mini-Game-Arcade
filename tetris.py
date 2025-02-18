import pygame
import random

class Tetriminos:
    def __init__(self):
        self.tetriminos = {
            "I": [[1, 1, 1, 1]],
            "J": [[1, 1, 1], [0, 0, 1]],
            "L": [[1, 1, 1], [1, 0, 0]],
            "O": [[1, 1], [1, 1]],
            "S": [[0, 1, 1], [1, 1, 0]],
            "T": [[1, 1, 1], [0, 1, 0]],
            "Z": [[1, 1, 0], [0, 1, 1]]
        }
        self.colors = {
            "I": (0, 255, 255),
            "J": (0, 0, 255),
            "L": (255, 165, 0),
            "O": (255, 255, 0),
            "S": (0, 255, 0),
            "T": (128, 0, 128),
            "Z": (255, 0, 0)
        }
    
    def get_list(self):
        return list(self.tetriminos.keys())

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen_width = 500
        self.screen_height = 550
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        
        #grid dimensions
        self.columns = 10
        self.rows = 20
        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        
        # Game state flags
        self.startingpage = True
        self.active = False
        self.game_over = False  
        self.running = True

        #intro background
        self.intro_background = pygame.image.load("assets/tetris.png")
        self.intro_background = pygame.transform.scale(self.intro_background, (self.screen_width, self.screen_height))

    
        # Custom event: piece falls every 500ms
        self.TETRIMINO_FALL_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TETRIMINO_FALL_EVENT, 500)
        
        self.tetriminos = Tetriminos()
        self.current_tetrimino = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)

    def spawn_new_piece(self):
        """Spawns a new piece at the top center of the grid.
           If the spawn position is invalid, sets game_over flag to True."""
        tetrimino_key = random.choice(self.tetriminos.get_list())
        shape = self.tetriminos.tetriminos[tetrimino_key]
        color = self.tetriminos.colors[tetrimino_key]
        x = (self.columns - len(shape[0])) // 2
        y = 0
        # Checks if the spawn position is valid; if not, it's game over.
        if not self.is_valid_position(shape, x, y):
            print("Game Over!")
            self.active = False
            self.game_over = True
            return
        self.current_tetrimino = shape
        self.current_color = color
        self.current_x = x
        self.current_y = y

    def is_valid_position(self, shape, x, y):
        """Returns True if the given shape at (x,y) does not collide with boundaries or settled pieces."""
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    grid_x = x + j
                    grid_y = y + i
                    # Checks boundaries
                    if grid_x < 0 or grid_x >= self.columns or grid_y < 0 or grid_y >= self.rows:
                        return False
                    # Checks for collision with settled blocks
                    if self.grid[grid_y][grid_x] is not None:
                        return False
        return True

    def merge_piece_to_grid(self):
        """Merge the current piece into the grid once it can no longer move down."""
        shape = self.current_tetrimino
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    grid_x = self.current_x + j
                    grid_y = self.current_y + i
                    if 0 <= grid_x < self.columns and 0 <= grid_y < self.rows:
                        self.grid[grid_y][grid_x] = self.current_color

    def clear_lines(self):
        """Clears completed lines, updates the grid, and increments the score (+1 per line cleared)."""
        new_grid = []
        lines_cleared = 0
        for row in self.grid:
            if all(cell is not None for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)
        # Adds empty rows for each cleared line
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(self.columns)])
        self.grid = new_grid
        self.score += lines_cleared

    def move_current_piece(self, dx, dy):
        """Attempts to move the current piece by (dx,dy); returns True if successful."""
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        if self.is_valid_position(self.current_tetrimino, new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
            return True
        return False

    def rotate_current_piece(self):
        """Rotates the current piece clockwise if the new position is valid."""
        rotated = list(zip(*self.current_tetrimino[::-1]))
        rotated = [list(row) for row in rotated]
        if self.is_valid_position(rotated, self.current_x, self.current_y):
            self.current_tetrimino = rotated

    def draw_grid(self):
        """Draws the settled pieces and grid lines."""
        block_width = self.screen_width / self.columns
        block_height = self.screen_height / self.rows
        
        # Draws settled pieces
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] is not None:
                    pygame.draw.rect(self.screen, self.grid[i][j],
                                     (j * block_width, i * block_height, block_width, block_height))
        
        # Draws grid lines
        for i in range(self.rows):
            pygame.draw.line(self.screen, (255, 255, 255), (0, i * block_height), (self.screen_width, i * block_height))
        for j in range(self.columns):
            pygame.draw.line(self.screen, (255, 255, 255), (j * block_width, 0), (j * block_width, self.screen_height))

    def draw_current_piece(self):
        """Draws the falling piece."""
        block_width = self.screen_width / self.columns
        block_height = self.screen_height / self.rows
        shape = self.current_tetrimino
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    x = (self.current_x + j) * block_width
                    y = (self.current_y + i) * block_height
                    pygame.draw.rect(self.screen, self.current_color, (x, y, block_width, block_height))
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, block_width, block_height), 1)

    def draw_score(self):
        """Displays the current score on the screen."""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def display_scoreboard(self):
        """Displays the game over screen with the final score."""
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        final_score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        prompt_text = self.font.render("Press any key to exit", True, (255, 255, 255))
        
        
        game_over_rect = game_over_text.get_rect(center=(self.screen_width/2, self.screen_height/2 - 50))
        score_rect = final_score_text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        prompt_rect = prompt_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, score_rect)
        self.screen.blit(prompt_text, prompt_rect)
        pygame.display.update()

    def intro(self):
        """Displays the intro screen."""
        self.screen.blit(self.intro_background, (0, 0))
        pygame.display.update()

    def gameplay(self):
        """Renders the gameplay: grid, current piece, and score."""
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_current_piece()
        self.draw_score()
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # If game is over, wait for any key press to exit
                if self.game_over:
                    if event.type == pygame.KEYDOWN:
                        self.running = False
                    continue

                # Start the game by pressing Enter on the intro screen
                if self.startingpage and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.active = True
                    self.startingpage = False
                    self.spawn_new_piece()
                
                # Game controls when active
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_LEFT:
                        self.move_current_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_current_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        # accelerate the piece
                        self.move_current_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_current_piece()
                
                # Automatic falling of the piece
                elif event.type == self.TETRIMINO_FALL_EVENT and self.active:
                    if not self.move_current_piece(0, 1):
                        self.merge_piece_to_grid()
                        self.clear_lines()
                        self.spawn_new_piece()

            if self.startingpage:
                self.intro()
            elif self.game_over:
                self.display_scoreboard()
            elif self.active:
                self.gameplay()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
