from abc import ABC, abstractmethod
import random

class Competence(ABC):
    def __init__(self, nom, puissance, portee, precision,type_competence):
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
        self.precision = precision
    @abstractmethod
    def use(self, utilisateur, allies, ennemis):
        """
        Utilise la compétence sur des cibles spécifiques.
        
        :param utilisateur: L'unité utilisant la compétence
        :param allies: Liste des alliés
        :param ennemis: Liste des cibles
        :return: Message de confirmation ou d'erreur
        """
        pass
    
    def distance(self, utilisateur, cible):
        """
        Calcule la distance entre l'utilisateur et la cible.
        
        :param utilisateur: L'unité utilisant la compétence
        :param cible: La cible de la compétence
        :return: La distance entre l'utilisateur et la cible
        """
        return abs(utilisateur.x - cible.x) + abs(utilisateur.y - cible.y)
    
class Attaque(Competence):
    def __init__(self,nom, puissance, portee, precision):
        super().__init__(nom, puissance, portee, precision, type_competence="attaque")
    def use(self, utilisateur, allies, ennemis):
        for ennemie in ennemis:
            distance = self.distance(utilisateur, ennemie)
            if distance <= self.portee:
                rand = random.randint(0, 100)
                if rand <= self.precision:
                    dommage = self.puissance * utilisateur.attack_power
                    
                    ennemie.recevoir_dommage(dommage)
                    print(f"{utilisateur.name} inflige {dommage} à {ennemie.name}.")
                else:
                    print(f"{utilisateur.name} a raté {ennemie.name}.")

            
class Defense(Competence):
    def __init__(self,nom, puissance, precision):
        super().__init__(nom, puissance, precision=precision, portee=0 ,type_competence="defense")
    @abstractmethod
    def use(self, utilisateur, allies, ennemis):
        effect = utilisateur.attack_power * self.puissance 
        return effect

class ArmeAFeu(Attaque):
    def __init__(self):
        super().__init__(
            nom="Arme à feu",
            puissance=1,
            portee=5,
            precision=90
        )
class Canon(Attaque):   
    def __init__(self):
        super().__init__(
            nom="Canon",
            puissance=3,
            portee=3,
            precision=75
        )
        
class Soin(Defense):
    def __init__(self):
        super().__init__(
            nom="Soin",
            puissance=2,
            precision=100
        )
    def use(self, utilisateur, allies, ennemis):
        effect = super().use( utilisateur, allies, ennemis)
        utilisateur.health = min(utilisateur.max_health, utilisateur.health + effect)
        
class Booster(Defense):
    def __init__(self):
        super().__init__(
            nom="Booster",
            puissance=1,
            precision=100,
        )
    def use(self, utilisateur, allies, ennemis):
        _ = super().use( utilisateur, allies, ennemis)
        utilisateur.max_distance += 1
    

    