__author__ = 'Gabrielle Martin-Fortier '

from tkinter import Tk, Button, Label, Entry, Frame, Checkbutton, W, E, scrolledtext, Listbox, END, Radiobutton, StringVar
from logs.patrouilleur import Patrouilleur
from logs.log import Log
from random import choice
from time import sleep
from logs.agent import Agent
import os

class FinQuart(Tk):
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

class GestionAgents(Tk):
    """ Crée la fenêtre d'options d'un jeu de dames.
        Attribute:
            fenetre (Tk): fenêtre du jeu de dames
        """

    def __init__(self, fenetre):
        """ Constructeur de la classe GestionAgents
            Args:
                fenetre (Tk) : fenetre actuelle de quart
        """
        super().__init__()
        self.resizable(0, 0)
        self.title("Gestion des agents")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1, minsize=10)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.fenetre = fenetre

        bouton_termine = Button(self, text="Terminé", font=("Arial", 13, "bold"), command=self.destroy)
        bouton_termine.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

        cadre_supprimer = Frame(self, relief="ridge", bd=2)
        cadre_ajouter = Frame(self, relief="ridge", bd=2)

        cadre_ajouter.grid(row=1, column=1, padx=10, pady=10)
        cadre_supprimer.grid(row=1, column=3, padx=10, pady=10)

        label_nom = Label(cadre_ajouter, text=" Nom : ", font=("Arial", 13, "bold"))
        self.entree_nom = Entry(cadre_ajouter, width=15, font=("Arial", 13))
        label_titre = Label(cadre_ajouter, text="  Titre : ", font=("Arial", 13, "bold"))
        self.entree_titre = Listbox(cadre_ajouter, height=3, exportselection=0, font=("Arial", 13), width=15)
        label_indicatif = Label(cadre_ajouter, text="Indicatif : ", font=("Arial", 13, "bold"))
        self.entree_indicatif = Entry(cadre_ajouter, width=15, font=("Arial", 13))

        self.agent_a_supprimer = Listbox(cadre_supprimer, height=6, exportselection=0,
                                             font=("Arial", 13), width=20)
        for agent_sup in sorted(self.fenetre.liste_agents, reverse=True):
            self.agent_a_supprimer.insert(0, agent_sup)

        supprimer_agent = lambda: self.supprimer_agent(self.agent_a_supprimer.get(self.agent_a_supprimer.curselection()))
        bouton_ajouter = Button(cadre_ajouter, text="Ajouter agent", font=("Arial", 13, "bold"), command=self.nouvel_agent)
        bouton_supprimer = Button(cadre_supprimer, text="Supprimer agent", font=("Arial", 13, "bold"), command=supprimer_agent)

        for item in ["Lieutenante", "Lieutenant", "Sergente", "Sergent", "Agente", "Agent"]:
            self.entree_titre.insert(0, item)
        self.entree_nom.grid(row=3, column=3, padx=5, pady=5, sticky=W)
        label_nom.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        label_titre.grid(row=6, column=1, sticky=W)
        label_indicatif.grid(row=9, column=1, sticky=W, padx=5, pady=5)
        self.entree_titre.grid(row=5, column=3, rowspan=3)
        self.entree_indicatif.grid(row=9, column=3, padx=5, pady=5, sticky=W)
        bouton_ajouter.grid(row=10, column=1, padx=5, pady=5, columnspan=3)

        self.agent_a_supprimer.grid(row=1, column=1, padx=5, pady=5)
        bouton_supprimer.grid(row=10, column=1, padx=5, pady=5, columnspan=1)

    def nouvel_agent(self):
        try:
            agent = Agent(self.entree_nom.get(),
                          self.entree_titre.get(self.entree_titre.curselection()),
                          self.entree_indicatif.get())
            if agent.afficher_sans_titre() in self.fenetre.liste_agents.values():
                Message("Agent existe déjà", "Cet agent est déjà dans la liste!")
            else:
                self.agent_a_supprimer.insert(END, agent.afficher_sans_titre())
                self.fenetre.liste_agents[agent.afficher_sans_titre()] = agent
                self.entree_nom.delete(0, END)
                self.entree_indicatif.delete(0, END)
                self.entree_titre.selection_clear(0, END)

                for cadre in self.fenetre.cadres_patrouilleurs.values():
                    cadre.entree_agent.insert(END, agent.afficher_sans_titre())
                self.fenetre.entree_lieutenant.insert(END, agent.afficher_sans_titre())
                with open("agents.txt", "a") as f:
                    f.write("\n")
                    f.writelines(agent.convertir_en_chaine())
                f.close()
        except:
            Message("Erreur", "Vous devez remplir tous les champs")

    def supprimer_agent(self, agent):
        for cadre in self.fenetre.cadres_patrouilleurs.values():
            cadre.entree_agent.delete(cadre.entree_agent.get(0, END).index(agent))
        self.fenetre.entree_lieutenant.delete(self.fenetre.entree_lieutenant.get(0, END).index(agent))
        self.agent_a_supprimer.delete(self.agent_a_supprimer.curselection())

        with open("agents.txt", "r") as f:
            lignes = f.readlines()
            if lignes[-1] == self.fenetre.liste_agents[agent].convertir_en_chaine():
                lignes[-2] = lignes[-2][:-1]
        f.close()

        with open("agents.txt", "w") as f:
            for ligne in lignes:
                if ligne not in [self.fenetre.liste_agents[agent].convertir_en_chaine() + "\n",
                                 self.fenetre.liste_agents[agent].convertir_en_chaine(), "\n"]:
                    f.write(ligne)
        f.close()


