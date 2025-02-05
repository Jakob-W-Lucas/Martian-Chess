from config import SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_SIZE, GRID_SPACES
import pygame # type: ignore

def in_sprite_area(pos: tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
    
    x_center, y_center = sprite.rect.center
    
    width = (sprite.width * PIXEL_SIZE // 2)
    height = (sprite.height * PIXEL_SIZE // 2)
    
    if pos[0] < x_center - width or pos[0] > x_center + width or\
        pos[1] < y_center - height or pos[1] > y_center + height:
            return False

    return True

def get_space(pos: tuple[int, int]) -> tuple[int, int] | None:
    
    x_dist = SCREEN_WIDTH // GRID_SPACES[0]
    y_dist = SCREEN_HEIGHT // GRID_SPACES[1]
    
    column  = pos[0] // x_dist
    row     = pos[1] // y_dist
    
    if row < 0 or row >= GRID_SPACES[1] or\
        column < 0 or column >= GRID_SPACES[0]:
            return None
        
    return [row, column]