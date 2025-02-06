from config import *
from utils import get_space
import pygame # type: ignore
from game import Game

pygame.init()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Martian Chess')
    
    configure_images()
    # Game state
    run = True
    game = Game()

    # Mouse buttons
    m_LEFT = 1

    # Game loop
    while run:
            
        # Create the screen background
        screen.fill(CRT_BLACK)
        
        game.pieces.update()
        
        game.pieces.draw(screen)
        
        if game.selected_piece != None:
            for line in game.selected_piece.move_lines:
                pygame.draw.line(screen, CRT_WHITE, line[0], line[1], width=10)
        
        for player in range(TOTAL_PLAYERS):
            game.captures[player].draw(screen)
                
        
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
                    
                    if loc:
                        game.select_space(loc)

            # Quit the game
            if event.type == pygame.QUIT:
                run = False
        
        # Update the game display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()