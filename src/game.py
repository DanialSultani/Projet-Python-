import pygame
from random import *
from unit import *
from case import *
from interface import *


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flags of Glory")
    
    # Charger les fresque
    try:
        fresque = pygame.image.load("Projet-Python-/images/fresque_1.png")
        fresque = pygame.transform.scale(fresque, (0.95*WIDTH,HEIGHT))  
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        return

    # Afficher la fresque
    screen.blit(fresque, (0, 0))
    pygame.display.flip()

    # Attendre qu'une touche soit pressée
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

   
    # Instanciation du jeu
    game = Game(screen)

   # Boucle principale
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()