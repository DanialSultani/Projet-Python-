import pygame

# Constantes
GRID_SIZE = 16
CELL_SIZE = 50
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

    def __init__(self, x, y, health, attack_power, team, deplacement):
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team
        self.deplacement = deplacement
        self.is_selected = False
        self.max_health = health

        # Définit la vitesse (distance maximale) et les pouvoirs par type d'unité
        if self.deplacement == 'soldat':
            self.max_distance = 2
            self.attack_power = 1  # Pouvoir d'attaque
            self.attack_range = 1  # Rayon d'attaque (8 cases autour)
        elif self.deplacement == 'medecin':  # Correction ici pour le médecin
            self.max_distance = 3  # Distance de déplacement correcte pour le médecin
            self.heal_power = 2  # Pouvoir de guérison
            self.attack_range = 1  # Rayon d'action (8 cases autour)
        elif self.deplacement == 'helico':
            self.max_distance = 4
            self.attack_power = 3  # Pouvoir d'attaque
            self.attack_range = 3  # Rayon d'attaque (3 cases en dessous)
        elif self.deplacement == 'char':
            self.max_distance = 6
            self.attack_power = 3  # Pouvoir d'attaque
            self.attack_range = 2  # Rayon d'attaque (2 cases)
        else:
            self.max_distance = 1  # Par défaut
            self.attack_power = 0
            self.attack_range = 0

        self.distance_remaining = self.max_distance  # Initialisation correcte

    def reset_distance(self):
        """Réinitialise la distance restante au maximum pour ce tour."""
        self.distance_remaining = self.max_distance

    def move(self, dx, dy):
        """Déplace l'unité dans une direction donnée, dans la limite de sa distance restante."""
        distance = abs(dx) + abs(dy)
        if distance > self.distance_remaining:
            print(f"Déplacement non autorisé : il reste {self.distance_remaining} cases.")
            return

        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y
            self.distance_remaining -= distance
        else:
            print("Déplacement hors des limites de la grille.")

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
            sprite = pygame.image.load("Projet-Python-/images/soldat.png")
            sprite = pygame.transform.scale(sprite, (2 * (CELL_SIZE - 1), 2 * (CELL_SIZE - 1)))
        elif self.deplacement == 'medecin':
            sprite = pygame.image.load("Projet-Python-/images/medecin.png")
            sprite = pygame.transform.scale(sprite, (4 * CELL_SIZE, 2 * CELL_SIZE))
        elif self.deplacement == 'helico':
            sprite = pygame.image.load("Projet-Python-/images/helico.png")
            sprite = pygame.transform.scale(sprite, (3 * (CELL_SIZE - 2), 3 * (CELL_SIZE - 2)))
        elif self.deplacement == 'char':
            sprite = pygame.image.load("Projet-Python-/images/char.png")
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
            health_x = self.x * CELL_SIZE + (2 * (CELL_SIZE - 1)) // 2 - health_bar // 2
        elif self.deplacement == 'medecin':
            health_x = self.x * CELL_SIZE + (4 * CELL_SIZE) // 2 - health_bar // 2
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
