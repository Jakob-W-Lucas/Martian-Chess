from abc import ABC, abstractmethod
from config import *
import pygame # type: ignore
from pieces import Queen, Drone, Pawn
from utils import get_space, get_player, create_captured_piece, get_winner

class Space():
    def __init__(self, world_position: tuple[int, int]):
        self.world_position = world_position
        self.grid_position = get_space(world_position)
        self.piece = None
        
class Game():
    def __init__(self):
        # Player 1 starts
        self.current_player = 0
        self.player_scores = [0 for _ in range(TOTAL_PLAYERS)]
        self.captures = [pygame.sprite.Group() for _ in range(TOTAL_PLAYERS)]
        self.grid = []
        self.pieces = self.create_pieces()
        
        self.selected_piece = None
        self.last_selected_piece = None
        
        self.game_over = False
    
    def create_pieces(self) -> pygame.sprite.Group:
        
        pieces = [pygame.sprite.Group() for _ in range(TOTAL_PLAYERS)]
    
        for row in range(len(GRID)):
            
            space_row = []
            
            for column, num in enumerate(GRID[row]):
                
                x = column * PIXEL_SIZE * SPACE_SIZE + (PIXEL_SIZE * SPACE_SIZE // 2) + column * PIXEL_SIZE + GAME_BOARD_OFFSET[0]
                y = row * PIXEL_SIZE * SPACE_SIZE + (PIXEL_SIZE * SPACE_SIZE // 2) + row * PIXEL_SIZE + GAME_BOARD_OFFSET[1]
                
                player = get_player(y)
                
                new_space = Space((x, y))
                space_row.append(new_space)
                
                piece = self.create_piece(num, new_space, player)
                
                if piece:
                    pieces[player].add(piece)
                    new_space.piece = piece
            
            self.grid.append(space_row)
        
        return pieces
    
    def create_piece(self, num: int, space: Space, player: int):
        if num == 1:
            return Queen(self, space, player)
        elif num == 2:
            return Drone(self, space, player)
        elif num == 3:
            return Pawn(self, space, player)
        return None
    
    def capture(self, player: int, piece):
        self.captures[player].add(piece)
        self.player_scores[player] += piece._value
        create_captured_piece(piece, player, len(self.captures[player]) - 1)
        
        print(self.player_scores)
    
    def get_grid_space(self, loc: tuple[int, int]) -> Space | None:
        
        if loc[0] > GRID_SPACES[1] or loc[1] >= GRID_SPACES[0]:
            print(f"Grid space {loc} is outside of range")
            return None
        
        return self.grid[loc[0]][loc[1]]
    
    def select_space(self, loc: tuple[int, int]) -> None:
        
        space = self.get_grid_space(loc)
        
        if space == None:
            print(f"The position {loc} has no space")
            return
        
        if space.piece == None :
            if self.selected_piece:
                self.selected_piece.move_piece(space)
        elif space.piece._player == self.current_player:
            
            self.selected_piece = space.piece
            self.selected_piece.select()
            return
        elif self.selected_piece != None:
            self.selected_piece.capture_piece(space)
        
        self.last_selected_piece = self.selected_piece
        self.selected_piece = None
        
        if self.last_selected_piece:
            get_winner(self.pieces, self.player_scores, self.last_selected_piece.player)
        
    def draw(self, screen):
        if self.selected_piece is not None:
            for line in self.selected_piece.move_lines:
                pygame.draw.line(screen, CRT_WHITE, line[0], line[1], width=LINE_WIDTH)
        
        for player in range(TOTAL_PLAYERS):
            self.pieces[player].update()
            self.pieces[player].draw(screen)
            self.captures[player].draw(screen)
    
# Die abstract base class
class Piece(ABC, pygame.sprite.Sprite):
    
    def __init__(self, game: Game, space: Space, value: int, player: int):
        pygame.sprite.Sprite.__init__(self)
        self._game = game
        self._space = space
        self._value = value
        self._player = player
        
        self.move_options = []
        self.move_lines = []
        
        self.switched_from_position = None
    
    @property
    def game(self) -> Game:
        return self._game
    
    @property
    def space(self) -> Space:
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
        
    def move_piece(self, space: Space) -> None:
        
        self.select()
        
        if space not in self.move_options:
            return
        
        old_player = self.player
        self._player = get_player(space.world_position[1])
        
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
    
    def capture_piece(self, space: Space) -> None:
        
        if space not in self.move_options:
            return
        
        self.game.capture(self.player, space.piece)
        
        self.game.pieces[space.piece._player].remove(space.piece)
        
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