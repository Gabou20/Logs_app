__author__ = 'Jean-Francis Roy, Valérie Dupont, Gabrielle Martin-Fortier'


class PieceInexistante(Exception):
    """Une exception indiquant qu'aucune pièce n'a pu être récupérée à la position choisie.

    """
    pass


class ErreurDeplacement(Exception):
    """Une exception indiquant qu'une erreur est survenue pendant le déplacement.

    """
    pass


class ErreurPositionSource(Exception):
    """Une exception indiquant que la position source est invalide.

    """
    pass


class ErreurPositionCible(Exception):
    """ Une exception indiquant que la position cible est invalide.

    """
    pass