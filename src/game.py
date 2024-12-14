import pygame
from random import *
from unit import *
from case import *
from interface import * 

# Variable globale pour verrouiller les appels à choose_map
choose_map_called = False

def main():
    global choose_map_called  # Accès à la variable globale
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

    print("Lancement du menu principal...")
    if not main_menu(screen, fresque):
        print("Quitter le jeu depuis le menu principal.")
        pygame.quit()
        exit()

    if not choose_map_called:  # Vérifie si choose_map a déjà été appelé
        print("Sélection de la carte...")
        selected_map_index = choose_map(screen)
        choose_map_called = True  # Empêche tout autre appel
        print(f"Carte choisie : {selected_map_index}")
    else:
        print("choose_map ne sera pas appelé à nouveau.")

    # Instanciation du jeu
    game = Game(screen,selected_map_index)
    # Afficher immédiatement la carte sélectionnée
    game.flip_display()

    # Boucle principale
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        game.play_game()
        # Afficher le timer
        game.draw_timer()
        # Vérifier les conditions de victoire
        if game.check_victory():  # Ajout de la vérification des conditions de victoire
            running = False  # Arrêter la boucle si une équipe a gagné
        clock.tick(FPS)

def main_menu(screen, fresque):
    """Affiche le menu principal avec les fresques comme fond."""
    # Polices
    font = pygame.font.Font("images/GameBoy.ttf", 15)

    # Textes du menu
    menu_options = ["Press ENTER to start", "SETTINGS", "QUIT"]
    selected_option = 0

    # Positions
    positions = [
        (WIDTH // 2, HEIGHT // 2 - 40),  # Position pour "Play"
        (WIDTH // 2, HEIGHT // 2),       # Position pour "Settings"
        (WIDTH // 2, HEIGHT // 2 + 40)   # Position pour "Quit"
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
            text = font.render(option, True, BLACK if i == selected_option else WHITE)
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
                return False  # Quitter le jeu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play
                        return True  # Retourne True pour lancer le jeu
                    elif selected_option == 1:  # Settings
                        settings_menu(screen)  # Ouvrir le menu de paramètres
                    elif selected_option == 2:  # Quit
                        return False  # Quitter le jeu

        # Mettre à jour l'écran
        pygame.display.flip()
        clock.tick(FPS)

def main_menu(screen, fresque):
    """Affiche le menu principal avec les fresques comme fond."""
    # Ppolices
    font = pygame.font.Font("images/GameBoy.ttf", 15)

def settings_menu(screen):
    """Affiche une fenêtre avec plusieurs onglets dans le menu des paramètres."""
    # Charger l'image de fond
    try:
        background = pygame.image.load("back.png")
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
        "   1. Capture du drapeau avant la fin du temps imparti.",
        "   2. Points par éliminations.",
    ]

    characters = [
        {"name": "Soldat", "image": "soldat.png", "description": "Vie: 6\nVitesse: 2\nPouvoir: Attaque infligeant 1 point de vie dans 8 cases.\nRapide et résistant."},
        {"name": "Médecin", "image": "medecin.png", "description": "Vie: 1\nVitesse: 3\nPouvoir: Guérison de 2 points de vie dans 8 cases.\nRapide et agile, mais fragile."},
        {"name": "Hélicoptère", "image": "helico.png", "description": "Vie: 2\nVitesse: 4\nPouvoir: Attaque infligeant 3 points de dégâts dans 3 cases.\nRapide mais vulnérable."},
        {"name": "Tank", "image": "char.png", "description": "Vie: 6\nVitesse: 1\nPouvoir: Attaque infligeant 3 points de dégâts dans 2 cases.\nLent mais puissant."}
    ]

    cases = [
        {"name": "Arbre", "image": "arbre.png", "description": "Bloque les projectiles et ne peut pas être traversé par les unités."},
        {"name": "Mur", "image": "mur.png", "description": "Structure solide bloquant les déplacements et les attaques."},
        {"name": "Buisson", "image": "buisson.png", "description": "Rend les unités invisibles aux attaques ennemies."},
        {"name": "Dune", "image": "dune.png", "description": "Accélère légèrement le déplacement des unités."},
        {"name": "Chameau", "image": "chameau.png", "description": "Augmente la vitesse des unités qui montent dessus."},
        {"name": "Bonhomme de neige", "image": "bonhomme.png", "description": "Décor traversable mais bloque les projectiles."},
        {"name": "Oasis", "image": "oasis.webp", "description": "Soigne les unités qui passent dessus."},
        {"name": "Puits", "image": "puit.png", "description": "Soigne légèrement les unités."},
        {"name": "Feu", "image": "feu.png", "description": "Inflige des dégâts aux unités traversantes."},
        {"name": "Glace", "image": "glace.png", "description": "Surface glissante modifiant les déplacements."},
        {"name": "Sapin", "image": "sapin.png", "description": "Bloque la vue et les projectiles, similaire à un arbre."},
        {"name": "Drapeau", "image": "flag.png", "description": "Objectif principal du jeu. Capturez-le pour gagner."}
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
    font = pygame.font.Font("GameBoy.ttf", 20)
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
    print("choose_map appelé")  # Trace pour confirmer l'appel
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

    selected_index = 0
    map_selected = False  # Contrôle pour quitter la boucle après sélection

    while not map_selected:
        # Dessiner le fond et les cartes
        screen.blit(background, (0, 0))

        for i, map_data in enumerate(maps):
            screen.blit(map_data["img"], positions[i])
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
                if event.key == pygame.K_LEFT:  # Déplacer le curseur à gauche
                    selected_index = (selected_index - 1) % len(maps)
                elif event.key == pygame.K_RIGHT:  # Déplacer le curseur à droite
                    selected_index = (selected_index + 1) % len(maps)
                elif event.key == pygame.K_RETURN:  # Lancer le jeu avec la carte sélectionnée
                    print(f"Carte sélectionnée : {maps[selected_index]['name']}")
                    afficher_map_selectionnee(screen, maps[selected_index])  # Affiche immédiatement la carte
                    map_selected = True  # Quitter la boucle

        pygame.display.flip()

    return selected_index






def afficher_map_selectionnee(screen, map_data):
    """Affiche immédiatement la carte sélectionnée."""
    try:
        terrain = pygame.image.load(map_data["image"])
        terrain = pygame.transform.scale(terrain, (WIDTH, HEIGHT))  # Adapter à la taille de l'écran
        screen.blit(terrain, (0, 0))
        pygame.display.flip()
    except pygame.error as e:
        print(f"Erreur lors de l'affichage de la carte sélectionnée : {e}")


        
if __name__ == "__main__":
    main()