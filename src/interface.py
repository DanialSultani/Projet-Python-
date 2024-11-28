import pygame
import random
from unit import *
from case import *

# Constantes pour l'adaptation dynamique
CELL_SIZE = 50
GRID_SIZE = 16  # Nombre de cellules par dimension
WIDTH = (GRID_SIZE * CELL_SIZE)+600
HEIGHT = GRID_SIZE * CELL_SIZE


# Couleur 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
BLUE= (0, 0, 255, 255)
FPS = 30



class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Unit(1, 3, 10, 2, 'player','soldat'),
                             Unit(1, 4, 10, 2, 'player','medecin'),
                             Unit(1, 1, 10, 2, 'player','helico')]

        self.enemy_units = [Unit(20, 9, 8, 1, 'enemy','char'),
                            Unit(20, 11, 10, 2, 'enemy','medecin'),
                            Unit(20, 13, 8, 1, 'enemy','soldat')]
        
        # Liste des maps avec un terrain spécifique
        self.maps = [
            { # Map 1
                "terrain": "images/terrain_herbe.png",  # Terrain de la map
                "cases": [  # Cases spécifiques de la map
                    Case(10, 9, 'boue'), Case(4, 5, 'boue'),
                    Case(19, 14, 'roche'), Case(0, 1, 'roche'),
                    Case(10, 10, 'buisson'), Case(17, 10, 'buisson'),
                    Case(3, 3, 'puit'), Case(17, 13, 'puit'),
                    Case(0, 3, 'flag1'), Case(21, 13, 'flag2'), # Drapeau 
                    Case(22, 1, 'arbre'), Case(21, 1, 'arbre'),Case(20, 1, 'arbre'), Case(19, 2, 'arbre'),Case(18, 1, 'arbre'),Case(22, 3, 'arbre'),Case(21, 2, 'arbre'),Case(20, 3, 'arbre'),Case(15, 5, 'arbre'),Case(10, 8, 'arbre'),Case(2, 12, 'arbre'),
                    Case(0, 12, 'arbre'), Case(-1, 12, 'arbre'), Case(2, 13, 'arbre'),Case(2, 13, 'arbre'),Case(0, 13, 'arbre'),Case(1, 14, 'arbre'),Case(-1, 14, 'arbre'),Case(3, 14, 'arbre') # Arbre 
 # Arbre 
                ]
            },
            { # Map 2
                "terrain": "images/terrain_sables.png",
                "cases": [
                    Case(0, 0, 'dune'), Case(3, 0, 'dune'), Case(6, 0, 'dune'), Case(9, 0, 'dune'),Case(12, 0, 'dune'),Case(15, 0, 'dune'),Case(17, 0, 'dune'),Case(20, 0, 'dune'),Case(23, 0, 'dune'),Case(25, 0, 'dune'),
                    Case(2, 1, 'flag1'), Case(14, 10, 'flag2'),
                    Case(3, 9, 'dune2'), Case(3, 8, 'dune2'),Case(10, 3, 'dune2'), Case(10, 4, 'dune2'),
                    Case(13, 13, 'palmier'), Case(8, 8, 'palmier')
                ]
            }
            ,
            { # Map 3
                "terrain": "images/terrain_neige.png",
                "cases": [
                    Case(6, 6, 'mur'), Case(7, 6, 'mur'),
                    Case(0, 7, 'flag1'), Case(15, 7, 'flag2'),
                    Case(5, 5, 'buisson'), Case(4, 4, 'arbre')
                ]
            }
        ]

        # Sélection d'une map aléatoire
        self.current_map = self.maps[0]

    def draw_map(self):
        """Affiche les cases spécifiques de la map actuelle."""
        for case in self.current_map["cases"]:
            case.draw(self.screen )
            
            

    def flip_display(self):
        """Affiche le jeu uniquement sur la surface dédiée (game_surface)."""

        # Dimensions de la fenêtre et de la surface de jeu
        game_width = int(WIDTH * 0.85)  # 3/4 de la largeur
        game_height = HEIGHT
        game_surface = pygame.Surface((game_width, game_height))  # Crée une surface pour le jeu

        # Charger et afficher le terrain de la map sur la surface de jeu
        try:
            terrain_image = pygame.image.load(self.current_map["terrain"])
            terrain_image = pygame.transform.scale(terrain_image, (CELL_SIZE, CELL_SIZE))  # Adapter la taille à une cellule
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image du terrain : {e}")
            pygame.quit()
            exit()

        # Dessiner le terrain sur toute la grille (dans la surface de jeu)
        for x in range(0, game_width, CELL_SIZE):
            for y in range(0, game_height, CELL_SIZE):
                game_surface.blit(terrain_image, (x, y))

        # Charger et Dessiner le ciel  (dans la surface de jeu)
        try:
            ciel= pygame.image.load("images/ciel.jpg")
            ciel= pygame.transform.scale(ciel, (2*CELL_SIZE, CELL_SIZE))  # Adapter la taille à une cellule
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image du terrain : {e}")
            pygame.quit()
            exit()
        for x in range(0, game_width, CELL_SIZE):
            game_surface.blit(ciel, (2*x, 0))

        # Afficher les cases spécifiques de la map
        for case in self.current_map["cases"]:
            case.draw(game_surface)

        # Afficher les unités sur la surface de jeu
        for unit in self.player_units + self.enemy_units:
            unit.draw(game_surface)

        # Blitter la surface de jeu (game_surface) sur la fenêtre principale (screen)
        self.screen.blit(game_surface, (0, 0))

        # Dessiner le panneau latéral (1/4 de la fenêtre) pour les options, pouvoirs, etc.
        sidebar_width = WIDTH - game_width  # 1/4 de la largeur
        sidebar_surface = pygame.Surface((sidebar_width, HEIGHT))
        sidebar_surface.fill((30, 30, 30))  # Fond sombre pour le panneau

        # Afficher des exemples de texte ou icônes sur le panneau latéral
        font = pygame.font.SysFont("Arial", 20)
        text = font.render("Options de jeu :", True, (255, 255, 255))
        sidebar_surface.blit(text, (10, 10))

        # Blitter la surface du panneau latéral sur la fenêtre principale
        self.screen.blit(sidebar_surface, (game_width, 0))

        # Rafraîchir l'affichage complet
        pygame.display.flip()