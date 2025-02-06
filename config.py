import pygame # type: ignore

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

TOTAL_PLAYERS = 2

# Scale size for each game pixel
PIXEL_SIZE = 6
# Size of each game cell
SPACE_SIZE = 21
# Offset of the game board on the screen
GAME_BOARD_OFFSET = [500, 50]
# Size of the game board
GAME_BOARD_SIZE = (GRID_SPACES[0] * SPACE_SIZE * PIXEL_SIZE + (GRID_SPACES[0] + 1) * PIXEL_SIZE,
                   GRID_SPACES[1] * SPACE_SIZE * PIXEL_SIZE + (GRID_SPACES[1] + 1) * PIXEL_SIZE)

SCREEN_WIDTH = GAME_BOARD_SIZE[0] + GAME_BOARD_OFFSET[0] * 2
SCREEN_HEIGHT = GAME_BOARD_SIZE[1] + GAME_BOARD_OFFSET[1] * 2

# Colors:
CRT_WHITE = (213, 224, 216)       # CRT White
CRT_GREY  = (139, 143, 140)       # CRT Grey
CRT_BLACK = (24, 14, 26)          # CRT Black
BLACK = (0, 0, 0)                 # Sys black

s_QUEEN = []
s_DRONE = []
s_PAWN = []

def configure_images():
    
    # Get the individual images from the sprite sheet
    def get_image(sheet, frame_x, frame_y, width, height, scale, color):
        
        # Create a base square to place sprite image on top of
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame_x * width), (frame_y * height), width, height))
        
        # Transform the image
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        
        return image
    
    # Load the sprite sheets
    pyramid_sprite_sheet_image = pygame.image.load('sprites/pyramid.png').convert_alpha()

    for y in range(GRID_SPACES[1] * 2):
        s_QUEEN.append([get_image(pyramid_sprite_sheet_image, x, y, SPACE_SIZE, SPACE_SIZE, PIXEL_SIZE, BLACK) for x in range(4)])

    
    for y in range(GRID_SPACES[1] * 2):
        s_DRONE.append([get_image(pyramid_sprite_sheet_image, x + GRID_SPACES[0], y, SPACE_SIZE, SPACE_SIZE, PIXEL_SIZE, BLACK) for x in range(4)])

    
    for y in range(GRID_SPACES[1] * 2):
        s_PAWN.append([get_image(pyramid_sprite_sheet_image, x + GRID_SPACES[0] * 2, y, SPACE_SIZE, SPACE_SIZE, PIXEL_SIZE, BLACK) for x in range(4)])
