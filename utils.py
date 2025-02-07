from config import *
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
    
    x_dist = GAME_BOARD_SIZE[0] // GRID_SPACES[0]
    y_dist = GAME_BOARD_SIZE[1] // GRID_SPACES[1]
    
    column  = (pos[0] - GAME_BOARD_OFFSET[0]) // x_dist
    row     = (pos[1] - GAME_BOARD_OFFSET[1]) // y_dist
    
    if row < 0 or row >= GRID_SPACES[1] or\
        column < 0 or column >= GRID_SPACES[0]:
            return None
        
    return [row, column]

def get_player(y: int) -> int:
   return int(y > GAME_BOARD_SIZE[1] // 2 + GAME_BOARD_OFFSET[1])

def get_winner(pieces: tuple, scores: tuple, last_player: int):
    
    win_condition = False
    for player in range(TOTAL_PLAYERS):
        if len(pieces[player]) == 0:
            win_condition = True
            
    if not win_condition:
        return
                
    winner = -1
    highest = -1
    for player, score in enumerate(scores):
        if score == highest:
            winner = last_player
        elif score > highest:
            winner = player
            highest = score
    
    print(f"Player {winner} has won!")