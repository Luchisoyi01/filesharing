import time
import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SIZE = 4  # 4x4 grid
WIDTH = 400  # Window width
HEIGHT = 400 + 100  # Window height with extra space for score
TILE_SIZE = WIDTH // SIZE
GAP_SIZE = 5  # Gap between tiles
FONT_SIZE = 40

# Colors
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_TILE_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Fonts
FONT = pygame.font.SysFont("arial", FONT_SIZE)
SCORE_FONT = pygame.font.SysFont("arial", 30)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Functions
def draw_tile(value, x, y):
    rect = pygame.Rect(x, y, TILE_SIZE - GAP_SIZE, TILE_SIZE - GAP_SIZE)
    color = TILE_COLORS.get(value, TILE_COLORS[2048])
    pygame.draw.rect(screen, color, rect, border_radius=5)
    if value:
        text = FONT.render(str(value), True, (119, 110, 101))
        text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        screen.blit(text, text_rect)

def draw_grid(grid, score):
    screen.fill(BACKGROUND_COLOR)
    for i in range(SIZE):
        for j in range(SIZE):
            value = grid[i][j]
            x = j * TILE_SIZE + GAP_SIZE
            y = i * TILE_SIZE + GAP_SIZE + 100
            draw_tile(value, x, y)
    score_text = SCORE_FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def initialize_grid():
    grid = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

def add_new_tile(grid):
    empty_tiles = [(i, j) for i in range(SIZE) for j in range(SIZE) if grid[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        grid[i][j] = 2 if random.random() < 0.9 else 4

def compress(grid):
    new_grid = [[0] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        pos = 0
        for j in range(SIZE):
            if grid[i][j] != 0:
                new_grid[i][pos] = grid[i][j]
                pos += 1
    return new_grid

def merge(grid):
    score = 0
    for i in range(SIZE):
        for j in range(SIZE - 1):
            if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                grid[i][j] *= 2
                score += grid[i][j]
                grid[i][j + 1] = 0
    return grid, score

def reverse(grid):
    new_grid = []
    for i in range(SIZE):
        new_grid.append(list(reversed(grid[i])))
    return new_grid

def transpose(grid):
    new_grid = []
    for i in range(SIZE):
        new_row = []
        for j in range(SIZE):
            new_row.append(grid[j][i])
        new_grid.append(new_row)
    return new_grid

def move_left(grid):
    new_grid = compress(grid)
    new_grid, score = merge(new_grid)
    new_grid = compress(new_grid)
    return new_grid, score

def move_right(grid):
    new_grid = reverse(grid)
    new_grid, score = move_left(new_grid)
    new_grid = reverse(new_grid)
    return new_grid, score

def move_up(grid):
    new_grid = transpose(grid)
    new_grid, score = move_left(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, score

def move_down(grid):
    new_grid = transpose(grid)
    new_grid, score = move_right(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, score

def is_game_over(grid):
    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i][j] == 0 or \
               (i < SIZE - 1 and grid[i][j] == grid[i + 1][j]) or \
               (j < SIZE - 1 and grid[i][j] == grid[i][j + 1]):
                return False
    return True

def main():
    grid = initialize_grid()
    score = 0

    running = True
    while running:
        draw_grid(grid, score)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_grid, new_score = move_left(grid)
                elif event.key == pygame.K_RIGHT:
                    new_grid, new_score = move_right(grid)
                elif event.key == pygame.K_UP:
                    new_grid, new_score = move_up(grid)
                elif event.key == pygame.K_DOWN:
                    new_grid, new_score = move_down(grid)
                else:
                    continue

                if new_grid != grid:
                    grid = new_grid
                    score += new_score
                    add_new_tile(grid)

                if is_game_over(grid):
                    draw_grid(grid, score)
                    pygame.display.update()
                    time.sleep(2)
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()
