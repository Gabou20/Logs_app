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

    def sauvegarder(self, nom_fichier):
        """Sauvegarde une partie dans un fichier. Le fichier contiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le joueur courant doit absolument effectuer une prise à son tour.
        - Une ligne contenant None si self.position_source_forcee est à None, et la position ligne,colonne autrement.
        - Le reste des lignes correspondent au damier. Voir la méthode convertir_en_chaine du damier pour le format.

        Warning:
            Lorsqu'on écrit ou lit dans un fichier texte, il faut s'assurer de bien convertir les variables
            dans le bon type.

        Exemple de contenu de fichier :

        blanc
        True
        6,1
        1,2,noir,dame
        1,6,blanc,pion
        4,1,noir,dame
        5,2,noir,pion
        6,1,blanc,dame


        Args:
            nom_fichier (str): Le nom du fichier où sauvegarder.

        """
        with open(nom_fichier, "w") as f:
            f.write("{}\n".format(self.couleur_joueur_courant))
            f.write("{}\n".format(self.doit_prendre))
            f.write("{}\n".format(self.damier.n_lignes))
            f.write("{}\n".format(self.damier.n_colonnes))
            f.write("{}\n".format(self.damier.n_rangees))
            if self.position_source_forcee is not None:
                f.write("{},{}\n".format(self.position_source_forcee.ligne, self.position_source_forcee.colonne))
            else:
                f.write("None\n")
            f.writelines(self.damier.convertir_en_chaine())

    #def charger(self, nom_fichier):
        """Charge une partie à partir d'un fichier. Le fichier a le même format que la méthode de sauvegarde.

        Warning: N'oubliez pas de bien convertir les chaînes de caractères lues!

        Args:
            nom_fichier (str): Le nom du fichier à lire.

    
        with open(nom_fichier) as f:
            self.couleur_joueur_courant = f.readline().rstrip("\n")
            doit_prendre_string = f.readline().rstrip("\n")
            dimensions = [f.readline(), f.readline(), f.readline()]
            if doit_prendre_string == "True":
                self.doit_prendre = True
            else:
                self.doit_prendre = False

            position_string = f.readline().rstrip("\n")
            if position_string == "None":
                self.position_source_forcee = None
            else:
                ligne_string, colonne_string = position_string.split(",")
                self.position_source_forcee = Position(int(ligne_string), int(colonne_string))

            self.damier.charger_dune_chaine(f.read())
        """