class GestionEquipes(Tk):
    """ Crée la fenêtre permettant de modifier les agents constituant une équipe

        Attribute:

        """

    def __init__(self, fenetre):
        """ Constructeur de la classe GestionEquipes

            Args:
                fenetre (Tk) : fenetre actuelle de quart
        """
        super().__init__()
        self.resizable(0, 0)
        self.title("Gestion équipes")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1, minsize=10)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.fenetre = fenetre
        self.valeur_equipe = StringVar(self)

        self.cadres_patrouilleurs = {
            "lieutenant": CadreAgent(0, "lieutenant", self, self.fenetre.liste_agents),
            "205": CadreAgent(1, "205", self, self.fenetre.liste_agents),
            "206": CadreAgent(2, "206", self, self.fenetre.liste_agents),
            "207": CadreAgent(3, "207", self, self.fenetre.liste_agents)
        }

        self.boutons_equipes = {
            "A": None,
            "B": None,
            "C": None,
            "D": None
        }

        self.cadre_boutons = Frame(self)
        self.cadre_boutons.grid(row=0, column=0, columnspan=4)

        for equipe in ["A", "B", "C", "D"]:
            self.boutons_equipes[equipe] = Radiobutton(self.cadre_boutons,
                                                       text="Equipe "+ equipe,
                                                       variable=self.valeur_equipe, value=equipe, bd=2,
                                                       indicatoron=0, width=8, font=("Arial", 13, "bold"))

        self.boutons_equipes["A"].grid(row=0, column=0, padx=5, pady=5)
        self.boutons_equipes["B"].grid(row=0, column=1, padx=5, pady=5)
        self.boutons_equipes["C"].grid(row=0, column=2, padx=5, pady=5)
        self.boutons_equipes["D"].grid(row=0, column=3, padx=5, pady=5)

        bouton_termine = Button(self, text="Sauvegarder les changements", font=("Arial", 13, "bold"),
                                command=self.sauvegarder_changements)
        bouton_termine.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

    def charger_equipe(self, equipe):
        lieutenant, a_205, a_206, a_207 = self.fenetre.liste_equipes[equipe]["lieutenant"], \
                                          self.fenetre.liste_equipes[equipe]["205"], \
                                          self.fenetre.liste_equipes[equipe]["206"], \
                                          self.fenetre.liste_equipes[equipe]["207"]

        index_205 = self.cadres_patrouilleurs["205"].entree_agent.get(0, END).index(a_205.afficher_sans_titre())
        self.cadres_patrouilleurs["205"].entree_agent.select_clear(0, END)
        self.cadres_patrouilleurs["205"].entree_agent.select_set(index_205)
        self.cadres_patrouilleurs["205"].entree_agent.see(index_205)

        index_206 = self.cadres_patrouilleurs["206"].entree_agent.get(0, END).index(a_206.afficher_sans_titre())
        self.cadres_patrouilleurs["206"].entree_agent.select_clear(0, END)
        self.cadres_patrouilleurs["206"].entree_agent.select_set(index_206)
        self.cadres_patrouilleurs["206"].entree_agent.see(index_206)

        index_207 = self.cadres_patrouilleurs["207"].entree_agent.get(0, END).index(a_207.afficher_sans_titre())
        self.cadres_patrouilleurs["207"].entree_agent.select_clear(0, END)
        self.cadres_patrouilleurs["207"].entree_agent.select_set(index_207)
        self.cadres_patrouilleurs["207"].entree_agent.see(index_207)

        index_207 = self.cadres_patrouilleurs["lieutenant"].entree_agent.get(0, END).index(lieutenant.afficher_sans_titre())
        self.cadres_patrouilleurs["lieutenant"].entree_agent.select_clear(0, END)
        self.cadres_patrouilleurs["lieutenant"].entree_agent.select_set(index_207)
        self.cadres_patrouilleurs["lieutenant"].entree_agent.see(index_207)

    def sauvegarder_changements(self):
        if self.valeur_equipe.get() == "":
            Message("Erreur", "Vous devez sélectionner une équipe!")
        else:
            lieutenant, a_205, a_206, a_207 = self.cadres_patrouilleurs["lieutenant"].entree_agent.get(self.cadres_patrouilleurs["lieutenant"].entree_agent.curselection()), \
                                              self.cadres_patrouilleurs["205"].entree_agent.get(self.cadres_patrouilleurs["205"].entree_agent.curselection()), \
                                              self.cadres_patrouilleurs["206"].entree_agent.get(self.cadres_patrouilleurs["206"].entree_agent.curselection()), \
                                              self.cadres_patrouilleurs["207"].entree_agent.get(self.cadres_patrouilleurs["207"].entree_agent.curselection())
            with open("equipes.txt", "r") as f:
                numero_ligne = 0
                lignes = f.readlines()
                f.close()

            for ligne in lignes:
                if ligne == self.valeur_equipe.get()+"\n":
                    numero_ligne = lignes.index(ligne)
            lignes[numero_ligne + 1] = self.fenetre.liste_agents[lieutenant].convertir_en_chaine() + "\n"
            lignes[numero_ligne + 2] = self.fenetre.liste_agents[a_205].convertir_en_chaine() + "\n"
            lignes[numero_ligne + 3] = self.fenetre.liste_agents[a_206].convertir_en_chaine() + "\n"
            lignes[numero_ligne + 4] = self.fenetre.liste_agents[a_207].convertir_en_chaine() + "\n"

            with open("equipes.txt", "w") as f:
                for ligne in lignes:
                    f.write(ligne)
                f.close()


