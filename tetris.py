import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],         # O
    [[1, 0, 0], [1, 1, 1]],   # L
    [[0, 0, 1], [1, 1, 1]],   # J
    [[0, 1, 1], [1, 1, 0]],   # S
    [[1, 1, 0], [0, 1, 1]],   # Z
    [[1, 1, 1, 1]]            # I
]

COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]

# Define Tetromino class
class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotated_shape(self):
        return list(zip(*self.shape[::-1]))

# Define the Tetris game class
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.running = True

    def new_piece(self):
        return Tetromino(3, 0, random.choice(SHAPES))

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, piece):
        shape = piece.rotated_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def valid_space(self, piece):
        shape = piece.rotated_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x
                    new_y = piece.y + y
                    if new_x < 0 or new_x >= len(self.grid[0]) or new_y >= len(self.grid):
                        return False
                    if self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def lock_piece(self, piece):
        shape = piece.rotated_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[piece.y + y][piece.x + x] = piece.color

    def clear_lines(self):
        lines_to_clear = [row for row in self.grid if all(cell != BLACK for cell in row)]
        for line in lines_to_clear:
            self.grid.remove(line)
            self.grid.insert(0, [BLACK for _ in range(len(self.grid[0]))])

    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        self.current_piece.y += 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        self.current_piece.rotation += 1
                        if not self.valid_space(self.current_piece):
                            self.current_piece.rotation -= 1

            self.current_piece.y += 1
            if not self.valid_space(self.current_piece):
                self.current_piece.y -= 1
                self.lock_piece(self.current_piece)
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()
                if not self.valid_space(self.current_piece):
                    self.running = False

            self.clear_lines()
            pygame.display.flip()
            self.clock.tick(10)

# Run the game
if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()
