__author__ = 'Gabrielle Martin-Fortier'

from logs.patrouilleur import Patrouilleur
from logs.agent import Agent
from logs.exceptions import PieceInexistante, ErreurDeplacement
from logs.log import Log
import datetime


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

    def __init__(self, id_lieutenant, couleur_lieutenant, nb_patrouilleurs=3, id_204=None, id_205=None, id_206=None, id_207=None):
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
        self.couleur_lieutenant = couleur_lieutenant
        self.dernier_pat_log = []
        self.nom_quart = datetime.datetime.now().strftime("%B-%d-%Y %Hh%M")

    def effacer_dernier_log(self):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """
        for pat in self.dernier_pat_log:
            self.id_patrouilleurs[pat].effacer_dernier_log()

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
        chaine = "{},{},{},{}\n".format(self.nb_patrouilleurs, self.couleur_lieutenant,
                                        self.id_lieutenant.convertir_en_chaine(),
                                        self.dernier_pat_log)

        for patrouilleur in self.id_patrouilleurs.values():
            if patrouilleur is not None:
                chaine += patrouilleur.convertir_en_chaine()

        return chaine

    def charger_dune_chaine(self, chaine):
        """Vide le damier actuel et le remplit avec les informations reçues dans une chaîne de caractères. Le format de
        la chaîne est expliqué dans la documentation de la méthode convertir_en_chaine.

        Args:
            chaine (str): La chaîne de caractères.
        """
        for vieux_pats in self.id_patrouilleurs:
            self.id_patrouilleurs[vieux_pats] = None
        numero_de_ligne = 0
        patrouilleur = False
        for information_quart in chaine.split("\n"):
            if information_quart in ["204", "205", "206", "207"]:
                numero_de_ligne = 1
                poste = information_quart
                patrouilleur = True
            if information_quart != "":
                if numero_de_ligne == 0:
                    nb_patrouilleurs, self.couleur_lieutenant, nom_lieutenant, titre_lieutenant, indicatif_lieutenant, \
                    self.dernier_pat_log = information_quart.split(",")
                    self.nb_patrouilleurs = int(nb_patrouilleurs)
                elif patrouilleur:
                    if numero_de_ligne == 2:
                        nom, titre, indicatif, couleur1, couleur2 = information_quart.split(",")
                        self.id_patrouilleurs[poste] = \
                            Patrouilleur(Agent(nom, titre, indicatif), poste, [couleur1, couleur2])
                    elif numero_de_ligne != 1:
                        nouveau_log = Log()
                        nouveau_log.charger_dune_chaine(information_quart)
                        self.id_patrouilleurs[poste].logs.insert(0, nouveau_log)
            numero_de_ligne += 1

        self.id_lieutenant = Agent(nom_lieutenant, titre_lieutenant, indicatif_lieutenant)
        for pat in self.id_patrouilleurs:
            if self.id_patrouilleurs[pat] is not None:
                self.id_patrouilleurs[pat].position = self.id_patrouilleurs[pat].logs[0]
                self.id_patrouilleurs[pat].logs.pop(0)

    def sauvegarder(self, nom_fichier):
        """Sauvegarde une partie dans un fichier. Le fichier contiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le joueur courant doit absolument effectuer une prise à son tour.
        - Une ligne contenant None si self.position_source_forcee est à None, et la position ligne,colonne autrement.
        - Le reste des lignes correspondent au damier. Voir la méthode convertir_en_chaine du damier pour le format.

        Exemple de contenu de fichier :

        Args:
            nom_fichier (str): Le nom du fichier où sauvegarder.

        """
        with open(nom_fichier, "w") as f:
            f.writelines(self.convertir_en_chaine())