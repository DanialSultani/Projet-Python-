import pygame
from sons import *

# Constantes pour l'adaptation dynamique
CELL_SIZE = 50
GRID_SIZE = 16  # Nombre de cellules par dimension
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
WIDTH = 1400
HEIGHT = 800

  

FPS = 30
def show_victory_screen(screen, winner):
    # Polices
    font = pygame.font.Font("images/GameBoy.ttf", 50)
    sound= SoundEffect()
    sound.play('victoir') #ajout du son

    # Dessiner la fresque comme fond
    back = pygame.image.load("images/back.png")
    back= pygame.transform.scale(back, (WIDTH, HEIGHT))
    screen.blit(back, (0, 0))

    if winner == "draw":
        message = "Match nul !"
    else:
        message = f"Victoire du {'Joueur 1' if winner == 'player1' else 'Joueur 2'} !"
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    small_font = pygame.font.Font("images/GameBoy.ttf", 36)
    instruction = "Appuyez sur Enter pour rejouer."
    instruction_surface = small_font.render(instruction, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(instruction_surface, instruction_rect)
    
    pygame.display.flip()

    # Attendre l'entrée utilisateur
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return False