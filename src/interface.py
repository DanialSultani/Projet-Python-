import pygame
import random
from unit import *
from case import *
from case import Case
from competence import *
from sons import *


# Constantes pour l'adaptation dynamique
CELL_SIZE = 50
GRID_SIZE = 16  # Nombre de cellules par dimension



# Couleur 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
BLUE= (0, 0, 255, 255)
FPS = 60

#Maps
MAPS = [
        { # Map 1: Foret
            "terrain": "images/terrain_herbe.png",  # Terrain de la map
            "cases": [  # Cases spécifiques de la map
                Case(22, 1, 'arbre'), Case(18, 1, 'arbre'), Case(13, 1, 'arbre'), Case(7, 2, 'arbre'),
                Case(15, 2, 'tronc'), Case(20, 4, 'arbre'), Case(11, 1, 'tronc'), Case(17, 8, 'arbre'),
                Case(4, 6, 'arbre'), Case(0, 7, 'arbre'), Case(12, 7, 'arbre'), Case(21, 7, 'arbre'),
                Case(10, 10, 'arbre'), Case(18, 10, 'buisson'), Case(11, 13, 'arbre'), Case(3, 11, 'arbre'), Case(13, 12, 'tronc'),
                Case(0, 13, 'arbre'),
                Case(13, 5, 'tronc'), Case(15, 13, 'tronc'),Case(15, 3, 'buisson'), Case(12, 13, 'buisson'),Case(18, 6, 'tronc'), Case(5, 9, 'tronc'),
                Case(4, 11, 'boue'), Case(3, 11, 'boue'),Case(10, 8, 'boue'),Case(7, 3, 'boue'),Case(14, 4, 'boue'),
                Case(19, 14, 'brin'),
                Case(3, 1, 'buisson'), Case(10, 3, 'buisson'),Case(3, 5, 'buisson'),Case(11, 6, 'buisson'),Case(7, 7, 'buisson'),Case(0, 10, 'buisson'),Case(21, 10, 'buisson'),Case(12, 16, 'buisson'),Case(3, 13, 'buisson'),
                Case(4, 4, 'puit'), Case(16, 11, 'puit'),
                Case(6, 4, 'mur'), Case(18, 12, 'mur'),
                Case(0, 1, 'flag1'), Case(22, 14, 'flag2'), # Drapeau 

            ]
        },
        { # Map 2 : Desert
            "terrain": "images/terrain_sables.png",
            "cases": [
                Case(0, 0, 'dune'), Case(3, 0, 'dune'), Case(6, 0, 'dune'), Case(9, 0, 'dune'),Case(12, 0, 'dune'),Case(15, 0, 'dune'),Case(17, 0, 'dune'),Case(20, 0, 'dune'),Case(23, 0, 'dune'),Case(25, 0 , 'dune'),
                Case(0, 1, 'flag1'), Case(22, 14, 'flag2'),
                Case(9, 3, 'dune2'), Case(21, 2, 'dune2'),Case(15, 5, 'dune2'),Case(17, 9, 'dune2'),Case(1, 13, 'dune2'),Case(11, 13, 'dune2'),Case(8, 9, 'dune2'), Case(1, 7, 'dune2'),
                Case(5, 12, 'tente'), Case(5, 5, 'tente'), Case(15, 3, 'tente'),Case(21, 6, 'tente'),Case(11, 7, 'tente'),
                Case(13, 10, 'chameau'), Case(15, 13, 'chameau'), Case(19, 5, 'chameau'), Case(2, 11, 'chameau'),Case(9, 6, 'chameau'),Case(7, 3, 'chameau'),
                Case(21, 9, 'oasis'), Case(3, 4, 'oasis'), 
            ]
        }
        ,
        { # Map 3 : Neige
            "terrain": "images/terrain_neige.png",
            "cases": [
                Case(24, 0, 'montagne'), Case(21, 0, 'montagne'), Case(18, 0, 'montagne'), Case(15, 0, 'montagne'), Case(12, 0, 'montagne'),Case(9, 0, 'montagne'),Case(6, 0, 'montagne'),Case(3, 0, 'montagne'),Case(0, 0, 'montagne'),
                Case(0, 1, 'flag1'), Case(22, 14, 'flag2'),
                Case(10, 7, 'glace'), Case(16, 9, 'glace'),Case(17, 3, 'glace'),Case(6, 3, 'glace'),Case(8, 11, 'glace'),Case(4, 9, 'glace'),
                Case(12, 10, 'bonhomme'), Case(11, 4, 'bonhomme'), Case(15, 3, 'bonhomme'),  Case(22, 2, 'bonhomme'),  Case(20, 9, 'bonhomme'), Case(6, 13, 'bonhomme'),  Case(2, 11, 'bonhomme'),
                Case(18, 12, 'feu'), Case(4, 5, 'feu'),
                Case(9, 9, 'sapin'),Case(16, 5, 'sapin'), Case(18, 1, 'sapin'), Case(13, 1, 'sapin'), Case(7, 2, 'sapin'),
                Case(20, 4, 'sapin'), Case(17, 8, 'sapin'),
                Case(5, 7, 'sapin'), Case(0, 7, 'sapin'), Case(12, 7, 'sapin'), Case(21, 7, 'sapin'),
                Case(13, 12, 'sapin'), Case(3, 11, 'sapin'),
                Case(0, 13, 'sapin'),Case(16, 16, 'sapin'),Case(11, 4, 'sapin'),Case(8, 14, 'sapin'),              
                ]
        }
    ]

