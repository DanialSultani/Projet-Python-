import pygame

class SoundEffect:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'click': pygame.mixer.Sound("Projet-Python-/sons/click.mp3"),
            'game over': pygame.mixer.Sound("Projet-Python-/sons/game over.mp3"),
            'marche': pygame.mixer.Sound("Projet-Python-/sons/marche.mp3"),
            'soin': pygame.mixer.Sound("Projet-Python-/sons/soin.mp3"),
            'tire': pygame.mixer.Sound("Projet-Python-/sons/tire.mp3"),
            'victoir': pygame.mixer.Sound("Projet-Python-/sons/victoir.mp3"),
            'fond': pygame.mixer.Sound("Projet-Python-/sons/fond.mp3"),
            'fondforet': pygame.mixer.Sound("Projet-Python-/sons/fondforet.mp3"),
        }

    
    def play(self, name, loop=0):
            """
            Joue un effet sonore.

            :param name: Nom du son (clé du dictionnaire `sounds`).
            :param loop: Nombre de boucles (-1 pour une boucle infinie, 0 pour une seule fois).
            """
            if name in self.sounds:
                self.sounds[name].play(loops=loop)  # Jouer le son avec boucle
            else:
                print(f"Erreur : le son '{name}' n'existe pas.")

    def set_volume(self, name, volume):
            """
            Définit le volume d'un son.

            :param name: Nom du son (clé du dictionnaire `sounds`).
            :param volume: Volume du son (entre 0.0 et 1.0).
            """
            if name in self.sounds:
                self.sounds[name].set_volume(volume)
            else:
                print(f"Erreur : le son '{name}' n'existe pas.")

