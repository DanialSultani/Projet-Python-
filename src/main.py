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
                        menu_parametres(screen)  # Ouvrir le menu de paramètres
                    elif selected_option == 2:  # Quit
                        return False  # Quitter le jeu

        # Mettre à jour l'écran
        pygame.display.flip()
        clock.tick(FPS)


def menu_parametres(screen):
    """Affiche une fenêtre avec plusieurs onglets dans le menu des paramètres."""
    # Charger l'image de fond
    try:
        fond = pygame.image.load("back.png")
        fond = pygame.transform.scale(fond, (WIDTH, HEIGHT))  # Ajuste à la taille de l'écran
    except pygame.error as e:
        print(f"Erreur lors du chargement de l'image de fond : {e}")
        return

    # Texte pour les onglets
    onglets = ["But du Jeu", "Personnages", "Cases"]
    onglet_courant = 0

    # Contenu des onglets
    contenu_but_du_jeu = [
        "Bienvenue dans Flags of Glory !",
        "Objectif :",
        "- Capturez le drapeau ennemi.",
        "- Défendez votre drapeau et gagnez des points.",
        "- Deux façons de gagner :",
        "   1. Capture du drapeau avant la fin du temps imparti.",
        "   2. Points par éliminations.",
    ]

    contenu_personnages = [
        {"nom": "Soldat", "image": "soldat.png", "description": "Vie: 6\nVitesse: 2\nPouvoir: Attaque infligeant 1 point de vie dans 8 cases.\nRapide et résistant."},
        {"nom": "Médecin", "image": "medecin.png", "description": "Vie: 1\nVitesse: 3\nPouvoir: Guérison de 2 points de vie dans 8 cases.\nRapide et agile, mais fragile."},
        {"nom": "Hélicoptère", "image": "helico.png", "description": "Vie: 2\nVitesse: 4\nPouvoir: Attaque infligeant 3 points de dégâts dans 3 cases.\nRapide mais vulnérable."},
        {"nom": "Tank", "image": "char.png", "description": "Vie: 6\nVitesse: 1\nPouvoir: Attaque infligeant 3 points de dégâts dans 2 cases.\nLent mais puissant."}
    ]

    contenu_cases = [
        {"nom": "Arbre", "image": "arbre.png", "description": "Pas traversable et bloque les balles."},
        {"nom": "Mur", "image": "mur.png", "description": "Bloquant les déplacements et les attaques."},
        {"nom": "Buisson", "image": "buisson.png", "description": "Rend les unités invisibles"},
        {"nom": "Dune", "image": "dune2.png", "description": "Pas traversable et bloque les balles."},
        {"nom": "Chameau", "image": "chameau.png", "description": "Augmente la vitesse des unités."},
        {"nom": "Bonhomme de neige", "image": "bonhomme.png", "description": "Traversable mais bloque les projectiles."},
        {"nom": "Oasis", "image": "oasis.webp", "description": "Soigne les unités."},
        {"nom": "Puits", "image": "puit.png", "description": "Soigne les unités."},
        {"nom": "Feu", "image": "feu.png", "description": "Soigne les unités."},
        {"nom": "Glace", "image": "glace.png", "description": "Surface glissante "},
        {"nom": "Sapin", "image": "sapin.png", "description": "Pas traversable et bloque les balles."},
        {"nom": "Drapeau", "image": "flag.png", "description": "Capturez-le pour gagner."}
    ]

    # Charger les images des personnages
    try:
        for personnage in contenu_personnages:
            personnage["image_chargee"] = pygame.image.load(personnage["image"])
            personnage["image_chargee"] = pygame.transform.scale(personnage["image_chargee"], (150, 150))
    except pygame.error as e:
        print(f"Erreur lors du chargement des images : {e}")
        return

    # Charger les images des cases
    try:
        for case in contenu_cases:
            case["image_chargee"] = pygame.image.load(case["image"])
            case["image_chargee"] = pygame.transform.scale(case["image_chargee"], (100, 100))  # Ajuste la taille des images
    except pygame.error as e:
        print(f"Erreur lors du chargement des images des cases : {e}")
        return

    # Police
    police_principale = pygame.font.Font("GameBoy.ttf", 20)
    police_secondaire = pygame.font.SysFont("Times New Roman", 20)

    en_cours = True
    while en_cours:
        screen.blit(fond, (0, 0))

        # Dessiner les onglets
        for i, onglet in enumerate(onglets):
            couleur = RED if i == onglet_courant else WHITE
            texte = police_principale.render(onglet, True, couleur)
            texte_rect = texte.get_rect(center=(WIDTH // len(onglets) * (i + 0.5), 40))
            screen.blit(texte, texte_rect)

        # Afficher le contenu selon l'onglet sélectionné
        if onglet_courant == 0:  # Onglet "But du jeu"
            y = 150
            for ligne in contenu_but_du_jeu:
                texte = police_secondaire.render(ligne, True, WHITE)
                screen.blit(texte, (500, y))
                y += 30

        elif onglet_courant == 1:  # Onglet "Personnages"
            x_depart = 50
            y_depart = 100
            espacement_x = 600
            espacement_y = 300

            for index, personnage in enumerate(contenu_personnages):
                colonne = index % 2
                ligne = index // 2
                
                x = x_depart + colonne * espacement_x
                y = y_depart + ligne * espacement_y
                
                screen.blit(personnage["image_chargee"], (x, y))

                texte_nom = police_principale.render(personnage["nom"], True, BLACK)
                screen.blit(texte_nom, (x + 140, y))

                description_lignes = personnage["description"].split("\n")
                for i, ligne in enumerate(description_lignes):
                    texte_ligne = police_secondaire.render(ligne, True, WHITE)
                    screen.blit(texte_ligne, (x + 140, y + 40 + i * 20))

        elif onglet_courant == 2:  # Onglet "Cases"
            x_depart = 50
            y_depart = 100
            espacement_x = 350
            espacement_y = 200

            for index, case in enumerate(contenu_cases):
                colonne = index % 4
                ligne = index // 4
                
                x = x_depart + colonne * espacement_x
                y = y_depart + ligne * espacement_y
                
                screen.blit(case["image_chargee"], (x, y))
                texte_nom = police_principale.render(case["nom"], True, BLACK)
                texte_desc = police_secondaire.render(case["description"], True, WHITE)
                screen.blit(texte_nom, (x, y + 110))
                screen.blit(texte_desc, (x-50, y + 140))

        # Gestion des événements
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_RIGHT:
                    onglet_courant = (onglet_courant + 1) % len(onglets)
                elif evenement.key == pygame.K_LEFT:
                    onglet_courant = (onglet_courant - 1) % len(onglets)
                elif evenement.key == pygame.K_RETURN:
                    en_cours = False

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