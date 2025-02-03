import pygame # type: ignore

# Scale size for each game pixel
pixel_size = 10

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
s_PAWNS = [get_image(die_sprite_sheet_image, x * 23, 0, 23, 23, pixel_size, BLACK) for x in range(6)]
s_DRONES = [get_image(die_sprite_sheet_image, x * 23, 23, 23, 23, pixel_size, BLACK) for x in range(4)]
s_QUEENS = [get_image(die_sprite_sheet_image, x * 23, 46, 23, 23, pixel_size, BLACK) for x in range(4)]

