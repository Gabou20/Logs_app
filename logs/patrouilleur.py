__author__ = 'Gabrielle Martin-Fortier'

from logs.log import Log
import datetime

class Patrouilleur:
    """Agent de la sûreté en poste.

    Attributes:
        agent (agent) : Nom de l'agent
        poste (int) : Numéro du poste occupé (200, 204, 205, 206 ou 207)
        position (log) : Position actuelle du patrouille
        logs (list) : Liste des logs précédents du patrouilleur

    """
    def __init__(self, agent, poste, couleur1, couleur2):
        """Constructeur de la classe Patrouilleur. Initialise les deux quatre de la classe.

        Args:
            agent (agent) : Identité du patrouilleur
            poste (int) : Numéro du poste occupé (200, 204, 205, 206 ou 207)
            position (log) : Position actuelle du patrouilleur
            logs (list) : Liste des logs précédents du patrouilleur

        """
        if poste not in {204, 205, 206, 207}:
            raise ValueError("Poste invalide. Doit être entre 200 et 207")

        self.agent = agent
        self.poste = poste
        self.couleur1 = couleur1
        self.couleur2 = couleur2
        self.position = Log("00:00", None, "Terminal", "", "Début du quart")
        self.logs = []

    def nouveau_log(self, log):
        """Ajoute un log dans la position actuelle et envoie le log précédent dans la liste de logs

        Args:
            position (Position): La position où vérifier.

        """
        self.position.heure_fin = datetime.datetime.now().strftime("%H:%M")
        self.logs.insert(0, self.position)
        self.position = log