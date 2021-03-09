import pygame
import engine

# pygame colours
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
YELLOW = (255,255, 0)
ORANGE = (255, 69 ,0)
GREY  = ( 30, 30, 30)


# screen dimensions
WIDTH = HEIGHT = 900

# resolution/square width and height
res = WIDTH // 3

# setting up display screen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
FPS = 60

# getting grid class
grid = engine.grid(win)

running = True

while running:
    over = grid.game_over()
    if over != None:
        print("Its a TIE!") if over == 'tie' else print(f"{over.title()} WON!")
        break
    if not grid.crossToGo:
        grid.make_best_move()
    
    win.fill(BLACK)
    clock.tick(FPS)
    for event in pygame.event.get():
        # user clicks the x
        if event.type == pygame.QUIT:
            running = False
        # user clicks the
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if 0 <= pos[0] <= WIDTH and 0 <= pos[1] <= HEIGHT and grid.crossToGo:
                if grid.click_in_box(pos):
                    # changes turn
                    grid.crossToGo = not grid.crossToGo
    
    grid.draw()
    pygame.display.update()
#pygame.quit()
