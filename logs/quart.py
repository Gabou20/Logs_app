__author__ = 'Gabrielle Martin-Fortier'

from logs.patrouilleur import Patrouilleur
from logs.agent import Agent
from logs.exceptions import PieceInexistante, ErreurDeplacement
from logs.log import Log


class Quart:
    """Quart de travail de la sûreté, contenant des patrouilleurs ainsi que leurs affectations de la journée.

    Attributes:
        nb_patrouilleurs (int): Le nombre de patrouilleurs mobiles
        id_lieutenant (agent) : l'identité et les attributs du lieutenant
        id_204 (Patrouilleur) : l'identité et les attributs de l'agent 204
        id_205 (Patrouilleur) : l'identité et les attributs de l'agent 205
        id_206 (Patrouilleur) : l'identité et les attributs de l'agent 205
        id_207 (Patrouilleur) : l'identité et les attributs de l'agent 207
        dernier_pat_log (Patrouilleur) : Le dernier patrouilleur à avoir eu un log
    """

    def __init__(self, id_lieutenant, nb_patrouilleurs=3, id_204=None, id_205=None, id_206=None, id_207=None):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        Args:
            id_lieutenant
            nb_patrouilleurs (int) : Le nombre de patrouilleurs dans le quart
            id_204=None (Patrouilleur) :
            id_205=None (Patrouilleur)
            id_206=None (Patrouilleur)
            id_207=None (Patrouilleur)

        Raises:
            ValueError: Si le nombre de lignes, de colonnes ou de rangées est invalide.
        """
        self.nb_patrouilleurs = nb_patrouilleurs
        self.id_lieutenant = id_lieutenant
        self.id_patrouilleurs = {
            "204": id_204,
            "205": id_205,
            "206": id_206,
            "207": id_207
        }
        self.dernier_pat_log = []

    def effacer_dernier_log(self):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """

    def convertir_en_chaine(self):
        """Retourne une chaîne de caractères où chaque case est écrite sur une ligne distincte.
        Chaque ligne contient l'information suivante (respectez l'ordre et la manière de séparer les éléments):
        ligne,colonne,couleur,type

        Par exemple, un damier à deux pièces (un pion noir en (1, 2) et une dame blanche en (6, 1)) serait représenté
        par la chaîne suivante:

        1,2,noir,pion
        6,1,blanc,dame

        Cette méthode pourrait par la suite être réutilisée pour sauvegarder un damier dans un fichier.

        Returns:
            (str): La chaîne de caractères construite.

        """
        chaine = ""
        for position, piece in self.cases.items():
            chaine += "{},{},{},{}\n".format(position.ligne, position.colonne, piece.couleur, piece.type_de_piece)

        return chaine

    def charger_dune_chaine(self, chaine):
        """Vide le damier actuel et le remplit avec les informations reçues dans une chaîne de caractères. Le format de
        la chaîne est expliqué dans la documentation de la méthode convertir_en_chaine.

        Args:
            chaine (str): La chaîne de caractères.


        self.clear()
        for information_piece in chaine.split("\n"):
            if information_piece != "":
                ligne_string, colonne_string, couleur, type_piece = information_piece.split(",")
                self.cases[Position(int(ligne_string), int(colonne_string))] = Piece(couleur, type_piece)
                """

