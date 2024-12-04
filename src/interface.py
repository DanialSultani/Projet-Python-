import pygame
import random
from unit import *
from case import *

# Constantes pour l'adaptation dynamique
CELL_SIZE = 50
GRID_SIZE = 16  # Nombre de cellules par dimension



# Couleur 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
BLUE= (0, 0, 255, 255)
FPS = 60



class Game :
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
                    Case(22, 1, 'arbre'), Case(20, 1, 'arbre'), Case(19, 2, 'arbre'),Case(18, 1, 'arbre'),Case(22, 3, 'arbre'),Case(21, 2, 'arbre'),Case(20, 3, 'arbre'),Case(22, 4, 'arbre'),Case(15, 5, 'arbre'),Case(10, 8, 'arbre'),Case(2, 12, 'arbre'),
                    Case(0, 12, 'arbre'), Case(-1, 12, 'arbre'), Case(2, 13, 'arbre'),Case(2, 13, 'arbre'),Case(0, 13, 'arbre'),Case(1, 14, 'arbre'),Case(-1, 14, 'arbre'),Case(3, 14, 'arbre') # Arbre 
 # Arbre 
                ]
            },
            { # Map 2
                "terrain": "images/terrain_sables.png",
                "cases": [
                    Case(0, 0, 'dune'), Case(3, 0, 'dune'), Case(6, 0, 'dune'), Case(9, 0, 'dune'),Case(12, 0, 'dune'),Case(15, 0, 'dune'),Case(17, 0, 'dune'),Case(20, 0, 'dune'),Case(23, 0, 'dune'),Case(25, 0, 'dune'),
                    Case(0, 11, 'flag1'), Case(22, 12, 'flag2'),
                    Case(3, 9, 'dune2'), Case(3, 8, 'dune2'),Case(10, 3, 'dune2'),
                    Case(10, 10, 'tente'), Case(2, 3, 'tente'),
                    Case(0, 13, 'oasis'), Case(2, 13, 'oasis'), Case(19, 13, 'oasis'), Case(21, 13, 'oasis')
                ]
            }
            ,
            { # Map 3
                "terrain": "images/terrain_neige.png",
                "cases": [
                    Case(24, 0, 'montagne'), Case(21, 0, 'montagne'), Case(18, 0, 'montagne'), Case(15, 0, 'montagne'), Case(12, 0, 'montagne'),Case(9, 0, 'montagne'),Case(6, 0, 'montagne'),Case(3, 0, 'montagne'),Case(-1, 0, 'montagne'),
                    Case(0, 7, 'flag1'), Case(15, 7, 'flag2'),
                    Case(10, 10, 'glace'), Case(5, 3, 'glace'),Case(5, 4, 'glace'),
                    Case(12, 10, 'bonhomme'), Case(2, 3, 'bonhomme'),
                    Case(22, 1, 'sapin'), Case(21, 1, 'sapin'),Case(20, 1, 'sapin'), Case(19, 2, 'sapin'),Case(18, 1, 'sapin'),Case(22, 3, 'sapin'),Case(21, 2, 'sapin'),Case(20, 3, 'sapin'),Case(15, 5, 'sapin'),Case(10, 8, 'sapin'),Case(2, 12, 'sapin'),
                    Case(0, 12, 'sapin'), Case(-1, 12, 'sapin'), Case(2, 13, 'sapin'),Case(2, 13, 'sapin'),Case(0, 13, 'sapin'),Case(1, 14, 'sapin'),Case(-1, 14, 'sapin'),Case(0, 14, 'sapin'),Case(2, 14, 'sapin'),Case(3, 14, 'sapin'),Case(4, 14, 'sapin'),Case(5, 14, 'sapin'),Case(6, 14, 'sapin'),Case(7, 14, 'sapin'),Case(8, 14, 'sapin'),Case(9, 14, 'sapin'),Case(10, 14, 'sapin') # Sapin
                ]
            }
        ]

        # Sélection d'une map aléatoire
        self.current_map = self.maps[0]

    def draw_map(self):
        """Affiche les cases spécifiques de la map actuelle."""
        for case in self.current_map["cases"]:
            case.draw(self.screen )
            
    
    def all_units_done(self, current_turn):
        """
        Vérifie si toutes les unités du joueur ou de l'ennemi ont terminé leurs actions.
        current_turn : str
            Le tour actuel, soit 'player' soit 'enemy'.
        Retourne :
            bool : True si toutes les unités ont terminé leurs actions, False sinon.
        """
        units = self.player_units if current_turn == 'player' else self.enemy_units
        return all(unit.distance_remaining == 0 for unit in units)   
    

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


    def handle_player_turn(self, player_units):
        """
        Gère le tour d'un joueur. Chaque joueur peut déplacer une unité.
        """
        for unit in player_units:
            unit.reset_distance()  # Réinitialise la distance restante au début du tour

        selected_unit = player_units[0]  # Exemple : on sélectionne toujours la première unité (améliorable)
        has_acted = False
        selected_unit.is_selected = True
        self.flip_display()

        while not has_acted:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0

                    # Déplacement pour les flèches (joueur 1)
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1

                    # Déplacement pour les touches ZQSD (joueur 2)
                    elif event.key == pygame.K_a:  # Gauche
                        dx = -1
                    elif event.key == pygame.K_d:  # Droite
                        dx = 1
                    elif event.key == pygame.K_w:  # Haut
                        dy = -1
                    elif event.key == pygame.K_s:  # Bas
                        dy = 1

                    # Effectuer le déplacement
                    selected_unit.move(dx, dy)
                    self.flip_display()

                    # Fin du tour avec espace
                    if event.key == pygame.K_SPACE:
                        has_acted = True
                        selected_unit.is_selected = False

    def play_game(self):
        """
        Gère la boucle principale du jeu à deux joueurs.
        """
        current_player = 1  # 1 pour le joueur 1, 2 pour le joueur 2

        while self.player_units and self.enemy_units:
            if current_player == 1:
                print("Tour du Joueur 1")
                self.handle_player_turn(self.player_units)
            else:
                print("Tour du Joueur 2")
                self.handle_player_turn(self.enemy_units)
            
            # Alterne entre les joueurs
            current_player = 2 if current_player == 1 else 1
        

    def calculate_move_simple(self, enemy, dx, dy, max_distance=None, prioritize_horizontal=False):
        """
        Calcul simplifié des déplacements pour une unité ennemie.
        Parameters:
            enemy (Unit): L'unité ennemie qui se déplace.
            dx (int): Distance horizontale vers la cible.
            dy (int): Distance verticale vers la cible.
            max_distance (int): Distance maximale autorisée (facultatif).
            prioritize_horizontal (bool): Prioriser les mouvements horizontaux (facultatif).
        Returns:
            (int, int): Déplacement optimal en x et y.
        """
        max_distance = max_distance if max_distance is not None else enemy.distance_remaining
        move_x, move_y = 0, 0
        if prioritize_horizontal:
            # Bouge d'abord horizontalement, puis verticalement
            if abs(dx) > 0:
                move_x = 1 if dx > 0 else -1
            elif abs(dy) > 0:
                move_y = 1 if dy > 0 else -1
        else:
            # Bouge dans la direction la plus éloignée
            if abs(dx) >= abs(dy):
                move_x = 1 if dx > 0 else -1
            elif abs(dy) > 0:
                move_y = 1 if dy > 0 else -1
        # Ajuster pour ne pas dépasser la distance maximale
        move_x = max(-max_distance, min(max_distance, move_x))
        move_y = max(-max_distance, min(max_distance - abs(move_x), move_y))
        return move_x, move_y