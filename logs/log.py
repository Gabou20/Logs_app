__author__ = 'Gabrielle Martin-Fortier'

import time

class Log:
    """ Log d'un patrouilleur

    Attributes:
        heure_debut (float) : Heure de début de l'affectation
        heure_fin (float) : Heure de fin de l'affectation
        exterieur (str) : True si à l'extérieur, false si dans le terminal
        cote_piste (str)  : True si côté piste, false si côté ville
        log (str) : Le log

    """

    def __init__(self, heure_debut, heure_fin, terminal_exterieur, cote, log):
        """Constructeur de la classe Log. Initialise les cinq attributs de la classe.

        Args:

        """
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.terminal_exterieur = terminal_exterieur
        self.cote = cote
        self.log = log

    def afficher_log(self):
        """Méthode servant à afficher les informations du log de façon concise dans la fenêtre du patrouilleur.

            Return:
                Une chaîne de caractère à afficher
        """
        texte = ""
        if self.terminal_exterieur == "Exterieur":
            texte += "Ext. "
            texte += self.cote
            texte += " : "
        else:
            texte += "Terminal : "

        texte += self.log
        return texte
