from abc import ABC
import pygame
from competence import *

# Constantes
GRID_SIZE = 16
CELL_SIZE = 50
WIDTH = (GRID_SIZE * CELL_SIZE)+600
game_width = int(WIDTH * 0.85)  # 3/4 de la largeur
game_width = int(WIDTH * 0.85)  # 3/4 de la largeur
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SPRITES = {
    "soldat": pygame.transform.scale(pygame.image.load("images/soldat.png"), (2 * CELL_SIZE, 2 * CELL_SIZE)),
    "medecin": pygame.transform.scale(pygame.image.load("images/medecin.png"), (2 * CELL_SIZE, 2 * CELL_SIZE)),
    "helico": pygame.transform.scale(pygame.image.load("images/helico.png"), (3 * CELL_SIZE, 3 * CELL_SIZE)),
    "char": pygame.transform.scale(pygame.image.load("images/char.png"), (3 * CELL_SIZE, 3 * CELL_SIZE)),
}


class Unit(ABC):
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

    def __init__(self, x, y, team, name, max_health, attack_power, attack_range, max_distance,competence):

        # Initialisation des attributs
        self.name = name 
        self.max_health = max_health
        self.attack_power = attack_power
        self.attack_range = attack_range
        self.max_distance = max_distance # Vitesse
        self.competence = competence
        # Initialisation des etats
        self.x = x
        self.y = y
        self.team = team
        self.is_selected = False
        self.health = max_health
        self.distance_remaining = 0  # Distance que l'unité peut encore parcourir
        
    def reset_distance(self):
        """Réinitialise la distance restante au maximum a chaque tour."""
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
        if self.distance_remaining <= 0:
            print(f"{self.name} ne peut plus se déplacer ce tour.")
            return

        # Calcul des nouvelles coordonnées
        dx, dy = 0, 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1

        new_x, new_y = self.x + dx, self.y + dy

        # Vérifie si la case cible est valide et traversable
        target_case = game.get_case_at(new_x, new_y)
        if not target_case or not target_case.effet.get("traversable", True):
            print(f"Déplacement bloqué : case non traversable à ({new_x}, {new_y}).")
            return

        # Mettre à jour la position et appliquer les effets
        self.x, self.y = new_x, new_y
        self.distance_remaining -= 1
        print(f"{self.name} déplacé à ({self.x}, {self.y}). Distance restante : {self.distance_remaining}.")

        # Appliquer les effets de la case après le déplacement
        target_case.appliquer_effet(self, game.screen)




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
                if 0 <= new_x < game_width and 0 <= new_y < HEIGHT-1:
                    target_case = game.get_case_at(new_x, new_y)

                    # Vérifie si la case est traversable
                    if target_case and target_case.effet.get("traversable", True):
                        cases_accessibles.append((new_x, new_y))
        return cases_accessibles
    
    def reset_effects(self):
        """Réinitialise les effets temporaires de l'unité."""
        self.invisible = False
        self.invincible = False

    def recevoir_dommage(self, montant):
        """
        Réduit les points de vie de l'unité sauf si elle est invincible.

        :param montant: Nombre de points de dégâts infligés.
        """
        """if self.invincible:
            print(f"{self.name} est invincible et ne reçoit pas de dégâts.")
            return"""
        self.health = max(0, self.health - montant)
        print(f"{self.name} reçoit {montant} de dégâts. Santé restante : {self.health}/{self.max_health}.")

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
    # Liste pour les compétences attribuées
        self.competences = []
    
    def attaquer(self, target):
        """Attaque une unité cible si elle est dans le rayon d'attaque."""
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        if distance <= self.attack_range:
            if hasattr(self, 'heal_power'):  # Si c'est un docteur, il soigne
                target.health = min(target.max_health, target.health + self.heal_power)
                print(f"{self.name} soigne {target.name} pour {self.heal_power} points de vie.")
            else:  # Sinon, il attaque
                target.health -= self.attack_power
                print(f"{self.name} attaque {target.name} pour {self.attack_power} dégâts.")

        else:
            print("Cible hors de portée.")

class Tank(Unit):
    name = "char"
    max_distance = 3 # Distance maximale (2 cases)
    max_health = 12
    attack_power = 3  # Pouvoir d'attaque
    attack_range = 3
    competence = [Canon(),Booster()]
    def __init__(self, x, y, team):
        super().__init__(x, y, team, self.name, self.max_health, self.attack_power, self.attack_range, self.max_distance,self.competence)
    

class Helico(Unit): 
    name = "helico"
    # Initialisation des capacités 
    max_distance = 50  # Distance maximale (4 cases)
    max_health = 3
    attack_power = 3  # Pouvoir d'attaque
    attack_range = 3
    competence = [ArmeAFeu(),Booster()]

    def __init__(self, x, y, team):
        super().__init__(x, y, team, self.name, self.max_health, self.attack_power, self.attack_range, self.max_distance,self.competence)

class Medecin(Unit):
    name = "medecin"
    # Initialisation des capacités 
    max_distance = 4  # Distance de déplacement
    health = 5
    max_health = 2
    heal_power = 2 
    attack_power = 3  # Pouvoir d'attaque
    attack_range = 3
    competence = [ArmeAFeu(),Soin()]

    def __init__(self, x, y, team):
        super().__init__(x, y, team, self.name, self.max_health, self.attack_power, self.attack_range, self.max_distance,self.competence)

class Soldat(Unit):
    name = "soldat"
    # Initialisation des capacités 
    max_distance = 2 # Distance maximale 
    health = 8
    max_health = 6
    attack_power = 1  # Pouvoir d'attaque
    attack_range = 8
    competence = [ArmeAFeu(),Booster()]

    def __init__(self, x, y, team):
        super().__init__(x, y, team, self.name, self.max_health, self.attack_power, self.attack_range, self.max_distance,self.competence)

if __name__ == "__main__":
    tank = Tank(2, 3, "player1", "char", 3, 6)
    print(tank.name)  # char
    
