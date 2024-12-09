import pygame

# Constantes
GRID_SIZE = 16
CELL_SIZE = 50
WIDTH = (GRID_SIZE * CELL_SIZE)+600
game_width = int(WIDTH * 0.85)  # 3/4 de la largeur
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    team : str
        L'équipe de l'unité ('player1' ou 'player2').
    nom : str
        Nom de l'unité ('soldat' ou 'medecin' ou 'helico' ou 'char').
    is_selected : bool
        Si l'unité est sélectionnée ou non.
    distance_remaining : int
        Nombre de cases que l'unité peut encore parcourir ce tour.

    Méthodes
    --------
    reset_distance()
        Réinitialise la distance restante au début d'un tour.
    move(direction)
        Déplace l'unité dans une direction donnée au maximum de son périmètre.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, team, name):
        self.x = x
        self.y = y
        self.team = team
        self.is_selected = False
        self.name = name 

        # Initialisation des capacités selon le type d'unité
        if self.name == 'soldat':
            self.max_distance = 2 # Distance maximale 
            self.health = 6
            self.max_health = 6

        elif self.name == 'medecin':
            self.max_distance = 2  # Distance de déplacement
            self.health = 2
            self.max_health = 2
        elif self.name == 'helico':
            self.max_distance = 4  # Distance maximale (4 cases)
            self.health = 3
            self.max_health = 3
        elif self.name == 'char':
            self.max_distance = 10 # Distance maximale (2 cases)
            self.health = 6
            self.max_health =6

    
    def reset_distance(self):
        """Réinitialise la distance restante au maximum a chaque tour."""
        self.distance_remaining = self.max_distance

    def move(self, direction, game):
        """
        Déplace l'unité dans une direction donnée si le déplacement est autorisé.

        Parameters:
        ----------
        direction : str
            La direction dans laquelle déplacer l'unité ('up', 'down', 'left', 'right').
        game : Game
            L'instance du jeu pour accéder aux cases et vérifier les déplacements autorisés.
        """
        # Calcul des nouvelles coordonnées en fonction de la direction
        new_x, new_y = self.x, self.y
        if self.distance_remaining > 0:  # Vérifier s'il reste des déplacements

            if direction == "up":
                new_y -= 1
            elif direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1
            else:
                print(f"Direction invalide : {direction}")
                return
            # Réduire le nombre de déplacements restants après chaque mouvement
            self.distance_remaining -= 1
            self.has_moved = True  # Marquer l'unité comme ayant bougé
        else:
            print("Cette unité a épuisé ses déplacements.")

        # Vérifie les limites de déplacement (distance autorisée)
        cases_autorisees = self.get_deplacement_autorise(game)
        if (new_x, new_y) in cases_autorisees:
            # Vérifie si la case cible est traversable
            target_case = game.get_case_at(new_x, new_y)
            if target_case and target_case.effet.get("traversable", True):
                # Mettre à jour la position de l'unité
                self.x, self.y = new_x, new_y
                self.distance_remaining -= 1  # Réduit la distance restante pour ce tour
                print(f"{self.name} déplacé à ({self.x}, {self.y}). Distance restante : {self.distance_remaining}.")
            else:
                print(f"Déplacement bloqué : case non traversable à ({new_x}, {new_y}).")
        else:
            print(f"Déplacement interdit : hors du rayon de déplacement autorisé ({new_x}, {new_y}).")



    def get_deplacement_autorise(self, game):
        """
        Calcule les cases accessibles selon la position actuelle et la distance maximale.

        Parameters:
        ----------
        game : Game
            Instance du jeu pour accéder aux cases et vérifier les traversabilités.

        Returns:
        -------
        List[Tuple[int, int]] : Liste des coordonnées accessibles.
        """
        cases_accessibles = []
        for dx in range(-self.max_distance, self.max_distance + 1):
            for dy in range(-self.max_distance, self.max_distance + 1):
                new_x = self.x + dx
                new_y = self.y + dy

                # Vérifie si les coordonnées sont dans les limites de la grille
                if 0 <= new_x < game_width and 0 <= new_y < HEIGHT:
                    target_case = game.get_case_at(new_x, new_y)

                    # Vérifie si la case est traversable
                    if target_case and target_case.effet.get("traversable", True):
                        cases_accessibles.append((new_x, new_y))
        return cases_accessibles


    def draw(self, screen):
        """Affiche l'unité sur l'écran."""

        # Charger et redimensionner les sprites
        if self.name == 'soldat':
            sprite = pygame.image.load("images/soldat.png")
            sprite = pygame.transform.scale(sprite, (2*CELL_SIZE , 2*CELL_SIZE ))
        elif self.name == 'medecin':
            sprite = pygame.image.load("images/medecin.png")
            sprite = pygame.transform.scale(sprite, (2*CELL_SIZE, 2*CELL_SIZE))
        elif self.name == 'helico':
            sprite = pygame.image.load("images/helico.png")
            sprite = pygame.transform.scale(sprite, (3 * (CELL_SIZE - 2), 3 * (CELL_SIZE - 2)))
        elif self.name == 'char':
            sprite = pygame.image.load("images/char.png")
            sprite = pygame.transform.scale(sprite, (3 * CELL_SIZE, 3 * CELL_SIZE))
        else:
            return  # Si aucun type ne correspond

        # Dessiner le sprite
        screen.blit(sprite, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Calcul de la barre de santé
        health_p = max(0, min(1, self.health / self.max_health))  # Proportion de santé restante
        health_bar = int(CELL_SIZE * 0.9)  # Largeur totale de la barre de santé
        health_width = int(health_bar * health_p)  # Largeur basée sur la santé restante
        health_height = 6  # Hauteur de la barre de santé

        # Position horizontale centrée
        if self.name == 'soldat':
            health_x = self.x * CELL_SIZE + (2 * (CELL_SIZE )) // 2 - health_bar // 2
        elif self.name == 'medecin':
            health_x = self.x * CELL_SIZE + (2 * CELL_SIZE) // 2 - health_bar // 2
        elif self.name== 'helico':
            health_x = self.x * CELL_SIZE + (3 * (CELL_SIZE - 2)) // 2 - health_bar // 2
        elif self.name == 'char':
            health_x = self.x * CELL_SIZE + (3 * CELL_SIZE) // 2 - health_bar // 2
        else:
            health_x = self.x * CELL_SIZE + CELL_SIZE // 2 - health_bar // 2

        # Position verticale ajustée
        if self.name == 'soldat':
            health_y = self.y * CELL_SIZE - 5
        elif self.name == 'medecin':
            health_y = self.y * CELL_SIZE - 5
        elif self.name == 'helico':
            health_y = self.y * CELL_SIZE + 10
        elif self.name == 'char':
            health_y = self.y * CELL_SIZE +60
        

        # Dessiner la bordure de la barre de santé
        border_largeur = 2
        borders = 3
        pygame.draw.rect(screen, (0, 0, 0), (health_x - border_largeur, health_y - border_largeur,
                                            health_bar + 2 * border_largeur, health_height + 2 * border_largeur),
                        border_radius=borders)

        # Dessiner la barre de santé
        color = GREEN if self.team == "player1" else RED
        pygame.draw.rect(screen, color, (health_x, health_y, health_width, health_height), border_radius=borders)

        if self.propriete == "oasis":
        # Dessiner une aura de soin.
            pygame.draw.circle(screen, (0, 255, 0), (self.x * CELL_SIZE, self.y * CELL_SIZE), 10)
        elif self.propriete == "glace":
        # Indiquer un ralentissement avec un effet de givre.
            pygame.draw.circle(screen, (173, 216, 230), (self.x * CELL_SIZE, self.y * CELL_SIZE), 10)