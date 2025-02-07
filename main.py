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
            
        screen.fill(CRT_BLACK)
        
        game.draw(screen)
        
        key = pygame.key.get_pressed()
            
        if key[pygame.K_ESCAPE]:
            run = False
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                pos = pygame.mouse.get_pos()
                
                if event.button == m_LEFT:
                    loc = get_space(pos)
                    
                    if loc:
                        game.select_space(loc)

            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()