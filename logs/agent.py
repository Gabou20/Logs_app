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

    def afficher_agent(self):
        return self.nom + " " + self.indicatif

    #def charger_dune_chaine(self, chaine):
