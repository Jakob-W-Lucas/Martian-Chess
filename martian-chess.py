import pygame # type: ignore
import random

pygame.init()

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 1092

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Martian Chess')

GRID_SPACES = [4, 8]
# Scale size for each game pixel
pixel_size = 6

# Colors:
CRT_WHITE = (213, 224, 216)       # White
CRT_GREY  = (139, 143, 140)       # Grey
CRT_BLACK = (24, 14, 26)          # CRT Black
BLACK = (0, 0, 0)

# Load the sprite sheets
die_sprite_sheet_image = pygame.image.load('sprites/die.png').convert_alpha()

# Get the individual images from the sprite sheet
def get_image(sheet, frame_x, frame_y, width, height, scale, color):
    
    # Create a base square to place sprite image on top of
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame_x * width), (frame_y * height), width, height))
    
    # Transform the image
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    
    return image

# Images:
s_PAWNS = [get_image(die_sprite_sheet_image, x, 0, 23, 23, pixel_size, BLACK) for x in range(6)]
s_DRONES = [get_image(die_sprite_sheet_image, x, 1, 23, 23, pixel_size, BLACK) for x in range(4)]
s_QUEENS = [get_image(die_sprite_sheet_image, x, 2, 23, 23, pixel_size, BLACK) for x in range(4)]

class Die():
    
    def __init__(self):
        self.moves = []

    def click(self) -> None:
        self.display_moves()

    def display_moves(self) -> None:
        pass
    
    def place(self, column: int, row: int) -> None:
        pass
    
    def capture(self) -> None:
        pass

class Pawn(Die):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_PAWNS[random.randint(0, len(s_PAWNS))]
        self.rect = self.image.get_rect()
        self.rect.center = spawn
        
        self.moves = [  [1, 0, 1],
                        [0, 0, 0],
                        [1, 0, 1]]

class Drone(Die):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_DRONES[random.randint(0, len(s_DRONES))]
        self.rect = self.image.get_rect()
        self.rect.center = spawn
        
        self.moves = [  [0, GRID_SPACES[1], 0],
                        [GRID_SPACES[0], 0, GRID_SPACES[0]],
                        [0, GRID_SPACES[1], 0]]

class Queen(Die):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_QUEENS[random.randint(0, len(s_QUEENS))]
        self.rect = self.image.get_rect()
        self.rect.center = spawn
        
        max_diag_dist = max(GRID_SPACES[0], GRID_SPACES[1]) 
        self.moves = [  [max_diag_dist, GRID_SPACES[1], max_diag_dist],
                        [GRID_SPACES[0], 0, GRID_SPACES[0]],
                        [max_diag_dist, GRID_SPACES[1], max_diag_dist]]
        
# Game state
run = True
game = None

# Game loop
while run:
        
    # Create the screen background
    screen.fill(CRT_BLACK)
    
    # Get key presses
    key = pygame.key.get_pressed()
        
    # Exit
    if key[pygame.K_ESCAPE]:
       run = False
       
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Mouse position
            pos = pygame.mouse.get_pos()

        # Quit the game
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()