class Display:
    def __init__(self, screen, current_map):
        self.screen = screen
        
         # Configure la carte sélectionnée
        self.current_map = current_map
        
        # Dimensions de la fenêtre et de la surface de jeu
        self.game_width = int(WIDTH * 0.85)  # 85% de la largeur pour le terrain de jeu
        self.game_height = HEIGHT
        self.game_surface = pygame.Surface((self.game_width, self.game_height))  # Surface temporaire pour le jeu
        
        # Charger le terrain de la map
        try:
            terrain_image = pygame.image.load(self.current_map["terrain"])
            self.terrain_image = pygame.transform.scale(terrain_image, (CELL_SIZE, CELL_SIZE))
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image du terrain : {e}")
            pygame.quit()
            exit()

        # Dessiner la barre latérale (1/4 de la fenêtre pour options, pouvoirs, etc.)
        sidebar_width = WIDTH - game_width
        self.sidebar_surface = pygame.Surface((sidebar_width, HEIGHT))
        try:
            sidebar_image = pygame.image.load("images/back_lateral.png")
            self.sidebar_image = pygame.transform.scale(sidebar_image, (3 * sidebar_width, HEIGHT))
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image de la barre latérale : {e}")


        self.font = pygame.font.Font("images/GameBoy.ttf", 10)

    def update(self,units):
        self.update_game_surface(units)
        self.update_sidebar_surface()

    def update_game_surface(self, units):
        self.draw_terrain()
        for unit in units :
            unit.draw(self.game_surface)
        self.screen.blit(self.game_surface, (0, 0))
        pygame.display.flip()
        
    def draw_terrain(self):
        """
        Affiche le terrain de la map actuelle.
        """
        for x in range(0, self.game_width, CELL_SIZE):
            for y in range(0, self.game_height, CELL_SIZE):
                self.game_surface.blit(self.terrain_image, (x, y))
        for case in self.current_map["cases"]:
            case.draw(self.game_surface)

    def update_sidebar_surface(self):
        self.sidebar_surface.blit(self.sidebar_image, (-200, 0))
        self.screen.blit(self.sidebar_surface, (self.game_width, 0))
        instructions = [
            " Selectionnez une unite :",
            " Z- Soldat",
            " Q- Medecin",
            " S- Helico",
            " D- Tank",
            "",
            "",
            "",
            " Selectionnez une compétence :",
            " 1- Attaque",
            " 2- Defense",  
            " 3- Aucun",         
        ]

        # Dessiner chaque ligne d'instruction
        y = 150
        for line in instructions:
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (self.game_width, y))
            y += 30
        pygame.display.flip()



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

    def __init__(self, screen, selected_map_index):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        
        self.screen = screen

        self.player1_units = [Soldat(2, 2,  'player1'),
                             Medecin(3, 1, 'player1'),
                             Helico(0, 3, 'player1'),
                             Tank(10, 10, 'player1')]

        self.player2_units = [Soldat(20, 12, 'player2'),
                            Medecin(22, 11, 'player2'),
                            Helico(19, 14, 'player2'),
                            Tank(11, 12, 'player2')]
        
        self.start_time = pygame.time.get_ticks()  # Enregistre le temps de départ
        self.time_limit = 200000 # Par exemple, 5 minutes = 300000 ms (5 * 60 * 1000)
    
        # Configure la carte sélectionnée
        self.current_map = MAPS[selected_map_index]
        self.display = Display(screen, self.current_map)
        self.initialiser_grille()
        self.sound= SoundEffect() #sond 
        
    def initialiser_grille(self):
        """
        Initialise la grille comme une matrice 2D où chaque cellule représente une case.
        """
        # Création d'une grille vide de dimensions WIDTH x HEIGHT
        self.grille = [[None for _ in range(WIDTH // CELL_SIZE)] for _ in range(HEIGHT // CELL_SIZE)]

        # Parcourir toutes les positions de la grille
        for x in range(WIDTH // CELL_SIZE):
            for y in range(HEIGHT // CELL_SIZE):
                # Vérifie si une case spécifique existe à cette position
                existing_case = next((case for case in self.current_map["cases"] if case.x == x and case.y == y), None)
                if existing_case:
                    self.grille[y][x] = existing_case  # Ajoute la case existante
                else:
                    # Ajoute une case par défaut (herbe) si aucune case spécifique n'est trouvée
                    self.grille[y][x] = Case(x, y, "herbe")
                    
    def check(self):
        # check units
        self.player1_units = [unit for unit in self.player1_units if unit.health > 0]
        self.player2_units = [unit for unit in self.player2_units if unit.health > 0]
        # check victory
        self.check_victory()
        
    def update(self):
        self.check()
        self.display.update(units=self.player1_units+self.player2_units)

        
         
    def get_time_remaining(self):
        """
        Calcule le temps restant avant la fin du jeu.
        Retourne le temps restant en secondes.
        """
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = max(0, self.time_limit - elapsed_time)  # Évite les valeurs négatives
        return remaining_time // 1000  # Retourne en secondes
            
    def check_victory(self):
        """
        Vérifie les conditions de victoire :
        - Capture de drapeau.
        - Élimination de toutes les unités adverses.
        - Fin du temps limite.
        """
        # Condition 1 : Toutes les unités de l'équipe 2 sont éliminées
        if all(unit.health <= 0 for unit in self.player2_units):
            show_victory_screen(self.screen, "player1")
            return True

        # Condition 2 : Toutes les unités de l'équipe 1 sont éliminées
        elif all(unit.health <= 0 for unit in self.player1_units):
            show_victory_screen(self.screen, "player2")
            return True

        # Condition 3 : Fin du temps
        if self.get_time_remaining() == 0:
            player1_units_alive = sum(1 for unit in self.player1_units if unit.health > 0)
            player2_units_alive = sum(1 for unit in self.player2_units if unit.health > 0)

            if player1_units_alive > player2_units_alive:
                show_victory_screen(self.screen, "player1")
            elif player2_units_alive > player1_units_alive:
                show_victory_screen(self.screen, "player2")
            else:
                show_victory_screen(self.screen, "draw")  # Match nul
            return True

        # Aucune condition de victoire atteinte
        return False



    def get_case_at(self, x, y):
        """
        Retourne la case à une position donnée ou None si elle est hors limites.
        """
        if 0 <= x < WIDTH // CELL_SIZE and 0 <= y < HEIGHT // CELL_SIZE:
            return self.grille[y][x]  # Accès direct à la case
        return None  # Hors des limites de la grille


    def handle_unit_turn(self, player_units, current_turn):
        """
        Gère le tour d'une unité. Chaque unité peut se déplacer ou attaquer.

        Parameters:
        ----------
        player_units : list
            La liste des unités du joueur en cours.
        current_turn : str
            Le joueur en cours ('player1' ou 'player2').
        """
        # Réinitialisation des distances des unités au début du tour
        for unit in player_units:
            unit.reset_distance()

        selected_unit = None
        has_acted = False
        selected_competence = None

        while not has_acted:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # Sélection de l'unité
                    if not selected_unit and event.key in [pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d]:
                        unit_index = {'z': 0, 'q': 1, 's': 2, 'd': 3}.get(event.unicode, -1)
                        if 0 <= unit_index < len(player_units):
                            selected_unit = player_units[unit_index]
                            self.sound.play('click') #ajout du son
                            print(f"{selected_unit.name} est sélectionné.")
                            self.display.update_game_surface(self.player1_units+self.player2_units)

                    # Déplacement de l'unité sélectionnée
                    if selected_unit and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        directions = {
                            pygame.K_UP: "up",
                            pygame.K_DOWN: "down",
                            pygame.K_LEFT: "left",
                            pygame.K_RIGHT: "right",
                        }
                        selected_unit.move(directions[event.key], self)
                        self.sound.play('marche')
                        pygame.time.delay(100)  # Empêche les déplacements trop rapides
                        self.display.update_game_surface(self.player1_units+self.player2_units)

                    # Utilisation des compétences
                    elif selected_unit and event.key in [pygame.K_1, pygame.K_2]:
                        competence_index = [pygame.K_1, pygame.K_2].index(event.key)     
                        if competence_index < len(selected_unit.competence):
                            competence = selected_unit.competence[competence_index]
                            if current_turn == 'player1':
                                self.sound.play('tire')
                                competence.use(selected_unit, self.player1_units, self.player2_units)
                                has_acted = True
                                selected_unit= False
                                selected_competence=True
                            else:
                                competence.use(selected_unit, self.player2_units, self.player1_units)
                                self.sound.play('tire')
                                has_acted = True
                                selected_unit= False
                                selected_competence=True
                            

                    elif not selected_competence and selected_unit and event.key ==pygame.K_3:
                        has_acted = True
                        selected_unit= False 
    
            self.update()

    
    def play_game(self):
        """Gère la boucle principale du jeu."""
        current_turn = 'player1'
        clock = pygame.time.Clock()

        while self.player1_units and self.player2_units:
            start_time = pygame.time.get_ticks()

            # Gère les tours des joueurs
            if current_turn == 'player1':
                # text = self.font.render('Tour du joueur 1', True, WHITE)
                # self.screen.blit(text, (game_width, 100))
                self.handle_unit_turn(self.player1_units, current_turn)
            else:
                # text = self.font.render('Tour du joueur 2', True, WHITE)
                # self.screen.blit(text, (game_width, 100))
                self.handle_unit_turn(self.player2_units, current_turn)

            # Alterner les tours
            current_turn = 'player2' if current_turn == 'player1' else 'player1'

            # Limiter le temps par frame
            elapsed_time = pygame.time.get_ticks() - start_time
            clock.tick(FPS)


