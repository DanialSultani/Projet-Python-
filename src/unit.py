import pygame

# Constantes
GRID_SIZE = 16
CELL_SIZE = 50
WIDTH = (GRID_SIZE * CELL_SIZE)+600
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
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    deplacement : str
        Moyen de déplacement de l'unité ('soldat' ou 'helico' ou 'char').
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
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team, deplacement, name=None):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team
        self.deplacement = deplacement
        self.is_selected = False
        self.max_health = health
        self.name = name or f"{team}_{deplacement}"

        # Initialisation des capacités selon le type d'unité
        if self.deplacement == 'soldat':
            self.max_distance = 8  # Distance maximale (8 cases)
            self.attack_power = 1  # Pouvoir d'attaque
            self.attack_range = 1  # Rayon d'attaque
        elif self.deplacement == 'medecin':
            self.max_distance = 8  # Distance de déplacement
            self.heal_power = 2    # Pouvoir de guérison
            self.attack_range = 1  # Rayon d'action
        elif self.deplacement == 'helico':
            self.max_distance = 4  # Distance maximale (4 cases)
            self.attack_power = 3  # Pouvoir d'attaque
            self.attack_range = 3  # Rayon d'attaque
        elif self.deplacement == 'char':
            self.max_distance = 2  # Distance maximale (2 cases)
            self.attack_power = 3  # Pouvoir d'attaque
            self.attack_range = 2  # Rayon d'attaque
        else:
            # Valeurs par défaut pour une unité inconnue
            self.max_distance = 1
            self.attack_power = 0
            self.attack_range = 0

        # Distance restante au début d'un tour
        self.distance_remaining = self.max_distance

    def reset_distance(self):
        """Réinitialise la distance restante au maximum pour ce tour."""
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
                if 0 <= new_x < game.GRID_WIDTH and 0 <= new_y < game.GRID_HEIGHT:
                    target_case = game.get_case_at(new_x, new_y)

                    # Vérifie si la case est traversable
                    if target_case and target_case.effet.get("traversable", True):
                        cases_accessibles.append((new_x, new_y))
        return cases_accessibles




    def attack(self, target):
        """Attaque une unité cible si elle est dans le rayon d'attaque."""
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        if distance <= self.attack_range:
            if hasattr(self, 'heal_power'):  # Si c'est un docteur, il soigne
                target.health = min(target.max_health, target.health + self.heal_power)
                print(f"{self.deplacement} soigne {target.deplacement} pour {self.heal_power} points de vie.")
            else:  # Sinon, il attaque
                target.health -= self.attack_power
                print(f"{self.deplacement} attaque {target.deplacement} pour {self.attack_power} dégâts.")
        else:
            print("Cible hors de portée.")

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""

        # Charger et redimensionner les sprites
        if self.deplacement == 'soldat':
            sprite = pygame.image.load("images/soldat.png")
            sprite = pygame.transform.scale(sprite, (2*CELL_SIZE , 2*CELL_SIZE ))
        elif self.deplacement == 'medecin':
            sprite = pygame.image.load("images/medecin.png")
            sprite = pygame.transform.scale(sprite, (2*CELL_SIZE, 2*CELL_SIZE))
        elif self.deplacement == 'helico':
            sprite = pygame.image.load("images/helico.png")
            sprite = pygame.transform.scale(sprite, (3 * (CELL_SIZE - 2), 3 * (CELL_SIZE - 2)))
        elif self.deplacement == 'char':
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
        if self.deplacement == 'soldat':
            health_x = self.x * CELL_SIZE + (2 * (CELL_SIZE )) // 2 - health_bar // 2
        elif self.deplacement == 'medecin':
            health_x = self.x * CELL_SIZE + (2 * CELL_SIZE) // 2 - health_bar // 2
        elif self.deplacement == 'helico':
            health_x = self.x * CELL_SIZE + (3 * (CELL_SIZE - 2)) // 2 - health_bar // 2
        elif self.deplacement == 'char':
            health_x = self.x * CELL_SIZE + (3 * CELL_SIZE) // 2 - health_bar // 2
        else:
            health_x = self.x * CELL_SIZE + CELL_SIZE // 2 - health_bar // 2

        # Position verticale ajustée
        if self.deplacement == 'soldat':
            health_y = self.y * CELL_SIZE - 10
        elif self.deplacement == 'medecin':
            health_y = self.y * CELL_SIZE - 5
        elif self.deplacement == 'helico':
            health_y = self.y * CELL_SIZE + 30
        elif self.deplacement == 'char':
            health_y = self.y * CELL_SIZE + 30
        else:
            health_y = self.y * CELL_SIZE - 15

        # Dessiner la bordure de la barre de santé
        border_largeur = 2
        borders = 3
        pygame.draw.rect(screen, (0, 0, 0), (health_x - border_largeur, health_y - border_largeur,
                                            health_bar + 2 * border_largeur, health_height + 2 * border_largeur),
                        border_radius=borders)

        # Dessiner la barre de santé
        color = (0, 255, 0) if self.team == "player" else (255, 0, 0)
        pygame.draw.rect(screen, color, (health_x, health_y, health_width, health_height), border_radius=borders)