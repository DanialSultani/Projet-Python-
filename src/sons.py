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
        }

    def play(self, name):
        self.sounds[name].play()
