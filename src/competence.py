import pygame


class Competence:
    def __init__(self, nom, type_competence, puissance, portee, zone_effet=1, precision=100, effet_special=None):
        """
            Attributs
        ---------
        nom : str
            Nom de la compétence.
        type_competence : str
            Type de compétence (ex: "attaque", "soin", "defence")
        puissance : int
            Puissance de la compétence
        portee : int
            Portée maximale en cases
        zone_effet : int
            Taille de la zone d'effet
        precision : int
            Probabilité de succès de la compétence (en %, 100 par défaut)
        
        Méthodes
        --------
        utiliser(self, utilisateur, cibles, grille)
            Utilise la compétence sur des cibles spécifiques.
        _est_a_portee(self, utilisateur, cibles, grille) 
            Vérifie si toutes les cibles sont à portée.
        _touche(self)
            Détermine si l'attaque touche la cible en fonction de la précision.
        """

        self.nom = nom
        self.type_competence = type_competence
        self.puissance = puissance
        self.portee = portee
        self.zone_effet = zone_effet
        self.precision = precision

    def utiliser(self, utilisateur, cibles):
        """
        Utilise la compétence sur des cibles spécifiques.
        
        :param utilisateur: Unité qui utilise la compétence (objet)
        :param cibles: Liste des cibles affectées par la compétence (liste d'objets)
        :param grille: Référence à la grille de jeu pour vérifier les portées/positions (objet Grille)
        :return: Résultat de l'utilisation (str ou autre selon besoin)
        """
        if not self._est_a_portee(utilisateur, cibles):
            return f"{self.nom} échoue : cible hors de portée."

        if self.zone_effet > 1:
            print(f"{self.nom} affecte une zone de {self.zone_effet} cases.")
            # Parcourir les cibles dans la zone d'effet
            for cible in cibles:
                if self._touche():
                    self.appliquer_effet(utilisateur, cible)
        else:
            for cible in cibles:
                if self._touche():
                    self.appliquer_effet(utilisateur, cible)

        if self.type_competence == "attaque":
            for cible in cibles:
                if self._touche():
                    dommage = self.puissance
                    cible.recevoir_dommage(dommage)
                    print(f"{self.nom} inflige {dommage} à {cible.nom}.")
                else:
                    print(f"{self.nom} a raté {cible.nom}.")

        elif self.type_competence == "soin":
            for cible in cibles:
                soin = self.puissance
                cible.recevoir_soin(soin)
                print(f"{self.nom} soigne {soin} points de vie à {cible.nom}.")

        

        return f"{self.nom} utilisée avec succès."

    def _est_a_portee(self, utilisateur, cibles, grille):
        """
        Vérifie si toutes les cibles sont à portée.
        
        :param utilisateur: L'unité utilisant la compétence
        :param cibles: Liste des cibles
        :param grille: Grille de jeu pour vérifier les distances
        :return: True si les cibles sont à portée, False sinon
        """
        for cible in cibles:
            distance = grille.calculer_distance(utilisateur.position, cible.position)
            if distance > self.portee:
                return False
        return True

    def _touche(self):
        """
        Détermine si l'attaque touche la cible en fonction de la précision.
        :return: True si l'attaque touche, False sinon
        """
        import random
        return random.randint(1, 100) <= self.precision



    
class GestionCompetences:
    def __init__(self):
        # Initialisation du dictionnaire des compétences
        self.competences = {}

    def ajouter_competence(self, competence):
        """
        Ajoute une compétence au dictionnaire avec son nom comme clé.
        """
        self.competences[competence.nom] = competence

    def get_competence(self, nom):
        """
        Récupère une compétence par son nom.
        """
        return self.competences.get(nom)
    

# Création de la gestion des compétences
gestion_competences = GestionCompetences()

# Création des compétences (comme dans les exemples précédents)
arme_a_feu = Competence(
    nom="Arme à feu",
    type_competence="attaque",
    puissance=40,
    portee=5,
    zone_effet=1,
    precision=85
)

soin = Competence(
    nom="Soin",
    type_competence="soin",
    puissance=30,
    portee=3,
    zone_effet=3,
    precision=100
)

grenade = Competence(
    nom="Grenade",
    type_competence="attaque",
    puissance=50,
    portee=6,
    zone_effet=2,
    precision=75
)

bouclier = Competence(
    nom="Bouclier",
    type_competence="effet",
    puissance=0,
    portee=1,
    zone_effet=1,
    precision=100,
    effet_special=lambda utilisateur, cibles, grille: [
        setattr(cible, "defense", cible.defense + 20) for cible in cibles
    ]
)

# Ajout des compétences dans le gestionnaire
gestion_competences.ajouter_competence(arme_a_feu)
gestion_competences.ajouter_competence(soin)
gestion_competences.ajouter_competence(grenade)
gestion_competences.ajouter_competence(bouclier) 