import pygame
import random
from utils import show_victory_screen

# Constantes pour l'adaptation dynamique
CELL_SIZE = 50
GRID_SIZE = 16  # Nombre de cellules par dimension
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)

FPS = 30


class Case :
    """
    Classe pour représenter une case.
    ...
    Attributs
    ---------
    x : int
        La position x de la case sur la grille.
    y : int
        La position y de la case sur la grille.
    propriete : str
        Propriété de la case ('mur', 'herbe', 'flag1', 'flag2', etc.).
    effet : dict
        Les effets spécifiques associés à la case.
    Méthodes
    --------
    draw(screen)
        Dessine la case sur la grille.
    appliquer_effet(unite)
        Applique l'effet de la case à une unité (à définir dans une autre classe).
    bloque_balle()
        Retourne True si la case bloque les balles, False sinon.
    """

    def __init__(self, x, y, propriete):
        """
        Construit une case avec une position et une propriété.

        Paramètres
        ----------
        x : int
            La position x de la case sur la grille.
        y : int
            La position y de la case sur la grille.
        propriete : str
            Type de la case ('mur', 'buisson', 'oasis', etc.).
        """
        self.x = x
        self.y = y
        self.propriete = propriete
        self.effet = self.definir_effet(propriete)
    
    def definir_effet(self, propriete):
        """
        Définit les effets associés au type de la case.

        Paramètres
        ----------
        propriete : str
            Type de la case ('mur', 'buisson', 'oasis', etc.).

        Retourne
        --------
        dict : Effets définis pour la case.
        """
        effets = {
            # Obstacles
            "mur": {"traversable": False, "bloque_balle": True, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "arbre": {"traversable": False, "bloque_balle": True, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "roche": {"traversable": False, "bloque_balle": True, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "dune": {"traversable": False, "bloque_balle": True, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},

            # Terrains traversables
            "herbe": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "sable": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "neige": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "glace": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": -1},

            # Terrains spéciaux
            "oasis": {"traversable": True, "bloque_balle": False, "soigne": True, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "buisson": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": True, "invincible": True, "boost_vitesse": 0},
            "eau": {"traversable": False, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},

            # Structures
            "pont": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "tente": {"traversable": False, "bloque_balle": True, "soigne": True, "invisible": False, "invincible": False, "boost_vitesse": 0},

            # Objets interactifs
            "chameau": {"traversable": True, "bloque_balle": True, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 1},
            "bonhomme_neige": {"traversable": True, "bloque_balle": True, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 1},

            # Zones stratégiques
            "flag1": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
            "flag2": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},

            # Zones bonus/malus
            "puit": {"traversable": False, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": -2},
            "oasis": {"traversable": True, "bloque_balle": False, "soigne": True, "invisible": False, "invincible": False, "boost_vitesse": 0},

            # Terrain inconnu
            "terrain_inconnu": {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0},
        }
        return effets.get(propriete, {"traversable": True, "bloque_balle": False, "soigne": False, "invisible": False, "invincible": False, "boost_vitesse": 0})


    def appliquer_effet(self, unite, screen):
        """
        Applique l'effet de la case à une unité (soins, invisibilité, invincibilité, etc.).

        Paramètres
        ----------
        unite : Unit
            L'unité affectée par l'effet.
        screen : pygame.Surface
            L'écran de jeu pour afficher des messages ou des effets.
        """
        if not self.effet["traversable"]:
            raise ValueError("Cette case ne peut pas être traversée !")

        # Effets de soin
        if self.effet.get("soigne"):
            unite.vie = min(unite.vie_max, unite.vie + 2)  # Soigne sans dépasser le maximum
            print(f"{unite.name} a été soigné à {unite.vie}/{unite.vie_max} points de vie.")

        # Effets de vitesse (positifs et négatifs)
        if self.effet.get("boost_vitesse") != 0:
            unite.vitesse += self.effet["boost_vitesse"]
            print(f"Vitesse de {unite.name} modifiée : {unite.vitesse}")

        # Effets d'état (invisibilité, invincibilité)
        if self.effet.get("invisible"):
            unite.invisible = True
            print(f"{unite.name} est maintenant invisible.")
        else:
            unite.invisible = False

        if self.effet.get("invincible"):
            unite.invincible = True
            print(f"{unite.name} est maintenant invincible.")
        else:
            unite.invincible = False

        # Effets de dégât feu
        if self.propriete == "feu":
            unite.vie = max(0, unite.vie - 1)  # Inflige des dégâts
            print(f"{unite.name} a subi des dégâts du feu. Vie restante : {unite.vie}/{unite.vie_max}.")
        if self.propriete == "glace":
            print(f"{unite.name} est ralenti par la glace.")

        # Vérification de victoire (drapeaux)
        if self.propriete == "flag1" and unite.team == "player2":
            show_victory_screen(screen, "enemy")
        elif self.propriete == "flag2" and unite.team == "player1":
            show_victory_screen(screen, "player")



    def bloque_balle(self):
        """
        Vérifie si cette case bloque les balles.

        Retourne
        --------
        bool : True si la case bloque les balles, sinon False.
        """
        return self.effet["bloque_balle"]

    def draw(self, screen):
        """Affiche les case sur l'écran."""
        
        # Afficher du drapeau du joueur 1 
        if self.propriete == 'flag1':
            flag_player1 = pygame.image.load("images/flag1.png")
            flag_player1 = pygame.transform.scale(flag_player1,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(flag_player1, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher du drapeau du joueur 2 
        elif self.propriete == 'flag2':
            flag_player2 = pygame.image.load("images/flag2.png")
            flag_player2 = pygame.transform.scale(flag_player2,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(flag_player2, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Map foret
        # Afficher les murs
        elif self.propriete == 'mur':
            mur = pygame.image.load("images/mur.png")
            mur = pygame.transform.scale(mur,  (CELL_SIZE, CELL_SIZE))  
            screen.blit(mur, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher les tronc
        elif self.propriete == 'tronc':
            tronc = pygame.image.load("images/tronc.png")
            tronc = pygame.transform.scale(tronc,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(tronc, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher les buisson
        elif self.propriete == 'buisson':
            buisson = pygame.image.load("images/buisson.png")
            buisson = pygame.transform.scale(buisson,  (5*CELL_SIZE, 3*CELL_SIZE))  
            screen.blit(buisson, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher les arbres
        elif self.propriete == 'arbre':
            arbre = pygame.image.load("images/arbre.png")
            arbre = pygame.transform.scale(arbre,  (3*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(arbre, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher la boue
        elif self.propriete == 'boue':
            boue = pygame.image.load("images/boue.png")
            boue = pygame.transform.scale(boue,  (8*CELL_SIZE, 5*CELL_SIZE))  
            screen.blit(boue, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher la montagne
        elif self.propriete == 'brin':
            brin = pygame.image.load("images/brin.png")
            brin= pygame.transform.scale(brin,  (CELL_SIZE, CELL_SIZE))  
            screen.blit(brin, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher le puit
        elif self.propriete == 'puit':
            puit = pygame.image.load("images/puit.png")
            puit= pygame.transform.scale(puit,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(puit, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Map desert
        # Afficher les chameaux
        elif self.propriete == 'chameau':
            chameau = pygame.image.load("images/chameau.png")
            chameau = pygame.transform.scale(chameau,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(chameau, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher les dunes
        elif self.propriete == 'dune2':
            dune = pygame.image.load("images/dune2.png")
            dune = pygame.transform.scale(dune,  (3*CELL_SIZE, 3*CELL_SIZE))  
            screen.blit(dune, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        elif self.propriete == 'tente':
            tente = pygame.image.load("images/tente.png")
            tente = pygame.transform.scale(tente,  (4*CELL_SIZE, 2.5*CELL_SIZE))  
            screen.blit(tente, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher les oasis
        elif self.propriete == 'oasis':
            palmier = pygame.image.load("images/oasis.webp")
            palmier = pygame.transform.scale(palmier,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(palmier, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()
        
        
        # Afficher les montagnes
        elif self.propriete == 'dune':
            dune = pygame.image.load("images/dune.png")
            dune = pygame.transform.scale(dune,  (4*CELL_SIZE, 3*CELL_SIZE))  
            screen.blit(dune, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

    
        # Map neige
        # Afficher les sapin
        elif self.propriete == 'sapin':
            sapin = pygame.image.load("images/sapin.png")
            sapin = pygame.transform.scale(sapin,  (3*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(sapin, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()
        # Afficher les bonhomme de neige 
        elif self.propriete == 'bonhomme':
            bonhomme = pygame.image.load("images/bonhomme.png")
            bonhomme = pygame.transform.scale(bonhomme,  (2*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(bonhomme, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

        # Afficher les feu
        elif self.propriete == 'feu':
            feu = pygame.image.load("images/feu.png")
            feu = pygame.transform.scale(feu,  (1.5*CELL_SIZE, 1.5*CELL_SIZE))  
            screen.blit(feu, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()

      

        # Afficher les glacier
        elif self.propriete == 'glace':
            glace = pygame.image.load("images/glace.jpg")
            glace  = pygame.transform.scale(glace ,  (1*CELL_SIZE, 1*CELL_SIZE))  
            screen.blit(glace , (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()
        
        
        # Afficher les montagnes
        elif self.propriete == 'montagne':
            montagne = pygame.image.load("images/montagne.png")
            montagne = pygame.transform.scale(montagne,  (5*CELL_SIZE, 2*CELL_SIZE))  
            screen.blit(montagne, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE))
            #pygame.display.flip()