import pygame

# Constantes pour l'adaptation dynamique
CELL_SIZE = 50
GRID_SIZE = 16  # Nombre de cellules par dimension
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
WIDTH = 1400
HEIGHT = 800

FPS = 60

def show_victory_screen(screen, winner):
    """
    Affiche un écran de victoire pour l'équipe gagnante.

    Paramètres
    ----------
    screen : pygame.Surface
        La surface sur laquelle afficher l'écran de victoire.
    winner : str
        Le gagnant ('player' ou 'enemy').
    """
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = f"Victoire de l'équipe {'Joueur' if winner == 'player' else 'Adverse'} !"
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # Attendre que l'utilisateur ferme l'écran ou appuie sur une touche
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False