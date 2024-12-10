import pygame
import random
from unit import *
from game import *
from case import *
from case import Case
from competence import *


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

        self.player1_units = [Unit(2, 2,  'player1','soldat'),
                             Unit(3, 1, 'player1','medecin'),
                             Unit(0, 3, 'player1','helico'),
                             Unit(0, 1, 'player1','char')]

        self.player2_units = [Unit(20, 12, 'player2','soldat'),
                            Unit(22, 11, 'player2','medecin'),
                            Unit(19, 14, 'player2','helico'),
                            Unit(21, 12, 'player2','char')]
        
        # Liste des maps avec un terrain spécifique  
        self.maps = [
            { # Map 1: Foret
                "terrain": "Projet-Python-/images/terrain_herbe.png",  # Terrain de la map
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
                "terrain": "Projet-Python-/images/terrain_sables.png",
                "cases": [
                    Case(0, 0, 'dune'), Case(3, 0, 'dune'), Case(6, 0, 'dune'), Case(9, 0, 'dune'),Case(12, 0, 'dune'),Case(15, 0, 'dune'),Case(17, 0, 'dune'),Case(20, 0, 'dune'),Case(23, 0, 'dune'),Case(25, 0, 'dune'),
                    Case(0, 1, 'flag1'), Case(22, 14, 'flag2'),
                    Case(9, 3, 'dune2'), Case(21, 2, 'dune2'),Case(15, 5, 'dune2'),Case(17, 9, 'dune2'),Case(1, 13, 'dune2'),Case(11, 13, 'dune2'),Case(8, 9, 'dune2'), Case(1, 7, 'dune2'),
                    Case(5, 12, 'tente'), Case(5, 5, 'tente'), Case(15, 3, 'tente'),Case(21, 6, 'tente'),Case(11, 7, 'tente'),
                    Case(13, 10, 'chameau'), Case(15, 13, 'chameau'), Case(19, 5, 'chameau'), Case(2, 11, 'chameau'),Case(9, 6, 'chameau'),Case(7, 3, 'chameau'),
                    Case(21, 9, 'oasis'), Case(3, 4, 'oasis'), 
                ]
            }
            ,
            { # Map 3 : Neige
                "terrain": "Projet-Python-/images/terrain_neige.png",
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

        # Sélection d'une map aléatoire
        self.current_map = self.maps[choose_map(screen)]

        # Initialisation de la grille avec toutes les cases traversables
        self.initialiser_grille()

        self.start_time = pygame.time.get_ticks()  # Temps initial du jeu
        self.time_limit = 3 * 60 * 1000  # 3 minutes en millisecondes

    def initialiser_grille(self):
        """
        Initialise la grille avec toutes les cases traversables par défaut,
        sauf celles occupées par des objets environnementaux.
        """
        traversable_cases = []
        # Parcourt toutes les positions de la grille
        for x in range(WIDTH):
            for y in range(HEIGHT):
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

    def get_time_remaining(self):
        """
        Calcule le temps restant avant la fin du jeu.
        :return: Temps restant en millisecondes.
        """
        elapsed_time = pygame.time.get_ticks() - self.start_time
        return max(0, self.time_limit - elapsed_time)


    def draw_map(self):
        """Affiche les cases spécifiques de la map actuelle."""
        for case in self.current_map["cases"]:
            case.draw(self.screen )

    def handle_interactions(self):
        """Gère les interactions entre les unités et les cases de la map actuelle."""
        for unit in self.player1_units + self.player2_units:
            case = self.get_case_at(unit.x, unit.y)
            if case:
                try:
                    case.appliquer_effet(unit, self.screen)  # Appliquer les effets de la case
                    print(f"{unit.name} interagit avec {case.propriete}.")
                except ValueError as e:
                    print(f"Erreur d'interaction : {e}")
            else:
                # Réinitialiser les effets si l'unité quitte une case
                unit.reset_effects()

         
    def all_units_done(self, current_turn):
        """
        Vérifie si toutes les unités du joueur ou de l'ennemi ont terminé leurs actions.
        current_turn : str
            Le tour actuel, soit 'player' soit 'enemy'.
        Retourne :
            bool : True si toutes les unités ont terminé leurs actions, False sinon.
        """
        units = self.player1_units if current_turn == 'player1' else self.player2_units
        return all(unit.distance_remaining == 0 for unit in units)  
        
    def check_victory(self):
        """
        Vérifie les conditions de victoire :
        - Capture de drapeau.
        - Élimination de toutes les unités adverses.
        - Fin du temps limite.
        """
        # Condition 1 : Toutes les unités de l'équipe 2 sont éliminées
        if all(unit.health <= 0 for unit in self.player2_units):
            show_victory_screen(self.screen, "player")
            return True

        # Condition 2 : Toutes les unités de l'équipe 1 sont éliminées
        elif all(unit.health <= 0 for unit in self.player1_units):
            show_victory_screen(self.screen, "enemy")
            return True

        # Condition 3 : Fin du temps
        if self.get_time_remaining() == 0:
            player1_units_alive = sum(1 for unit in self.player1_units if unit.health > 0)
            player2_units_alive = sum(1 for unit in self.player2_units if unit.health > 0)

            if player1_units_alive > player2_units_alive:
                show_victory_screen(self.screen, "player")
            elif player2_units_alive > player1_units_alive:
                show_victory_screen(self.screen, "enemy")
            else:
                show_victory_screen(self.screen, "draw")  # Match nul
            return True

        # Aucune condition de victoire atteinte
        return False
    def draw_timer(self):
        """
        Affiche le temps restant sur l'écran de jeu.
        """
        time_remaining = self.get_time_remaining() // 1000  # Convertir en secondes
        minutes = time_remaining // 60
        seconds = time_remaining % 60
        timer_text = f"Temps restant : {minutes:02}:{seconds:02}"

        font = pygame.font.Font(None, 36)
        text = font.render(timer_text, True, (255, 255, 255))  # Blanc
        self.screen.blit(text, (10, 10))  # Affiche en haut à gauche



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
            ciel= pygame.image.load("Projet-Python-/images/ciel.jpg")
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
        for unit in self.player1_units+ self.player2_units:
            unit.draw(game_surface)

        # Blitter la surface de jeu (game_surface) sur la fenêtre principale (screen)
        self.screen.blit(game_surface, (0, 0))

        # Dessiner le panneau latéral (1/4 de la fenêtre) pour les options, pouvoirs, etc.
        sidebar_width = WIDTH - game_width  # 1/4 de la largeur
        sidebar_surface = pygame.Surface((sidebar_width, HEIGHT))
        back_lat= pygame.image.load("Projet-Python-/images/back_lateral.png")
        back_lat= pygame.transform.scale(back_lat, (3*sidebar_width , HEIGHT))
        sidebar_surface.blit(back_lat,(-200, 0))  # Fond sombre pour le panneau

        
        # Rafraîchir l'affichage
        self.screen.blit(sidebar_surface, (game_width, 0))
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
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            return Case(x, y, "herbe")  # Case traversable par défaut
        return None

    def draw_instructions_select_unit(self):
        """
        Dessine les instructions pour sélectionner une unité.
        """
        # Effacer la zone de la bande latérale
        game_width = int(WIDTH * 0.85)  # 3/4 de la largeur
        sidebar_width = WIDTH - game_width  # 1/4 de la largeur
        sidebar_surface = pygame.Surface((sidebar_width, HEIGHT))
        back_lat= pygame.image.load("Projet-Python-/images/back_lateral.png")
        back_lat= pygame.transform.scale(back_lat, (3*sidebar_width , HEIGHT))
        sidebar_surface.blit(back_lat,(-200, 0))  # Fond sombre pour le panneau

        # Texte des instructions
        instructions = [
            "Selectionnez une unite :",
            "Z - Soldat",
            "Q - Medecin",
            "S - Helico",
            "D - Tank",
        ]

        # Dessiner chaque ligne d'instruction
        font = pygame.font.Font("Projet-Python-/images/GameBoy.ttf", 10)
        y = 150
        for line in instructions:
                text = font.render(line, True, WHITE)
                self.screen.blit(text, (game_width, y))
                y += 30

    

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
        selected_unit = None
        has_acted = False
        self.draw_instructions_select_unit()

        

        while not has_acted:

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    # Sélection d'une unité
                    if event.key == pygame.K_z and len(player_units) > 0:
                        selected_unit = player_units[0]
                    elif event.key == pygame.K_q and len(player_units) > 1:
                        selected_unit =player_units[1]
                    elif event.key == pygame.K_s and len(player_units) > 2:
                        selected_unit = player_units[2] 
                    elif event.key == pygame.K_d and len(player_units) > 3:
                        selected_unit = player_units[3]

                    # Si une unité est sélectionnée
                    if selected_unit:
                        print(f"{selected_unit.name} est sélectionné.")
                        self.flip_display()

                        if event.key == pygame.K_UP:
                            selected_unit.move("up", self)
                        elif event.key == pygame.K_DOWN:
                            selected_unit.move("down", self)
                        elif event.key == pygame.K_LEFT:
                            selected_unit.move("left", self)
                        elif event.key == pygame.K_RIGHT:
                            selected_unit.move("right", self)
                            
                            
                        # Gérer les compétences
                        elif event.key == pygame.K_1:  # Première compétence
                            if len(unit.competences) >= 1:
                                competence = unit.competences[0]
                                self.utiliser_competence(unit, competence, player_units)
                        elif event.key == pygame.K_2:  # Deuxième compétence
                            if len(unit.competences) >= 2:
                                competence = unit.competences[1]
                                self.utiliser_competence(unit, competence, player_units)
                        elif event.key == pygame.K_3:  # Troisième compétence
                            if len(unit.competences) >= 3:
                                competence = unit.competences[2]
                                self.utiliser_competence(unit, competence, player_units)


                        # Met à jour l'affichage
                        self.flip_display()

                        # Fin du tour avec la touche ESPACE
                        if event.key == pygame.K_SPACE:
                            has_acted = True
                            selected_unit.is_selected = False
    
    
    def utiliser_competence(self, unit, competence, player_units):
        """
        Permet à une unité d'utiliser une compétence.

        :param unit: L'unité qui utilise la compétence.
        :param competence: La compétence à utiliser.
        :param game: L'instance du jeu pour gérer les effets sur les cibles.
        """
        # Récupérer les cibles à portée
        cibles = self.get_cibles_a_portee(unit, competence, player_units)

        if not cibles:
            print(f"{unit.name} ({unit.team}) ne peut pas utiliser {competence.nom} : aucune cible à portée.")
            return

        # Appliquer la compétence
        result = competence.utiliser(unit, cibles)
        print(result)                

    def play_game(self):
        current_turn = 'player1'

        while self.player1_units and self.player2_units:
            if current_turn == 'player1':
                print("Tour du joueur 1.")
                for unit in self.player1_units:
                    unit.reset_distance()
                self.handle_unit_turn(self.player1_units, current_turn)
            else:
                print("TTour du joueur 2.")
                for unit in self.player2_units:
                    unit.reset_distance()
                self.handle_unit_turn(self.player2_units, current_turn)

            # Alterner les tours
            current_turn = 'player2' if current_turn == 'player1' else 'player1'

    