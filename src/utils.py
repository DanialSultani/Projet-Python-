import pygame

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
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    if winner == "draw":
        message = "Match nul !"
    else:
        message = f"Victoire de l'équipe {'Joueur' if winner == 'player' else 'Adverse'} !"
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    small_font = pygame.font.Font(None, 36)
    instruction = "Appuyez sur [Entrée] pour retourner au menu principal."
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
                if event.key == pygame.K_RETURN:  # Retour au menu principal
                    return
