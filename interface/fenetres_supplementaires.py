__author__ = 'Gabrielle Martin-Fortier '

from tkinter import Tk, Button, Label, Entry, Frame, Checkbutton, N, S, W, E, scrolledtext, Listbox
from logs.patrouilleur import Patrouilleur
from logs.log import Log
from random import choice
from time import sleep

class Fin_quart(Tk):
    """ Fenêtre s'ouvrant à la fin d'une partie de dames. Offre trois actions : nouvelle partie, revoir la partie et
        quitter.

        Attribute:
            fenetre (Tk): fenêtre du jeu de dame

    """

    def __init__(self, fenetre, afficher_sources):
        """ Constructeur de la classe Fin_partie. Initialise son attribut.

        Arg:
            fenetre (Tk): fenêtre du jeu de dames
        """
        super().__init__()
        self.fenetre = fenetre
        self.resizable(0, 0)
        self.title("Fin de la partie")
        if fenetre.partie.couleur_joueur_courant == "blanc":
            nom = fenetre.nom_joueur_blanc
        elif fenetre.partie.couleur_joueur_courant == "noir":
            nom = fenetre.nom_joueur_noir
        if nom == "blanc" or nom == "noir":
            phrase = "le joueur"
        else:
            phrase = ""
        etiquette = Label(self, text="Partie terminée! Le gagnant est {} {}.".format(phrase, nom),
                          fg='blue')
        nouvelle_partie = lambda: fenetre.nouvelle_partie_quitter(self, fenetre.partie.damier.n_lignes,
                                                                  fenetre.partie.damier.n_colonnes,
                                                                  fenetre.partie.damier.n_rangees, fenetre.delai,
                                                                  fenetre.nom_joueur_blanc, fenetre.nom_joueur_noir,
                                                                  afficher_sources)
        bouton_revoir_partie = Button(self, text="Revoir la partie", command=self.revoir_partie)
        bouton_nouvelle_partie = Button(self, text="Nouvelle partie",
                                        command=nouvelle_partie)
        bouton_quitter = Button(self, text="Quitter", command=fenetre.quit)
        etiquette.grid()
        bouton_nouvelle_partie.grid(pady=2)
        bouton_revoir_partie.grid(pady=2)
        bouton_quitter.grid(pady=2)


