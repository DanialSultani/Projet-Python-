
import pygame
from random import *
from unit import *
from case import *
from interface import * 


def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flags of Glory")
    
    # Charger les fresques
    try:
        fresque = [
            pygame.image.load("images/fresque_1.png"),
            pygame.image.load("images/fresque_2.png"),
            pygame.image.load("images/fresque_3.png"),
        ]
        fresque = [
            pygame.transform.scale(f, (int( WIDTH), HEIGHT))
            for f in fresque
        ]
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        return

    # Afficher le menu principal avec les fresques en fond
    if not main_menu(screen, fresque):
        pygame.quit()
        exit()

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        game.play_game()
        clock.tick(FPS)

def main_menu(screen, fresque):
    """Affiche le menu principal avec les fresques comme fond."""
    # Ppolices
    font = pygame.font.Font("images/GameBoy.ttf", 15)

    # Textes du menu
    menu_options = ["Press ENTER to start ", "SETTINGS","QUIT"]
    selected_option = 0

    # Positions 
    positions = [
        (WIDTH // 2, HEIGHT // 2 -40),  # Position pour "Play"
        (WIDTH // 2, HEIGHT // 2 ),   # Position pour "Settings"
        (WIDTH // 2, HEIGHT // 2 +40)   # Position pour "Settings"
    ]

    clock = pygame.time.Clock()
    running = True

    # Choisir une fresque aléatoire pour le fond
    current_fresque = choice(fresque)

    while running:
        # Dessiner la fresque comme fond
        screen.blit(current_fresque, (0, 0))

        # Afficher les options du menu
        for i, (option, position) in enumerate(zip(menu_options, positions)):
            text = font.render(option, True, BLACK)
            text_rect = text.get_rect(center=position)
            screen.blit(text, text_rect)

            # Dessiner le triangle indicateur
            if i == selected_option:
                triangle_x = text_rect.left - 15
                triangle_y = text_rect.centery
                pygame.draw.polygon(screen, BLACK, [
                    (triangle_x, triangle_y),
                    (triangle_x - 10, triangle_y - 8),
                    (triangle_x - 10, triangle_y + 8)
                ])

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        choose_map(screen)
                        return True  # Lancer le jeu
                    elif selected_option == 1:
                        settings_menu(screen)  # Ouvrir le menu de paramètres
                    elif selected_option == 2:
                        return False  # Ouvrir le menu de paramètres

        # Mettre à jour l'écran
        pygame.display.flip()
        clock.tick(FPS)

def settings_menu(screen):
    """Affiche une fenêtre avec plusieurs onglets dans le menu des paramètres."""
    # Charger l'image de fond
    try:
        background = pygame.image.load("images/back.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajuste à la taille de l'écran
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image de fond : {e}")
        return
    
    # Texte pour les onglets
    tabs = ["But du Jeu", "Personnages", "Cases"]
    current_tab = 0

    # Contenu des onglets
    game_goal_text = [
        "Bienvenue dans Flags of Glory !",
        "Objectif :",
        "- Capturez le drapeau ennemi.",
        "- Défendez votre drapeau et gagnez des points.",
        "- Deux façons de gagner :",
        "   1. Capture du drapeau avant la fin du temps impartie.",
        "   2. Points par éliminations.",
    ]

    characters = [
        {"name": "Soldat", "image": "images/soldat.png", "description": "Vie: 6 \n Vitesse: 2 \n Pouvoir: Attaque infligeant 1 point de vie dans 8 cases.\n Rapide et resistant "},
        {"name": "Medecin", "image": "images/medecin.png", "description": "Vie: 1 \n Vitesse: 3 \n Pouvoir: guérison de 2 points de vie dans 8 cases. \n Rapide et agile, mais fragile."},
        {"name": "Helicoptere ", "image": "images/helico.png", "description": "Vie: 2 \n Vitesse: 4 \n Pouvoir: Attaque infligeant des dégâts de 3 points dans 3 cases.\n Lent mais avec plus de vie."},
        {"name": "Tank", "image": "images/char.png", "description": "Vie: 6 \n Vitesse: 1 \n Pouvoir: Attaque infligeant des dégâts de 3 points de vie dans 2 cases.\n Lent mais avec plus de vie."},

        
    ]

    cases = [
        {"name": "Arbre", "image": "images/arbre.png", "description": "Rapide et agile, mais fragile."},
        {"name": "buisson", "image": "images/buisson.png", "description": "Rapide et agile, mais fragile."},
        {"name": "oasis ", "image": "images/oasis.webp", "description": "Lent mais avec plus de vie."},
        {"name": "Bonhomme de neige", "image": "images/bonhomme.png", "description": "Rapide et agile, mais fragile."},

    ]

    # Charger les images des personnages
    try:
        for char in characters:
            char["loaded_image"] = pygame.image.load(char["image"])
            char["loaded_image"] = pygame.transform.scale(char["loaded_image"], (150, 150))
    except pygame.error as e:
        print(f"Erreur lors du chargement des images : {e}")
        return
    # Charger les images des cases
    try:
        for case in cases:
            case["loaded_image"] = pygame.image.load(case["image"])
            case["loaded_image"] = pygame.transform.scale(case["loaded_image"], (100, 100))  # Ajuste la taille des images
    except pygame.error as e:
        print(f"Erreur lors du chargement des images des cases : {e}")
        return

    # Police
    font = pygame.font.Font("images/GameBoy.ttf", 20)
    small_font = pygame.font.SysFont("Times New Roman", 20)

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Dessiner les onglets
        for i, tab in enumerate(tabs):
            color = RED if i == current_tab else WHITE
            text = font.render(tab, True, color)
            text_rect = text.get_rect(center=(WIDTH // len(tabs) * (i + 0.5), 40))
            screen.blit(text, text_rect)

        # Afficher le contenu selon l'onglet sélectionné
        if current_tab == 0:  # Onglet "But du jeu"
            y = 150
            for line in game_goal_text:
                text = small_font.render(line, True, WHITE)
                screen.blit(text, (500, y))
                y += 30

        elif current_tab == 1:  # Onglet "Personnages"
            x_start = 50  # Position de départ pour la première colonne
            y_start = 100  # Position de départ pour la première ligne
            x_gap = 600  # Espace horizontal entre les colonnes
            y_gap = 300  # Espace vertical entre les lignes

            for index, char in enumerate(characters):
                # Calculer la position (colonne et ligne)
                col = index % 2  # Colonne (0 ou 1)
                row = index // 2  # Ligne (0, 1, 2, etc.)
                
                x = x_start + col * x_gap
                y = y_start + row * y_gap
                
                # Afficher l'image
                screen.blit(char["loaded_image"], (x, y))

                # Afficher le nom
                text_name = font.render(char["name"], True, BLACK)
                screen.blit(text_name, (x+140, y ))  # Décalage sous l'image
                
                # Afficher les caractéristiques (description)
                description_lines = char["description"].split("\n")  # Découper les lignes
                for i, line in enumerate(description_lines):
                    text_line = small_font.render(line, True, WHITE)
                    screen.blit(text_line, (x+140, y + 40 + i * 20))  # Décalage progressif pour chaque ligne

        elif current_tab == 2:  # Onglet "Cases"
            x_start = 50  # Position de départ pour la première colonne
            y_start = 100  # Position de départ pour la première ligne
            x_gap = 300  # Espace horizontal entre les colonnes
            y_gap = 150  # Espace vertical entre les lignes

            for index, case in enumerate(cases):
                # Calculer la position (colonne et ligne)
                col = index % 4  # Colonne (0, 1, 2)
                row = index // 4  # Ligne (0, 1, 2, etc.)
                
                x = x_start + col * x_gap
                y = y_start + row * y_gap
                
                # Afficher l'image
                screen.blit(case["loaded_image"], (x, y))
                # Afficher le nom et la description
                text_name = font.render(case["name"], True, BLACK)
                text_desc = small_font.render(case["description"], True, WHITE)
                screen.blit(text_name, (x, y + 110))  # Nom en dessous de l'image
                screen.blit(text_desc, (x, y + 140))  # Description en dessous du nom

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_tab = (current_tab + 1) % len(tabs)  # Passer à l'onglet suivant
                elif event.key == pygame.K_LEFT:
                    current_tab = (current_tab - 1) % len(tabs)  # Passer à l'onglet précédent
                elif event.key == pygame.K_RETURN:
                    running = False  # Quitter les paramètres

        # Mettre à jour l'affichage
        pygame.display.flip()

def choose_map(screen):
    """Permet au joueur de choisir une carte avant de lancer le jeu."""
    # Charger l'image de fond
    try:
        background = pygame.image.load("images/back.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajuste à la taille de l'écran
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image de fond : {e}")
        return
    
    # Charger les images des cartes
    maps = [
        {"name": "Foret", "image": "images/fresque_1.png"},
        {"name": "Desert", "image": "images/fresque_2.png"},
        {"name": "Neige", "image": "images/fresque_3.png"},
    ]

    # Charger et redimensionner les images des cartes
    for map_data in maps:
        try:
            map_data["img"] = pygame.image.load(map_data["image"])
            map_data["img"] = pygame.transform.scale(map_data["img"], (300, 200))
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image pour la carte {map_data['name']}: {e}")
            return None

    # Positions pour afficher les cartes
    positions = [
        (WIDTH // 4 - 150, HEIGHT // 2 - 100),
        (WIDTH // 2 - 150, HEIGHT // 2 - 100),
        (3 * WIDTH // 4 - 150, HEIGHT // 2 - 100),
    ]

    # Police pour le texte
    font = pygame.font.Font("images/GameBoy.ttf", 20)

    # Curseur initial
    selected_index = 0

    running = True

    while running:
        # Fond d'écran noir
        screen.blit(background, (0, 0))

        # Afficher chaque carte et son nom
        for i, map_data in enumerate(maps):
            screen.blit(map_data["img"], positions[i])
            # Couleur du texte : en surbrillance si sélectionnée
            color = BLACK if i == selected_index else WHITE
            text = font.render(map_data["name"], True, color)
            text_rect = text.get_rect(center=(positions[i][0] + 150, positions[i][1] + 220))
            screen.blit(text, text_rect)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Déplacer le czurseur à gauche
                    selected_index = (selected_index - 1) % len(maps)
                elif event.key == pygame.K_RIGHT:  # Déplacer le curseur à droite
                    selected_index = (selected_index + 1) % len(maps)
                elif event.key == pygame.K_RETURN:  # Lancer le jeu avec la carte sélectionnée
                    return selected_index

        # Mettre à jour l'affichage
        pygame.display.flip()
        
if __name__ == "__main__":
    main()
