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

class Space():
    def __init__(self, world_position: tuple[int, int]):
        self.world_position = world_position
        self.grid_position = get_space(world_position)
        self.piece = None

class Game():
    def __init__(self):
        # Player 1 starts
        self.current_player = 1
        self.player_score_1 = 0
        self.player_score_2 = 0
        self.grid = []
        self.pieces = self.create_pieces()
        
        self.selected_piece = None
    
    def create_pieces(self) -> pygame.sprite.Group:
        
        pieces = pygame.sprite.Group()
    
        for row in range(len(GRID)):
            
            space_row = []
            
            for column, num in enumerate(GRID[row]):
                
                x = column * PIXEL_SIZE * SPACE_SIZE + (PIXEL_SIZE * SPACE_SIZE // 2) + column * PIXEL_SIZE
                y = row * PIXEL_SIZE * SPACE_SIZE + (PIXEL_SIZE * SPACE_SIZE // 2) + row * PIXEL_SIZE
                
                player = 1 if y < SCREEN_HEIGHT // 2 else 2
                
                new_space = Space((x, y))
                space_row.append(new_space)
                
                match num:
                    case 0:
                        piece = None
                    case 1:
                        piece = Queen(self, new_space, player)
                    case 2:
                        piece = Drone(self, new_space, player)
                    case 3:
                        piece = Pawn(self, new_space, player)
                    case _:
                        print("Grid has not been initialized correctly")
                        return None
                
                if piece != None:
                    pieces.add(piece)
                    new_space.piece = piece
                
            
            self.grid.append(space_row)
        
        return pieces
    
    def get_grid_space(self, loc: tuple[int, int]) -> Space | None:
        
        if loc[0] > GRID_SPACES[0] or loc[1] >= GRID_SPACES[1]:
            return None
        
        return self.grid[loc[0]][loc[1]]
    
    def select_space(self, loc: tuple[int, int]) -> None:
        
        space = self.get_grid_space(loc)
        
        if space.piece == None :
            if self.selected_piece:
                self.selected_piece.move_piece(space)
        
        elif space.piece._player == self.current_player:
            self.selected_piece = space.piece
            self.selected_piece.select()
            return
        elif self.selected_piece != None:
            self.selected_piece.move_piece(space)
        
        self.selected_piece = None
    
# Die abstract base class
class Piece(ABC, pygame.sprite.Sprite):
    
    def __init__(self, game: Game, space: Space, player: int):
        pygame.sprite.Sprite.__init__(self)
        self._game = game
        self._space = space
        self._player = player
        
        self.move_options = []
        self.move_lines = []
    
    @property
    def game(self) -> Game:
        return self._game
    
    @property
    def space(self) -> Space:
        return self._space
    
    @property
    def player(self) -> int:
        return self._player
    
    @property
    @abstractmethod
    def moves(self):
        pass
    
    def switch_player(self, player: int):
        self._player = player
        
    def select(self):
        self.get_movement_options()
        
    def move_piece(self, space: Space) -> None:
        
        self.select()
        
        if space not in self.move_options:
            return
        
        self.move_lines.clear()
        
        space.piece = self
        self._space.piece = None
        self._space = space
            
    def calculate_movement(self, move: tuple[int, int]) -> tuple[tuple[int, int]]:
        
        moves = []
        
        row, column = self.space.grid_position
        x, y = move
        
        move_distance = self.moves[1 + x][1 + y]
                
        step = 0 
        for _ in range(move_distance):
            
            x_movement = x * (step + 1)
            y_movement = y * (step + 1)
            
            if row + y_movement < 0 or row + y_movement >= GRID_SPACES[1] or\
                column + x_movement < 0 or column + x_movement >= GRID_SPACES[0]:
                    break
                
            obstacle = self.game.get_grid_space((row + y, column + x)).piece
            
            if obstacle == None:
                step += 1
                
                x_location = (step * x * PIXEL_SIZE * SPACE_SIZE) + self.space.world_position[0]
                y_location = (step * y * PIXEL_SIZE * SPACE_SIZE) + self.space.world_position[1]
                
                moves.append([x_location, y_location])
            
            elif obstacle._player != self._player:
                step += 1
        
                x_location = (step * x * PIXEL_SIZE * SPACE_SIZE) + self.space.world_position[0]
                y_location = (step * y * PIXEL_SIZE * SPACE_SIZE) + self.space.world_position[1]
                
                moves.append([x_location, y_location])
                
                break
            
            elif obstacle._player == self._player:
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
                    
                    self.move_options.append(space)
                    self.move_lines.append([self.rect.center, move])

class Pawn(Piece):
    def __init__(self, game: Game, spawn_space: Space, player: int):
        super().__init__(game, spawn_space, player)
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_PAWNS[random.randint(0, len(s_PAWNS) - 1)]
        self.rect = self.image.get_rect()
        self.rect.center = spawn_space.world_position
    
    def update(self):
        self.rect.center = self.space.world_position
    
    @property
    def moves(self):
        return [  [1, 0, 1],
                  [0, 0, 0],
                  [1, 0, 1]]

class Drone(Piece):
    def __init__(self, game: Game, spawn_space: Space, player: int):
        super().__init__(game, spawn_space, player)
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_DRONES[random.randint(0, len(s_DRONES) - 1)]
        self.rect = self.image.get_rect()
        self.rect.center = spawn_space.world_position
    
    def update(self):
        self.rect.center = self.space.world_position
        
    @property
    def moves(self):
        return [    [0, 2, 0],
                    [2, 0, 2],
                    [0, 2, 0]]

class Queen(Piece):
    def __init__(self, game: Game, spawn_space: Space, player: int):
        super().__init__(game, spawn_space, player)
        
        pygame.sprite.Sprite.__init__(self)
        self.image = s_QUEENS[random.randint(0, len(s_QUEENS) - 1)]
        self.rect = self.image.get_rect()
        self.rect.center = spawn_space.world_position
    
    def update(self):
        self.rect.center = self.space.world_position
        
    @property
    def moves(self):
        min_diag_dist = min(GRID_SPACES[0], GRID_SPACES[1]) 
        
        return [    [min_diag_dist, GRID_SPACES[1], min_diag_dist],
                    [GRID_SPACES[0], 0, GRID_SPACES[0]],
                    [min_diag_dist, GRID_SPACES[1], min_diag_dist]]
        
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
    
    game.pieces.update()
    
    game.pieces.draw(screen)
    
    if game.selected_piece != None:
        for line in game.selected_piece.move_lines:
            pygame.draw.line(screen, CRT_WHITE, line[0], line[1], width=10)
    
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
                loc = get_space(pos)
                game.select_space(loc)

        # Quit the game
        if event.type == pygame.QUIT:
            run = False
    
    # Update the game display
    pygame.display.update()

pygame.quit()