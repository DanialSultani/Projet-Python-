import pygame
import random
from unit import *
from case import *
from case import Case


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
        self.CELL_SIZE = 50  # Taille d'une cellule
        self.GRID_WIDTH = screen.get_width() // self.CELL_SIZE  # Largeur en cellules
        self.GRID_HEIGHT = screen.get_height() // self.CELL_SIZE  # Hauteur en cellules

        self.player_units = [Unit(1, 3, 10, 2, 'player','soldat',name='soldat'),
                             Unit(1, 4, 10, 2, 'player','medecin',name='medecin'),
                             Unit(1, 1, 10, 2, 'player','helico',name='helico'),
                             Unit(1, 6, 8, 1, 'player','char',name='char')]

        self.enemy_units = [Unit(20, 9, 8, 1, 'enemy','soldat',name='soldat'),
                            Unit(20, 11, 10, 2, 'enemy','medecin',name='medecin'),
                            Unit(20, 13, 8, 1, 'enemy','helico',name='helico'),
                            Unit(23, 13, 8, 1, 'enemy','char',name='char')]
        
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

        # Initialisation de la grille avec toutes les cases traversables
        self.initialiser_grille()

    def initialiser_grille(self):
        """
        Initialise la grille avec toutes les cases traversables par défaut,
        sauf celles occupées par des objets environnementaux.
        """
        traversable_cases = []
        # Parcourt toutes les positions de la grille
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                # Vérifie si une case environnementale existe déjà ici
                existing_case = self.get_case_at(x, y)
                if existing_case:
                    # Si une case environnementale existe, on conserve sa propriété
                    traversable_cases.append(existing_case)
                else:
                    # Ajoute une case traversable par défaut
                    traversable_cases.append(Case(x, y, "herbe"))

        # Remplace les cases actuelles par celles nouvellement générées
        self.current_map["cases"] = traversable_cases

    def draw_map(self):
        """Affiche les cases spécifiques de la map actuelle."""
        for case in self.current_map["cases"]:
            case.draw(self.screen )

    def handle_interactions(self):
        """
        Gère les interactions entre les unités et les cases de la map actuelle.
        """
        for unit in self.player_units + self.enemy_units:
            for case in self.current_map["cases"]:
                if case.x == unit.x and case.y == unit.y:
                    try:
                        case.appliquer_effet(unit, self.screen)  # Passe l'écran pour l'affichage
                        print(f"Interaction : {unit.name} interagit avec {case.propriete}.")
                    except ValueError as e:
                        print(f"Erreur d'interaction : {e}")
         
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

    def get_case_at(self, x, y):
        """
        Retourne la case à une position donnée ou None si aucune case n'est définie.

        Si aucune case spécifique n'est trouvée, retourne une case traversable par défaut
        si les coordonnées sont dans les limites de la grille.
        """
        for case in self.current_map["cases"]:
            if case.x == x and case.y == y:
                return case
        # Par défaut, retourne une case traversable si elle est dans la grille
        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
            return Case(x, y, "herbe")  # Case traversable par défaut
        return None



    def handle_unit_turn(self, player_units, current_turn):
        """
        Gère le tour d'une unité. Chaque unité peut se déplacer.

        Parameters:
        ----------
        player_units : list
            La liste des unités du joueur en cours.
        current_turn : str
            Le joueur en cours ('player' ou 'enemy').
        """
        for unit in player_units:
            unit.reset_distance()

        selected_unit = player_units[0]
        has_acted = False
        selected_unit.is_selected = True
        self.flip_display()

        while not has_acted:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_unit.move("up", self)
                    elif event.key == pygame.K_DOWN:
                        selected_unit.move("down", self)
                    elif event.key == pygame.K_LEFT:
                        selected_unit.move("left", self)
                    elif event.key == pygame.K_RIGHT:
                        selected_unit.move("right", self)

                    # Met à jour l'affichage
                    self.flip_display()

                    # Fin du tour avec la touche ESPACE
                    if event.key == pygame.K_SPACE:
                        has_acted = True
                        selected_unit.is_selected = False

    def play_game(self):
        current_turn = 'player'

        while self.player_units and self.enemy_units:
            if current_turn == 'player':
                print("Tour du joueur.")
                for unit in self.player_units:
                    unit.reset_distance()
                self.handle_unit_turn(self.player_units, current_turn)
            else:
                print("Tour de l'ennemi.")
                for unit in self.enemy_units:
                    unit.reset_distance()
                self.handle_unit_turn(self.enemy_units, current_turn)

            # Alterner les tours
            current_turn = 'enemy' if current_turn == 'player' else 'player'

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