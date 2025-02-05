from config import *
import pygame # type: ignore
from abc import ABC, abstractmethod
from utils import get_space

class Piece(ABC, pygame.sprite.Sprite):
    
    def __init__(self, game, space, value: int, player: int):
        pygame.sprite.Sprite.__init__(self)
        self._game = game
        self._space = space
        self._value = value
        self._player = player
        
        self.move_options = []
        self.move_lines = []
        
        self.switched_from_position = None
    
    @property
    def game(self):
        return self._game
    
    @property
    def space(self):
        return self._space
    
    @property
    def value(self) -> int:
        return self._value
    
    @property
    def player(self) -> int:
        return self._player

    @abstractmethod
    def get_image(self):
        pass
    
    @property
    @abstractmethod
    def moves(self):
        pass
        
    def select(self):
        self.get_movement_options()
        
    def move_piece(self, space) -> None:
        
        self.select()
        
        if space not in self.move_options:
            return
        
        old_player = self.player
        self._player = int(space.world_position[1] > SCREEN_HEIGHT // 2)
        
        if old_player != self.player:
            self.switched_from_position = self.space.grid_position
        else:
            self.switched_space = None
        
        self.move_lines.clear()
        
        space.piece = self
        self._space.piece = None
        self._space = space
        self.get_image()
        
        self.game.current_player = (self.game.current_player + 1) % TOTAL_PLAYERS
    
    def capture_piece(self, space) -> None:
        
        if space not in self.move_options:
            return
        
        self.game.capture(self.player, space.piece)
        
        self.game.pieces.remove(space.piece)
        
        space.piece = None
        
        self.move_piece(space)
            
    def calculate_movement(self, move: tuple[int, int]) -> tuple[tuple[int, int]]:
        
        moves = []
        
        row, column = self.space.grid_position
        x, y = move
        
        move_distance = self.moves[1 + y][1 + x]
                
        step = 0 
        for _ in range(move_distance):
            
            x_movement = x * (step + 1)
            y_movement = y * (step + 1)
            
            if row + y_movement < 0 or row + y_movement >= GRID_SPACES[1] or\
                column + x_movement < 0 or column + x_movement >= GRID_SPACES[0]:
                    break
                
            obstacle = self.game.get_grid_space((row + y_movement, column + x_movement)).piece
            
            if obstacle is None or obstacle._player != self._player:
                step += 1
                
                x_location = (step * x * PIXEL_SIZE * SPACE_SIZE) + self.space.world_position[0]
                y_location = (step * y * PIXEL_SIZE * SPACE_SIZE) + self.space.world_position[1]
                
                moves.append((x_location, y_location))
                
                if obstacle is not None:
                    break
            else:
                break
        
        return moves
    
    def get_movement_options(self) -> None:
        
        self.move_lines.clear()
        self.move_options.clear()
        
        for x in range(-1, 2):
            for y in range(-1 ,2):
                movement = self.calculate_movement((x, y))
                
                for move in movement:
                    
                    space = self.game.get_grid_space(get_space(move))
                    
                    if space.grid_position == self.switched_from_position and self == self.game.last_selected_piece:
                        continue
                        
                    self.move_options.append(space)
                    self.move_lines.append([self.rect.center, move])

class Pawn(Piece):
    def __init__(self, game, spawn_space, player: int):
        super().__init__(game, spawn_space, 1, player)
        
        pygame.sprite.Sprite.__init__(self)
        
        self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = spawn_space.world_position
    
    def get_image(self) -> None:
        column, row = self._space.grid_position
        self.image = s_PAWN[column + GRID_SPACES[1] * self._player][row]
    
    def update(self):
        self.rect.center = self.space.world_position
    
    @property
    def moves(self):
        return [  [1, 0, 1],
                  [0, 0, 0],
                  [1, 0, 1]]

class Drone(Piece):
    def __init__(self, game, spawn_space, player: int):
        super().__init__(game, spawn_space, 2, player)
        
        pygame.sprite.Sprite.__init__(self)
        
        self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = spawn_space.world_position
    
    
    def get_image(self) -> None:
        column, row = self._space.grid_position
        self.image = s_DRONE[column + GRID_SPACES[1] * self._player][row]
    
    def update(self):
        self.rect.center = self.space.world_position
        
    @property
    def moves(self):
        return [    [0, 2, 0],
                    [2, 0, 2],
                    [0, 2, 0]]

class Queen(Piece):
    def __init__(self, game, spawn_space, player: int):
        super().__init__(game, spawn_space, 3, player)
        
        pygame.sprite.Sprite.__init__(self)
        
        self.get_image()
        self.rect = self.image.get_rect()
        self.rect.center = spawn_space.world_position
        
    def get_image(self) -> None:
        column, row = self._space.grid_position
        self.image = s_QUEEN[column + GRID_SPACES[1] * self._player][row]
    
    def update(self):
        self.rect.center = self.space.world_position
        
    @property
    def moves(self):
        min_diag_dist = min(GRID_SPACES[0], GRID_SPACES[1]) 
        
        return [    [min_diag_dist, GRID_SPACES[1], min_diag_dist],
                    [GRID_SPACES[0], 0, GRID_SPACES[0]],
                    [min_diag_dist, GRID_SPACES[1], min_diag_dist]]