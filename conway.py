import pygame
import sys

pygame.init() # initialize it
width, height = 1000, 1000 
square_size = 20  
black = (0, 0, 0)
white = (255, 255, 255)
line_color = (50, 50, 50)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("conway's game of life")
grid = [[0 for _ in range(100)] for _ in range(100)]
drawing = False  
drawing_enabled = True  
auto_update = False 

def count_neighbours(grid, row, col):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 100 and 0 <= nc < 100 and grid[nr][nc] == 1:
            count += 1
    return count

def update_grid(grid):
    new_positions = set()
    all_neighbours = set()
    
    # collect relevant positions
    for row in range(100):
        for col in range(100):
            if grid[row][col] == 1:
                all_neighbours.add((row, col))
                # ddd all neighboring cells to the set
                for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < 100 and 0 <= nc < 100:
                        all_neighbours.add((nr, nc))

    # create a copy of the grid to avoid modifying while iterating
    new_grid = [[0 for _ in range(100)] for _ in range(100)]
    
    # apply rules
    for row, col in all_neighbours:
        neighbours = count_neighbours(grid, row, col)
        if grid[row][col] == 1:  # if cell is alive
            if 2 <= neighbours <= 3:
                new_grid[row][col] = 1
                new_positions.add((row, col))
        else:  
            if neighbours == 3:
                new_grid[row][col] = 1
                new_positions.add((row, col))
    
    return new_grid, new_positions

# main game loop
clock = pygame.time.Clock()
fps = 30  
running = True
while running:
    clock.tick(fps) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled:
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:  # start game
                drawing_enabled = False
                auto_update = True

    if auto_update:
        grid, new_positions = update_grid(grid)

    if drawing and drawing_enabled:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // square_size
        grid_y = mouse_y // square_size
        if 0 <= grid_x < 100 and 0 <= grid_y < 100:
            grid[grid_y][grid_x] = 1

    screen.fill(black)
    
    for row in range(100):
        for col in range(100):
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            if grid[row][col] == 1:
                pygame.draw.rect(screen, white, rect)
            else:
                pygame.draw.rect(screen, black, rect, 1)
            pygame.draw.rect(scree, line_color, rect, 1) # grid lines
    
    pygame.display.flip()

pygame.quit()
sys.exit()