class Options(Tk):
    """ Crée la fenêtre d'options d'un jeu de dames.

    Attribute:
        fenetre (Tk): fenêtre du jeu de dames
    """

    def __init__(self, fenetre, jouer_contre_ordinateur_avant, afficher_sources_avant, afficher_cibles_avant):
        """ Constructeur de la classe Options. Initialise son attribut.

            Args:
                fenetre (Tk) : fenetre de laquelle on veut gérer les options
                jouer_contre_ordinateur_avant (bool): Information sur l'attribut fenetre.jouer_contre_ordinateur avant
                                                      l'ouverture de la fenêtre. Permet de cocher ou décocher
                                                      le bouton selon l'état actuel de l'attribut.
                afficher_sources_avant (bool): Information sur l'attribut fenetre.afficher_sources avant
                                                l'ouverture de la fenêtre. Permet de cocher ou décocher
                                                le bouton selon l'état actuel de l'attribut.
                afficher_cibles_avant (bool): Information sur l'attribut self.afficher_cibles avant
                                                l'ouverture de la fenêtre. Permet de cocher ou décocher
                                                le bouton selon l'état actuel de l'attribut.
        """
        super().__init__()
        self.resizable(0, 0)
        self.title("Options")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.fenetre = fenetre
        cadre_options = Frame(self)
        cadre_noms = Frame(self)
        cadre_dimensions = Frame(self)
        cadre_boutons = Frame(self)
        options_attributs_ordinateur = lambda: self.options_dans_attributs("ordinateur")
        options_attributs_sources = lambda: self.options_dans_attributs("sources")
        options_attributs_cibles = lambda: self.options_dans_attributs("cibles")
        bouton_jouer_contre_ordinateur = Checkbutton(cadre_options, text="Jouer contre l'ordinateur",
                                                     command=options_attributs_ordinateur)
        bouton_afficher_possibilites_sources = Checkbutton(cadre_options,
                                                           text="Afficher les pièces qui peuvent bouger",
                                                           command=options_attributs_sources)
        bouton_afficher_possibilite_cibles = Checkbutton(cadre_options,
                                                         text="Afficher les cases possibles pour la pièce sélectionnée",
                                                         command=options_attributs_cibles)
        label_delai = Label(cadre_options, text="Délai des mouvements automatiques (secondes): ")
        entree_delai_mouvement_automatique = Entry(cadre_options, width=5)
        entree_delai_mouvement_automatique.insert(0, fenetre.delai / 1000)
        label_nom_blanc = Label(cadre_noms, text="Nom du joueur blanc : ")
        label_nom_noir = Label(cadre_noms, text="Nom du joueur noir : ")
        entree_nom_blanc = Entry(cadre_noms, width=20)
        entree_nom_blanc.insert(0, self.fenetre.nom_joueur_blanc)
        entree_nom_noir = Entry(cadre_noms, width=20)
        entree_nom_noir.insert(0, self.fenetre.nom_joueur_noir)
        label_dimensions = Label(cadre_dimensions, text="Dimensions du damier :", padx=5, pady=5)
        label_lignes = Label(cadre_dimensions, text="   Nombre de lignes : ")
        label_colonnes = Label(cadre_dimensions, text="   Nombre de colonnes : ")
        label_rangees = Label(cadre_dimensions, text="   Nombre de rangées avec des pièces : ")
        entree_nombre_ligne = Entry(cadre_dimensions, width=5)
        entree_nombre_ligne.insert(0, fenetre.partie.damier.n_lignes)
        entree_nombre_colonne = Entry(cadre_dimensions, width=5)
        entree_nombre_colonne.insert(0, fenetre.partie.damier.n_colonnes)
        entree_nombre_rangees = Entry(cadre_dimensions, width=5)
        entree_nombre_rangees.insert(0, fenetre.partie.damier.n_rangees)
        if fenetre.jouer_contre_ordinateur:
            bouton_jouer_contre_ordinateur.select()
        else:
            bouton_jouer_contre_ordinateur.deselect()
        if fenetre.afficher_sources:
            bouton_afficher_possibilites_sources.select()
        else:
            bouton_afficher_possibilites_sources.deselect()
        if fenetre.afficher_cibles:
            bouton_afficher_possibilite_cibles.select()
        else:
            bouton_afficher_possibilite_cibles.deselect()
        cadre_options.grid(row=0)
        bouton_jouer_contre_ordinateur.grid(sticky=W, padx=5, pady=5)
        bouton_afficher_possibilites_sources.grid(sticky=W, padx=5, pady=5)
        bouton_afficher_possibilite_cibles.grid(sticky=W, padx=5, pady=5)
        label_delai.grid(row=3, sticky=W, padx=5, pady=5)
        entree_delai_mouvement_automatique.grid(row=3, sticky=E, padx=5, pady=5)
        cadre_dimensions.grid(row=2, sticky=W)
        label_dimensions.grid(sticky=W, padx=5, pady=5)
        label_lignes.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        entree_nombre_ligne.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        label_colonnes.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        entree_nombre_colonne.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        label_rangees.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        entree_nombre_rangees.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        cadre_noms.grid(row=1, sticky=W)
        label_nom_blanc.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        entree_nom_blanc.grid(row=0, column=1, padx=5, pady=5)
        entree_nom_noir.grid(row=1, column=1, padx=5, pady=5)
        label_nom_noir.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        cadre_boutons.grid(row=3, sticky=E)
        ok = lambda: self.fenetre.nouvelle_partie_quitter(self, entree_nombre_ligne, entree_nombre_colonne,
                                                          entree_nombre_rangees, entree_delai_mouvement_automatique,
                                                          entree_nom_blanc, entree_nom_noir, fenetre.afficher_sources)
        bouton_ok = Button(cadre_boutons, text="Nouvelle partie", command=ok)
        annuler = lambda: self.annuler(self, jouer_contre_ordinateur_avant, afficher_sources_avant,
                                       afficher_cibles_avant)
        bouton_annuler = Button(cadre_boutons, text="Annuler", command=annuler)
        bouton_annuler.grid(row=6, column=2, padx=5, pady=5, sticky=E)
        bouton_ok.grid(row=6, column=1, pady=8, sticky=E)

    def annuler(self, fenetre, jouer_contre_ordinateur_avant, afficher_sources_avant, afficher_cibles_avant):
        """ Annule les changements faits pour l'option de jouer contre l'ordinateur et ferme la fenêtre passée en
            argument.

        Args:
            fenetre: la fenêtre à détruire
            jouer_contre_ordinateur_avant: l'état de l'attribut self.jouer_contre_ordinateur avant l'ouverture de la
            fenêtre des options
        """
        self.fenetre.jouer_contre_ordinateur = jouer_contre_ordinateur_avant
        self.fenetre.afficher_sources = afficher_sources_avant
        self.fenetre.afficher_cibles = afficher_cibles_avant
        fenetre.destroy()

    def options_dans_attributs(self, poste):
        """ Change l'attribut self.jouer_contre_ordinateur.
        """


class Tous_les_logs(Tk):
    """Ouvre une nouvelle fenêtre qui affiche une liste des déplacement effectués jusqu'à maintenant dans la partie.
    """

    def __init__(self, fenetre):
        """ Constructeur de la classe Deplacements_effectues. Initialise son argument.

        Arg:
            fenetre (Tk): fenêtre du jeu de dames
        """
        super().__init__()
        self.resizable(0, 0)
        self.config(height=10)
        scroll = scrolledtext.ScrolledText(self, height=20, width=65, wrap='word')
        self.title("Déplacements effectués")
        for i in range(0, len(fenetre.partie.damier.liste_mouvements)):
            mouvement = fenetre.partie.damier.liste_mouvements[i]
            if mouvement.type_piece == "dame":
                type_piece = "Dame"
                if mouvement.couleur_piece == "noir":
                    couleur = "noire"
                else:
                    couleur = "blanche"
            else:
                type_piece = "Pion"
                if mouvement.couleur_piece == "noir":
                    couleur = "noir"
                else:
                    couleur = "blanc"
            if mouvement.position_prise is None:
                message_prise = "Aucune prise."
            else:
                prise = mouvement.position_prise
                if mouvement.type_piece_prise == "dame":
                    type_prise = "Dame"
                    feminin = "e"
                    if mouvement.couleur_prise == "noir":
                        couleur_prise = "noire"
                    else:
                        couleur_prise = "blanche"
                else:
                    type_prise = "Pion"
                    feminin = ""
                    couleur_prise = mouvement.couleur_prise
                message_prise = "{} {} pris{} en {}.".format(type_prise, couleur_prise, feminin, prise)
            deplacement = "- {} {} de {} à {}. {}\n".format(type_piece, couleur,
                                                            mouvement.position_source, mouvement.position_cible,
                                                            message_prise)
            scroll.insert('end', deplacement)
        scroll.grid()
