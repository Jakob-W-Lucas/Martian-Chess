from abc import ABC, abstractmethod
import pygame # type: ignore
import random

pygame.init()

GRID = [    [1, 1, 2, 0],
            [1, 2, 3, 0],
            [2, 3, 3, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 3, 3, 2],
            [0, 3, 2, 1],
            [0, 2, 1, 1]]

GRID_SPACES = [len(GRID[0]), len(GRID)]

# Scale size for each game pixel
PIXEL_SIZE = 6
# Size of each game cell
SPACE_SIZE = 21

SCREEN_WIDTH = GRID_SPACES[0] * SPACE_SIZE * PIXEL_SIZE + (GRID_SPACES[0] + 1) * PIXEL_SIZE
SCREEN_HEIGHT = GRID_SPACES[1] * SPACE_SIZE * PIXEL_SIZE + (GRID_SPACES[1] + 1) * PIXEL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Martian Chess')

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
s_PAWNS  = [get_image(die_sprite_sheet_image, x, 0, SPACE_SIZE, SPACE_SIZE, PIXEL_SIZE, BLACK) for x in range(6)]
s_DRONES = [get_image(die_sprite_sheet_image, x, 1, SPACE_SIZE, SPACE_SIZE, PIXEL_SIZE, BLACK) for x in range(4)]
s_QUEENS = [get_image(die_sprite_sheet_image, x, 2, SPACE_SIZE, SPACE_SIZE, PIXEL_SIZE, BLACK) for x in range(6)]

# Die abstract base class
class Die(ABC, pygame.sprite.Sprite):
    
    def __init__(self):
        pass

    def click(self) -> None:
        self.display_moves()

    def display_moves(self) -> None:
        pass
    
    def place(self, column: int, row: int) -> None:
        pass
    
    def capture(self) -> None:
        pass
    
    @property
    @abstractmethod
    def moves(self):
        pass


class Pawn(Die):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_PAWNS[random.randint(0, len(s_PAWNS) - 1)]
        self.rect = self.image.get_rect()
        self.rect.center = spawn
    
    @property
    def moves(self):
        return [  [1, 0, 1],
                  [0, 0, 0],
                  [1, 0, 1]]

class Drone(Die):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_DRONES[random.randint(0, len(s_DRONES) - 1)]
        self.rect = self.image.get_rect()
        self.rect.center = spawn
        
    @property
    def moves(self):
        return [    [0, 2, 0],
                    [2, 0, 2],
                    [0, 2, 0]]

class Queen(Die):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_QUEENS[random.randint(0, len(s_QUEENS) - 1)]
        self.rect = self.image.get_rect()
        self.rect.center = spawn
        
    @property
    def moves(self):
        min_diag_dist = min(GRID_SPACES[0], GRID_SPACES[1]) 
        
        return [    [min_diag_dist, GRID_SPACES[1], min_diag_dist],
                    [GRID_SPACES[0], 0, GRID_SPACES[0]],
                    [min_diag_dist, GRID_SPACES[1], min_diag_dist]]

class Game():
    def __init__(self):
        self.player_score_1 = 0
        self.player_score_2 = 0
        self.grid = [[] for _ in range(len(GRID))]
        self.pieces = self.create_pieces()
        
    def create_pieces(self) -> pygame.sprite.Group:
        
        pieces = pygame.sprite.Group()
    
        for row in range(len(GRID)):
            for column, num in enumerate(GRID[row]):
                
                x = column * PIXEL_SIZE * SPACE_SIZE + (PIXEL_SIZE * SPACE_SIZE // 2) + column * PIXEL_SIZE
                y = row * PIXEL_SIZE * SPACE_SIZE + (PIXEL_SIZE * SPACE_SIZE // 2) + row * PIXEL_SIZE
                
                match num:
                    case 0:
                        piece = None
                    case 1:
                        piece = Queen((x, y))
                        pieces.add(piece)
                    case 2:
                        piece = Drone((x, y))
                        pieces.add(piece)
                    case 3:
                        piece = Pawn((x, y))
                        pieces.add(piece)
                    case _:
                        print("Grid has not been initialized correctly")
                        return None
                
                self.grid[row].append(piece)
        
        return pieces
    
    def get_space(self, loc: tuple[int, int]) -> Die:
        return self.grid[loc[1]][loc[0]]

def get_space(pos: tuple[int]) -> tuple[int, int]:
    
    x, y = pos
    
    row = x // SPACE_SIZE
    column = y // SPACE_SIZE
    
    # Return nothing if coords are outside bounds
    if row >= GRID_SPACES[0] or column >= GRID_SPACES[1] or\
        row < 0 or column < 0:
        return None
    
    return [row, column]

def in_sprite_area(pos: tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
    
    x_center, y_center = sprite.rect.center
    
    width = (sprite.width * PIXEL_SIZE // 2)
    height = (sprite.height * PIXEL_SIZE // 2)
    
    if pos[0] < x_center - width or pos[0] > x_center + width or\
        pos[1] < y_center - height or pos[1] > y_center + height:
            return False

    return True

def get_clicked_space(pos: tuple[int, int]) -> tuple[int, int] | None:
    
    x_dist = SCREEN_WIDTH // GRID_SPACES[0]
    y_dist = SCREEN_HEIGHT // GRID_SPACES[1]
    
    row     = pos[0] // x_dist
    column  = pos[1] // y_dist
    
    if row < 0 or row >= GRID_SPACES[0] or\
        column < 0 or column >= GRID_SPACES[1]:
            return None
        
    return [row, column]

# Game state
run = True
game = None

# Mouse buttons
m_LEFT = 1

# Game loop
while run:
        
    # Create the screen background
    screen.fill(CRT_BLACK)
    
    if game == None:
        game = Game()
            
    game.pieces.draw(screen)
    
    # Get key presses
    key = pygame.key.get_pressed()
        
    # Exit
    if key[pygame.K_ESCAPE]:
       run = False
       
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Mouse position
            pos = pygame.mouse.get_pos()
            
            # Left click to mine cells
            if event.button == m_LEFT:
                loc = get_clicked_space(pos)
                print(f"The space: {loc} has piece: {game.get_space(loc)}")

        # Quit the game
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()