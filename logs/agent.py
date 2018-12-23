__author__ = 'Gabrielle Martin-Fortier'
from logs.exceptions import ErreurPositionCible, ErreurPositionSource, PieceInexistante


class Agent:
    """Agent de la sûreté aéroportuaire

    Attributes:
        nom (string) : nom de l'agent
        titre (string) : titre de l'agent (agent, sergent, lieutenant)
        indicatif (int) : Indicatif de l'agent

    """
    def __init__(self, nom, titre, indicatif):
        """Constructeur de la classe Agent.

        """
        self.nom = nom
        self.titre = titre
        self.indicatif = indicatif

    def convertir_en_chaine(self):
        chaine = "{},{},{}".format(self.nom, self.titre, self.indicatif)

        return chaine

    def afficher_sans_titre(self):
        return self.nom + " " + self.indicatif


    def afficher_avec_titre(self):
        return self.titre + "  " + self.nom + "  " + self.indicatif