class CadreAgent():
    def __init__(self, colonne, poste, cadre_parent, liste_agents):
        # Création objets
        self.cadre = Frame(cadre_parent, bd=3, relief='ridge')

        self.cadre_pat = Frame(self.cadre)
        label_pat = Label(self.cadre_pat, text=poste, font=("Arial", 13, "bold"))
        self.entree_agent = Listbox(self.cadre, height=5, width=18, exportselection=0, yscrollcommand=1,
                                    font=("Arial", 13))
        for item in sorted(liste_agents, reverse=True):
            self.entree_agent.insert(0, item)

        numero = 0
        while numero < 5:
            self.cadre.columnconfigure(numero, weight=1)
            self.cadre.rowconfigure(numero, weight=1)
            numero += 2
        self.cadre.rowconfigure(6, weight=1)

        self.cadre_pat.columnconfigure(0, weight=1)
        self.cadre_pat.columnconfigure(2, weight=1)
        self.cadre_pat.columnconfigure(4, weight=1)
        self.cadre_pat.rowconfigure(0, weight=1)
        self.cadre_pat.rowconfigure(2, weight=1)

        self.cadre.grid(row=1, column=colonne, sticky=W, padx=5, pady=5)
        self.cadre_pat.grid(columnspan=5, row=0, column=1)

        label_pat.grid(row=1, column=1, sticky=W)
        self.entree_agent.grid(row=5, column=3, padx=5, pady=5, sticky=W)


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


class TousLesLogs(Tk):
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
        self.title("Registre des logs du quart")


class Message(Tk):
    """Ouvre une nouvelle fenêtre qui affiche une liste des déplacement effectués jusqu'à maintenant dans la partie.
    """

    def __init__(self, titre, message):
        """ Constructeur de la classe Deplacements_effectues. Initialise son argument.

        Arg:
            fenetre (Tk): fenêtre du jeu de dames
        """
        super().__init__()
        self.resizable(0, 0)
        self.title(titre)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.message = Label(self, text=message, font=("Arial", 14))
        self.message.grid(row=1, column=1, padx=10, pady=10)

        ok = lambda: self.destroy()
        self.ok = Button(self, text="ok", command=ok, font=("Arial", 15), width=8, bd=2)
        self.ok.grid(row=3, column=1, padx=10, pady=1)
