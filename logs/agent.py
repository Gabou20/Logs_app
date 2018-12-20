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

    def assurer_position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode ne retourne rien, par contre elle lancera une exception si la position source n'est pas valide.

        Warning:
            Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        Warning:
            Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Raises:
            ErreurPositionSource: Si la position source n'est pas valide.

        """
        try:
            piece_source = self.damier.recuperer_piece_a_position(position_source)

        except PieceInexistante:
            raise ErreurPositionSource("Position source invalide: aucune pièce à cet endroit")

        if not piece_source.couleur == self.couleur_joueur_courant:
            raise ErreurPositionSource("Position source invalide: pièce de mauvaise couleur")

        if self.position_source_forcee is not None:
            if not (self.position_source_forcee == position_source):
                raise ErreurPositionSource("Position source invalide: vous devez faire jouer avec la pièce en ({},{})".format(self.position_source_forcee.ligne, self.position_source_forcee.colonne))

        if not (self.damier.piece_peut_se_deplacer(position_source) or self.damier.piece_peut_faire_une_prise(position_source)):
            raise ErreurPositionSource("Aucun déplacement possible avec cette pièce")

    def assurer_position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Raises:
            ErreurPositionCible: Si la position cible n'est pas valide.

        """
        if self.position_source_forcee is None:
            position_source = self.position_source_selectionnee
        else:
            position_source = self.position_source_forcee
        deplacement_valide = self.damier.piece_peut_se_deplacer_vers(position_source, position_cible)
        saut_valide = self.damier.piece_peut_sauter_vers(position_source, position_cible)
        if self.doit_prendre:
            if not saut_valide:
                raise ErreurPositionCible("Le déplacement demandé n'est pas une prise alors qu'une prise est possible")

        if not (deplacement_valide or saut_valide):
            raise ErreurPositionCible("Position cible invalide")

    def convertir_en_chaine(self):
        chaine = "{},{},{}".format(self.nom, self.titre, self.indicatif)

        return chaine

    #def charger_dune_chaine(self, chaine):
