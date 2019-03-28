__author__ = 'Gabrielle Martin-Fortier'

from tkinter import Tk, Label, Entry, Checkbutton, Button, W, Listbox, Frame, NSEW, Menu, filedialog, Radiobutton, \
    StringVar, END, CENTER, IntVar
from logs.log import Log
from logs.agent import Agent
from logs.exceptions import ErreurDeplacement, ErreurPositionCible, ErreurPositionSource, PieceInexistante
from logs.patrouilleur import Patrouilleur
from logs.quart import Quart
from interface.fenetres_supplementaires import FinQuart, Options, TousLesLogs, Message, GestionAgents, About
import datetime
import os


class CadreNouveauPatrouilleur(Frame):
    def __init__(self, colonne, cadre_parent, patrouilleur, commande, agents, couleur_defaut):
        #Création objets
        self.cadre = Frame(cadre_parent, bd=3, relief='ridge')

        self.couleurs_possibles = {
            "rouge": ["Indianred2", "IndianRed3"],
            "jaune": ["yellow2", "yellow3"],
            "bleu": ["DodgerBlue2", "DodgerBlue3"],
            "vert": ["chartreuse2", "chartreuse3"],
            "mauve": ["DarkOrchid2", "DarkOrchid"],
            "rose": ["maroon1", "maroon3"],
            "gris": ["light grey", "gray60"],
            "orange": ["DarkOrange2", "DarkOrange3"],
            "blanc": ["snow", "snow3"],
            "noir": ["gray37", "gray33"]
        }

        self.boutons_couleurs = {
            "rouge": None,
            "jaune": None,
            "bleu": None,
            "vert": None,
            "mauve": None,
            "rose": None,
            "gris": None,
            "orange": None,
            "blanc": None,
            "noir": None
        }

        self.cadre_pat = Frame(self.cadre)
        label_pat = Label(self.cadre_pat, text="Patrouilleur "+patrouilleur, font=("Arial", 13, "bold"))
        self.actif = IntVar()
        self.bouton = Checkbutton(self.cadre_pat, command=commande, variable=self.actif)
        self.entree_agent = Listbox(self.cadre, height=5, width=18, exportselection=0, yscrollcommand=1, font=("Arial", 13))
        for item in sorted(agents, reverse=True):
            self.entree_agent.insert(0, item)
        self.cadre_couleurs = Frame(self.cadre)
        self.valeur_couleur = StringVar()
        self.valeur_couleur.set(couleur_defaut)
        for couleur in self.couleurs_possibles:
            self.boutons_couleurs[couleur] = Radiobutton(self.cadre_couleurs, bg=self.couleurs_possibles[couleur][0],
                                                         selectcolor=self.couleurs_possibles[couleur][0],
                                                         variable=self.valeur_couleur, value=couleur, bd=2,
                                                         indicatoron=0, width=2)

        numero = 0
        while numero < 19:
            self.cadre_couleurs.columnconfigure(0, weight=1)
            numero += 2

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
        self.cadre_couleurs.grid(columnspan=5, row=8, column=1)
        self.cadre_pat.grid(columnspan=5, row=0, column=1)

        label_pat.grid(row=1, column=1, sticky=W)
        self.bouton.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        self.entree_agent.grid(row=5, column=3, padx=5, pady=5, sticky=W)
        colonne = 1
        for couleur in self.boutons_couleurs:
            self.boutons_couleurs[couleur].grid(row=8, column=colonne, padx=2, pady=2)
            colonne += 2


class Nouveau_quart(Tk):
    """ Crée la fenêtre demandant les informations pour créer un nouveau quart.
    Attribute:
    """
    def __init__(self):
        """ Constructeur de la classe Nouveau_quart.
        """
        super().__init__()
        self.resizable(0, 0)
        self.title("Nouveau quart")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.cadre_nouveau_quart = Frame(self)
        self.liste_agents = {}
        self.charger_agents()
        self.jour_nuit = StringVar()

        activer_204 = lambda: self.options_dans_attributs("204")
        activer_205 = lambda: self.options_dans_attributs("205")
        activer_206 = lambda: self.options_dans_attributs("206")
        activer_207 = lambda: self.options_dans_attributs("207")

        self.cadres_patrouilleurs = {
            "204": CadreNouveauPatrouilleur(0, self.cadre_nouveau_quart, "204", activer_204, self.liste_agents, "jaune"),
            "205": CadreNouveauPatrouilleur(1, self.cadre_nouveau_quart, "205", activer_205, self.liste_agents, "bleu"),
            "206": CadreNouveauPatrouilleur(2, self.cadre_nouveau_quart, "206", activer_206, self.liste_agents, "vert"),
            "207": CadreNouveauPatrouilleur(3, self.cadre_nouveau_quart, "207", activer_207, self.liste_agents, "rouge")
        }

        self.patrouilleurs_actifs = {
            "204": 0,
            "205": 0,
            "206": 0,
            "207": 0
        }

        self.couleurs_possibles = {
            "rouge": ["Indianred2", "IndianRed3"],
            "jaune": ["yellow2", "yellow3"],
            "bleu": ["DodgerBlue2", "DodgerBlue3"],
            "vert": ["chartreuse2", "chartreuse3"],
            "mauve": ["DarkOrchid2", "DarkOrchid"],
            "rose": ["maroon1", "maroon3"],
            "gris": ["light grey", "gray60"],
            "orange": ["DarkOrange2", "DarkOrange3"],
            "blanc": ["snow", "snow3"],
            "noir": ["gray37", "gray33"]
        }

        self.boutons_couleurs = {
            "rouge": None,
            "jaune": None,
            "bleu": None,
            "vert": None,
            "mauve": None,
            "rose": None,
            "gris": None,
            "orange": None,
            "blanc": None
        }

        self.cadre_nouveau_quart.grid(row=0, padx=5, pady=5)

        #On coche les patrouilleurs par défaut
        self.cadres_patrouilleurs["205"].bouton.select()
        self.cadres_patrouilleurs["206"].bouton.select()
        self.cadres_patrouilleurs["207"].bouton.select()
        self.options_dans_attributs("205")
        self.options_dans_attributs("206")
        self.options_dans_attributs("207")

        #Cadre options
        cadre_options = Frame(self.cadre_nouveau_quart, bd=3, relief="ridge")
        cadre_options.grid(row=0, column=0, columnspan=2)

        self.cadre_jour_nuit = Frame(self.cadre_nouveau_quart, bd=3, relief="ridge")
        self.cadre_jour_nuit.grid(row=0, column=2, columnspan=2)

        bouton_gestion_agents = Button(cadre_options, text="Gestion des agents",
                                       font=("Arial", 13, "bold"),
                                       command=self.gestion_agents)
        bouton_charger_quart = Button(cadre_options, text="Charger un quart",
                                      font=("Arial", 13, "bold"),
                                      command=self.charger_quart)

        bouton_gestion_agents.grid(row=0, column=0, padx=5, pady=5)
        bouton_charger_quart.grid(row=2, column=0, padx=5, pady=5)

        bouton_jour = Radiobutton(self.cadre_jour_nuit, selectcolor="Yellow", width=4,
                                                         variable=self.jour_nuit, value="Jour",
                                                         indicatoron=0, text="Jour", font=("Arial", 13, "bold"))
        bouton_nuit = Radiobutton(self.cadre_jour_nuit, selectcolor="Blue",width=4,
                                                         variable=self.jour_nuit, value="Nuit",
                                                         indicatoron=0, text="Nuit", font=("Arial", 13, "bold"))

        bouton_jour.grid(row=0, column=0, padx=5, pady=5)
        bouton_nuit.grid(row=0, column=1, padx=5, pady=5)

        # Lieutenant
        cadre_lieutenant = Frame(self.cadre_nouveau_quart, bd=3, relief="ridge")
        label_lieutenant = Label(cadre_lieutenant, text="Lieutenant", font=("Arial", 13, "bold"))
        cadre_couleurs = Frame(cadre_lieutenant)
        self.valeur_couleur = StringVar()
        self.valeur_couleur.set("gris")
        for couleur in self.couleurs_possibles:
            self.boutons_couleurs[couleur] = Radiobutton(cadre_couleurs, bg=self.couleurs_possibles[couleur][0],
                                                         selectcolor=self.couleurs_possibles[couleur][0],
                                                         variable=self.valeur_couleur, value=couleur, bd=2,
                                                         indicatoron=0, width=2)
        self.entree_lieutenant = Listbox(cadre_lieutenant, height=5, width=18, exportselection=0, yscrollcommand=1, font=("Arial", 13))
        for item in sorted(self.liste_agents, reverse=True):
            self.entree_lieutenant.insert(0, item)

        cadre_lieutenant.grid(columnspan=4, row=0, column=0, padx=5, pady=5)
        label_lieutenant.grid(row=0, column=0, padx=5, pady=5)
        self.entree_lieutenant.grid(row=1, column=0, padx=5, pady=5)
        cadre_couleurs.grid(row=3, column=0)

        numero = 0
        while numero < 19:
            cadre_couleurs.columnconfigure(0, weight=1)
            numero += 2

        colonne = 1
        for couleur in self.boutons_couleurs:
            self.boutons_couleurs[couleur].grid(row=8, column=colonne, padx=2, pady=2)
            colonne += 2

        cadre_bouton = Frame(self.cadre_nouveau_quart)
        cadre_bouton.grid(columnspan=4, row=3, column=0)
        bouton_ok = Button(cadre_bouton, text="Nouveau quart", command=self.nouvelle_fenetre_quart, width=60,
                           font=("Arial", 13, "bold"))
        bouton_ok.grid(padx=5, pady=5, sticky=W)

    def gestion_agents(self):
        GestionAgents(self)

    def nouvelle_fenetre_quart(self):
        nb_pat = 0
        patrouilleurs = {
            "204": None,
            "205": None,
            "206": None,
            "207": None
        }
        erreur = False
        try:
            lieutenant = self.liste_agents[self.entree_lieutenant.get(self.entree_lieutenant.curselection())]
        except:
            self.afficher_message("Lieutenant sans âme", "Vous devez choisir un agent pour le lieutenant")
            erreur = True

        for pat in self.patrouilleurs_actifs:
            if self.patrouilleurs_actifs[pat]:
                try:
                    agent = self.liste_agents[self.cadres_patrouilleurs[pat].entree_agent.get(self.cadres_patrouilleurs[pat].entree_agent.curselection())]
                    patrouilleurs[pat] = Patrouilleur(agent, pat, self.couleurs_possibles[
                        self.cadres_patrouilleurs[pat].valeur_couleur.get()])
                    nb_pat += 1
                except:
                   if not erreur:
                        self.afficher_message("Patrouilleurs anonymes",
                                              "L'un des patrouilleurs est activé mais n'a pas d'identité")
                        erreur = True

        if nb_pat == 0 and not erreur:
            self.afficher_message("Aucun patrouilleur", "L'aéroport n'est pas très sécuritaire sans aucun patrouilleur!")
        elif not (self.jour_nuit.get() == "Jour" or self.jour_nuit.get() == "Nuit") and not erreur:
            self.afficher_message("Jour ou nuit?", "Est-ce le matin ou le soir?")
        elif nb_pat != 0 and not erreur:
            quart = Quart(self.jour_nuit.get(), lieutenant, self.couleurs_possibles[self.valeur_couleur.get()][0],
                        nb_pat, patrouilleurs["204"], patrouilleurs["205"], patrouilleurs["206"], patrouilleurs["207"])
            Fenetre(quart, "Moyen")
            self.destroy()


    def options_dans_attributs(self, patrouilleur):
        self.patrouilleurs_actifs[patrouilleur] = self.cadres_patrouilleurs[patrouilleur].actif

    def charger_agents(self):
        fichier = open("agents.txt", 'r')
        chaine = fichier.read()
        if chaine != "":
            for agent in chaine.split("\n"):
                if agent !="":
                    nom, titre, indicatif = agent.split(",")
                    agent = Agent(nom, titre, indicatif)
                    self.liste_agents[agent.afficher_sans_titre()] = agent
        fichier.close()

    def afficher_message(self, titre, message):
        Message(titre, message)

    def charger_quart(self):
        fichier = filedialog.askopenfilename(parent=self, defaultextension='txt', title='Charger un quart')
        if fichier != "":
            with open(fichier, "r") as f:
                quart = Quart()
                quart.charger_dune_chaine(f.read())
                fenetre = Fenetre(quart, "Moyen")
                for pat in fenetre.quart.id_patrouilleurs:
                    if fenetre.quart.id_patrouilleurs[pat] is not None:
                        logs = fenetre.quart.id_patrouilleurs[pat].logs
                        fenetre.quart.id_patrouilleurs[pat].logs = []
                        for log in logs:
                            fenetre.creer_log_existant(pat, log)
            f.close()
        self.destroy()


class CadrePatrouilleur(Frame):
    def __init__(self, colonne, cadre_parent, poste, agent, couleur1, couleur2, grosseurs, heure_debut):

        largeur = grosseurs["Largeur cadre"]
        hauteur = grosseurs["Hauteur cadre"]
        police = grosseurs["Police"]

        #Création objets
        self.cadre = Frame(cadre_parent, height=hauteur, width=largeur, bd=3, relief='ridge', bg=couleur1)
        self.cadre_position = Frame(self.cadre, bd=3, relief="ridge", bg=couleur2, width=largeur-10, height=0.12*hauteur)
        self.cadre_logs = Frame(self.cadre, bd=1, relief='ridge', bg=couleur2, width=largeur-10, height=grosseurs["Hauteur cadre logs"])
        self.labels_logs_precedents = []

        self.label_nom = Label(self.cadre, text=agent.afficher_avec_titre(), bg=couleur1, font=("Arial", police, "bold"))
        self.label_poste = Label(self.cadre, text=poste, bg=couleur1, font=("Arial", police+6, "bold"))

        self.position_actuelle = Label(self.cadre_position)
        self.heure_position = Entry(self.cadre_position)

        #Configuration objets
        col = 0
        while col < 5:
            self.cadre_position.columnconfigure(col, weight=1)
            col += 2

        ligne = 0
        while ligne < 3:
            self.cadre_position.rowconfigure(ligne, weight=1)
            ligne += 2

        self.cadre_logs.columnconfigure(0, weight=1)
        self.cadre_logs.columnconfigure(2, weight=1)

        col = 0
        while col < 7:
            self.cadre.columnconfigure(col, weight=1)
            col += 2

        self.position_actuelle.config(text="Début de quart", bg=couleur2, font=("Arial", police-2, "bold"))
        self.heure_position.config(bd=0, bg=couleur2, font=("Arial", police-2, "bold"), width=6, justify=CENTER)
        self.heure_position.insert(END, heure_debut)

        #Grid objets
        self.cadre.grid(row=4, column=colonne, sticky=NSEW)
        self.label_poste.grid(row=0, column=0, padx=5, pady=5)
        self.label_nom.grid(row=1, column=0, padx=5, pady=5)

        self.cadre_logs.grid(row=4, column=0, padx=5)
        self.cadre_logs.grid_propagate(0)
        self.cadre_position.grid(row=3, column=0, padx=5)
        self.cadre_position.grid_propagate(0)

        self.position_actuelle.grid(row=1, column=1, padx=5, pady=5)
        self.heure_position.grid(row=1, column=3, padx=5, pady=5)


class CadreLogs:
    def __init__(self, fenetre, cadre_parent, nb_patrouilleurs, grosseurs):
        hauteur = grosseurs["Hauteur cadre"]
        largeur = grosseurs["Largeur logs"]
        self.police = grosseurs["Police"]
        self.largeur_boutons = grosseurs["Largeur boutons logs"]


        self.cadre = Frame(cadre_parent, height=hauteur, width=largeur)
        self.cadre.grid_propagate(0)
        hauteur = hauteur*0.13
        self.cadre_parent = cadre_parent
        self.cadre_parent.columnconfigure(nb_patrouilleurs, weight=1)
        self.cadre.grid(row=4, column=nb_patrouilleurs+1, sticky=NSEW)
        self.cadre_parent.columnconfigure(nb_patrouilleurs+2, weight=1)
        self.fenetre = fenetre
        self.types_logs = ["logs_terminal", "logs_exterieur_piste", "logs_exterieur_ville"]

        self.valeur_boutons = {
            "patrouilleurs": [],
            "terminal_exterieur": None,
            "cote": None
        }

        self.cadres_par_section = {
            "patrouilleurs": Frame(self.cadre, height=hauteur, width=largeur, relief="groove", bd=1),
            "terminal_exterieur": Frame(self.cadre, height=hauteur, width=largeur, relief="groove", bd=1),
            "cote": Frame(self.cadre, height=hauteur, width=largeur, relief="groove", bd=1),
            "logs_terminal": Frame(self.cadre, height=hauteur*5.3, width=largeur, relief="groove", bd=1),
            "logs_exterieur_ville": Frame(self.cadre, height=hauteur * 5.3, width=largeur, relief="groove", bd=1),
            "logs_exterieur_piste": Frame(self.cadre, height=hauteur * 5.3, width=largeur, relief="groove", bd=1),
            "note": Frame(self.cadre, height=hauteur * 5.3, width=largeur, relief="groove", bd=1)
        }

        self.boutons_par_section = {
            "patrouilleurs": {},
            "terminal_exterieur": {},
            "cote": {},
            "logs_terminal": {},
            "logs_exterieur_ville": {},
            "logs_exterieur_piste": {},
            "note": {}
        }

        self.logs_par_section = {"logs_terminal": [],
                                 "logs_exterieur_ville": [],
                                 "logs_exterieur_piste": []}
        self.charger_logs()

        #Création boutons patrouilleurs
        for patrouilleur in self.fenetre.quart.id_patrouilleurs:
            if self.fenetre.quart.id_patrouilleurs[patrouilleur] is not None:
                self.boutons_par_section["patrouilleurs"][patrouilleur] = self.creer_bouton_log(patrouilleur, "patrouilleurs")

        self.repartir_boutons("patrouilleurs")
        self.afficher_section("patrouilleurs")

        #Création boutons terminal et extérieur
        self.boutons_par_section["terminal_exterieur"]["Terminal"] = \
            self.creer_bouton_log("Terminal", "terminal_exterieur")
        self.boutons_par_section["terminal_exterieur"]["Exterieur"] = \
            self.creer_bouton_log("Exterieur", "terminal_exterieur")

        self.repartir_boutons("terminal_exterieur")
        self.afficher_section("terminal_exterieur")

        # Creation boutons cote
        self.boutons_par_section["cote"]["Piste"] = self.creer_bouton_log("Piste", "cote")
        self.boutons_par_section["cote"]["Ville"] = self.creer_bouton_log("Ville", "cote")

        self.repartir_boutons("cote")

        #Création des boutons de logs : 3 cadres différents avec des boutons différents
        for type in self.types_logs:
            self.creation_boutons_logs(type)

        #Création entrée note
        self.boutons_par_section["note"]["note"] = Entry(self.cadres_par_section["note"], font=("Arial", self.police-1))
        self.boutons_par_section["note"]["label"] = Label(self.cadres_par_section["note"], font=("Arial", self.police-1, "bold"),
                                                          text="Note : ")
        self.cadres_par_section["note"].columnconfigure(0, weight=1)
        self.cadres_par_section["note"].columnconfigure(3, weight=1)
        self.boutons_par_section["note"]["label"].grid(row=0, column=1, padx=5, pady=5)
        self.boutons_par_section["note"]["note"].grid(row=0, column=2, padx=5, pady=5)

    def repartir_boutons(self, section):
        colonne = 1
        col_log = 1
        par_deux = 0
        self.cadres_par_section[section].grid_columnconfigure(0, weight=1)
        self.cadres_par_section[section].grid_rowconfigure(0, weight=1)
        if section in self.types_logs:
            self.cadres_par_section[section].grid_columnconfigure(2, weight=1)
            self.cadres_par_section[section].grid_columnconfigure(4, weight=1)

        for nom in sorted(self.boutons_par_section[section]):
            bouton = self.boutons_par_section[section][nom]
            if section in self.types_logs:
                bouton.grid(row=par_deux+1, column=col_log, padx=5, pady=5)
                if col_log == 1:
                    col_log = 3
                else:
                    col_log = 1
                if col_log == 1:
                    self.cadres_par_section[section].grid_rowconfigure(par_deux+2, weight=1)
                    par_deux += 2
            else:
                bouton.grid(row=1, column=colonne, padx=5, pady=5)
                self.cadres_par_section[section].grid_columnconfigure(colonne + 1, weight=1)
            colonne += 2
        self.cadres_par_section[section].grid_rowconfigure(par_deux + 2, weight=1)

    def choisir_section_log(self):
        if self.valeur_boutons["terminal_exterieur"] == "Terminal":
            section = "logs_terminal"
        elif self.valeur_boutons["terminal_exterieur"] == "Exterieur" and self.valeur_boutons["cote"] == "Piste":
            section = "logs_exterieur_piste"
        else:
            section = "logs_exterieur_ville"

        return section

    #Affichage d'une section de boutons
    def afficher_section(self, section):
        if section == "logs":
            section = self.choisir_section_log()
        sections = ["patrouilleurs", "terminal_exterieur", "cote"] + self.types_logs + ["note"]
        self.cadres_par_section[section].grid(row=sections.index(section), column=0, sticky=NSEW)
        self.cadres_par_section[section].grid_propagate(0)

    def creation_boutons_logs(self, type_logs):
        for log in self.logs_par_section[type_logs]:
            self.boutons_par_section[type_logs][log] = self.creer_bouton_log(log, type_logs)
        self.repartir_boutons(type_logs)

    def updater_boutons(self, bouton, section):
        #On commence par enfoncer (ou désenfoncer) le bon bouton et mettre à jour les valeurs
        if section == "terminal_exterieur" or section == "cote":
            if bouton != self.valeur_boutons[section]:
                self.all_clear(section)
                self.valeur_boutons[section] = bouton
                self.enfoncer_bouton(self.boutons_par_section[section][bouton])
            else:
                self.relacher_bouton(self.boutons_par_section[section][bouton])
                self.valeur_boutons[section] = None

        elif section == "patrouilleurs":
            if self.valeur_boutons[section].count(bouton) != 0:
                self.valeur_boutons[section].remove(bouton)
                self.relacher_bouton(self.boutons_par_section[section][bouton])
            else:
                self.valeur_boutons[section].append(bouton)
                self.enfoncer_bouton(self.boutons_par_section[section][bouton])

        else:
            self.fenetre.creer_log(self.valeur_boutons["patrouilleurs"], self.valeur_boutons["terminal_exterieur"],
                                        self.valeur_boutons["cote"], bouton, self.boutons_par_section["note"]["note"].get())

            self.all_clear("patrouilleurs")
            self.all_clear("terminal_exterieur")
            self.all_clear("cote")
            self.all_clear("note")

        #Ensuite on ajuste les sections à afficher selon les valeurs courantes

        if section not in self.types_logs:
            self.cacher_section("logs")
            self.afficher_section("logs")
            self.afficher_section("note")

        else:
            self.cacher_section("logs")
            self.cacher_section("note")
            self.cacher_section("cote")
            self.valeur_boutons["terminal_exterieur"] = None
            self.valeur_boutons["patrouilleurs"] = []

        if self.valeur_boutons["terminal_exterieur"] == "Exterieur":
            self.afficher_section("cote")
        else:
            self.cacher_section("cote")

        if self.valeur_boutons["terminal_exterieur"] is None or (self.valeur_boutons["terminal_exterieur"] == "Exterieur" and self.valeur_boutons["cote"] is None):
            self.cacher_section("logs")
            self.cacher_section("note")
            self.boutons_par_section["logs"] = {}

    def cacher_section(self, section):
        if section != "logs":
            self.valeur_boutons[section] = None
            self.all_clear(section)
            self.cadres_par_section[section].grid_forget()
        else:
            for section_log in self.types_logs:
                self.cadres_par_section[section_log].grid_forget()


    def all_clear(self, section):
        if section != "note":
            for bouton in self.boutons_par_section[section].values():
                self.relacher_bouton(bouton)
        else:
            self.valeur_boutons["note"] = ""
            self.boutons_par_section["note"]["note"].delete(0, END)

    def enfoncer_bouton(self, bouton):
        bouton.config(relief="sunken", bg="SteelBlue1")

    def relacher_bouton(self, bouton):
        bouton.config(relief="raised", bg="gray70")

    def creer_bouton_log(self, caption, section):
        largeur = 8
        appuyer = lambda: self.updater_boutons(caption, section)
        if section == "patrouilleurs":
            largeur = 5
        if section in self.types_logs:
            largeur = self.largeur_boutons
        return Button(self.cadres_par_section[section], text=caption, font=("Arial", self.police, "bold"),
                      width=largeur, bd=3, relief="raised", bg="gray70", command=appuyer)

    def charger_logs(self):
        fichier = open("logs.txt", 'r')
        chaine = fichier.read()
        if chaine != "":
            for section in chaine.split("\n"):
                if section !="":
                    nom, liste = section.split(";")
                    for element in liste.split(","):
                        self.logs_par_section[nom].append(element)
        fichier.close()


class Fenetre(Tk):
    def __init__(self, quart, grosseur):
        super().__init__()
        #Quart courant
        self.quart = quart

        #Cadres des patrouilleurs
        self.cadres_patrouilleurs = {
            204: None,
            205: None,
            206: None,
            207: None
        }

        #Grosseurs références
        self.grosseurs_ref = {
            "Petit": {"Police": 9,
                     "Hauteur fenetre": 365,
                     "Largeur fenetre": 400 + self.quart.nb_patrouilleurs*255,
                     "Hauteur cadre": 310,
                     "Hauteur cadre logs": 190,
                     "Largeur cadre": 255,
                     "Largeur logs": 350,
                     "Largeur boutons logs": 18},
            "Moyen": {"Police": 11,
                     "Hauteur fenetre": 460,
                     "Largeur fenetre": 500 + self.quart.nb_patrouilleurs*300,
                     "Hauteur cadre": 400,
                     "Hauteur cadre logs": 265,
                     "Largeur cadre": 300,
                     "Largeur logs": 450,
                     "Largeur boutons logs": 18},
            "Gros": {"Police": 14,
                     "Hauteur fenetre": 565,
                     "Largeur fenetre": 600 + self.quart.nb_patrouilleurs*400,
                     "Hauteur cadre": 500,
                     "Hauteur cadre logs": 352,
                     "Largeur cadre": 400,
                     "Largeur logs": 550,
                     "Largeur boutons logs": 20}
        }

        #if self.quart.nb_patrouilleurs == 0:
            #self.afficher_message("Aucun patrouilleur!", "Vous n'avez ajouté aucun patrouilleur!")
            #Nouveau_quart()
            #self.destroy()
        self.grosseur = grosseur
        self.title("Gestion des logs")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(0, 0)
        self.config(height=self.grosseurs_ref[self.grosseur]["Hauteur fenetre"],
                    width=self.grosseurs_ref[self.grosseur]["Largeur fenetre"])
        self.grid_propagate(0)
        self.cadre_quart = Frame(self, height=self.grosseurs_ref[self.grosseur]["Hauteur fenetre"],
                                                     width=self.grosseurs_ref[self.grosseur]["Largeur fenetre"])
        self.cadre_quart.grid(columnspan=2, row=0, column=1, padx=5, pady=5)
        self.cadre_quart.grid_propagate(0)

        # Création des cadres pour les patrouilleurs
        self.dessiner_cadres(self.cadre_quart)

        #Et pour les boutons
        self.cadre_logs = CadreLogs(self, self.cadre_quart, self.quart.nb_patrouilleurs, self.grosseurs_ref[self.grosseur])

        # On crée le menu
        menu_logs = Menu(self)
        menu_principal = Menu(menu_logs, tearoff=0)
        menu_donnees = Menu(menu_logs, tearoff=0)
        menu_aide = Menu(menu_logs, tearoff=0)

        sauvegarder_quart = lambda: self.sauvegarder_quart(True)
        logs_effectues = lambda: self.nouveau_quart_quitter(self.grosseur)

        #Premier onglet
        menu_logs.add_cascade(label="Quart", menu=menu_principal)
        menu_principal.add_command(label="Nouveau quart", command=self.nouveau_quart)
        menu_principal.add_command(label="Sauvegarder le quart", command=sauvegarder_quart)
        menu_principal.add_command(label="Charger un quart", command=self.charger_quart)
        menu_principal.add_command(label="Annuler le dernier log", command=self.annuler_dernier_log)
        menu_principal.add_command(label="Voir tous les logs", command=logs_effectues)
        menu_principal.add_command(label="Options", command=self.options)
        menu_principal.add_command(label="Quitter", command=self.quit)

        #Deuxième onglet
        #menu_donnees.add_command(label="Gestion des agents", command=self.gerer_agents)
        #menu_donnees.add_command(label="Gestion des logs", command=self.gerer_logs)
        menu_logs.add_cascade(label="Gestion des données", menu=menu_donnees)

        #Troisieme onglet
        menu_logs.add_cascade(label="Aide", menu=menu_aide)
        menu_aide.add_command(label="Fonctionnement", command=self.aide)

        self.config(menu=menu_logs)

        self.sauvegarder_quart(False)

    #def gerer_logs(self):

    def aide(self):
        About()

    def options(self):
        Options()

    def redimensionner(self, grosseur):
        #self.cadre_quart = Frame(self, height=555, width=largeur)
        self.cadre_quart.grid(columnspan=2, row=0, column=1, padx=5, pady=5)
        self.cadre_quart.grid_propagate(0)

        # Création des cadres pour les patrouilleurs
        self.dessiner_cadres(self.cadre_quart)

        #Et pour les boutons
        self.cadre_logs = CadreLogs(self, self.cadre_quart, self.quart.nb_patrouilleurs)

    def dessiner_cadres(self, cadre_quart):
        """Initialise un quart avec les cadres pour chaque patrouilleur. Dépend du nombre de patrouilleurs.
        """
        police = self.grosseurs_ref[self.grosseur]["Police"]

        cadre_lieutenant = Frame(cadre_quart, bd=3, relief='ridge', bg=self.quart.couleur_lieutenant)
        label_lieutenant = Label(cadre_lieutenant, text=self.quart.id_lieutenant.titre, bg=self.quart.couleur_lieutenant,
                                 font=("Arial", police+1, "bold"))
        label_agent = Label(cadre_lieutenant, text=self.quart.id_lieutenant.afficher_sans_titre(),
                                bg=self.quart.couleur_lieutenant, font=("Arial", police+1, "bold"))
        if self.quart.nb_patrouilleurs !=0:
            cadre_lieutenant.grid(columnspan=self.quart.nb_patrouilleurs, row=0, column=0, padx=10, pady=10)
        label_lieutenant.grid(row=0, column=1)
        label_agent.grid(row=0, column=3)

        heures_debut = [["18:30", "18:30", "18:45", "19:00"], ["06:30", "06:30", "06:45", "07:00"]]

        colonne = 0
        for pat in sorted(self.quart.id_patrouilleurs):
            if self.quart.id_patrouilleurs[pat] is not None:
                if self.quart.jour_nuit == "Jour":
                    heure_debut = heures_debut[1][int(pat)-204]
                else:
                    heure_debut = heures_debut[0][int(pat) - 204]

                self.cadres_patrouilleurs[pat] = CadrePatrouilleur(colonne, cadre_quart, pat,
                                                                   self.quart.id_patrouilleurs[pat].agent,
                                                                   self.quart.id_patrouilleurs[pat].theme[0],
                                                                   self.quart.id_patrouilleurs[pat].theme[1],
                                                                   self.grosseurs_ref[self.grosseur], heure_debut)
                colonne += 1

    def nouveau_quart_quitter(self, grosseur):
        """ Initialise une fenêtre de nouveau quart avec les attributs de quart courant.
        """

        f = Fenetre(self.quart, grosseur)
        for pat in f.quart.id_patrouilleurs:
            if f.quart.id_patrouilleurs[pat] is not None:
                logs = f.quart.id_patrouilleurs[pat].logs
                f.quart.id_patrouilleurs[pat].logs = []
                for log in logs:
                    f.creer_log_existant(pat, log)
        self.destroy()

    def tous_les_logs(self):
        """Crée une instance de la classeTous_les_logs.
        """
        TousLesLogs()

    def annuler_dernier_log(self):
        if self.quart.dernier_pat_log == []:
            self.afficher_message("Erreur", "Aucun log à effacer")
        else:
            self.quart.effacer_dernier_log()
            for pat in self.quart.dernier_pat_log[0]:
                self.retirer_dernier_log(pat)
            self.quart.dernier_pat_log.pop(0)

    def options(self):
        """ Crée la fenêtre d'options et les cadres et boutons appropriés.
            Args:
        """
        Options(self)

    def creer_log(self, patrouilleurs, terminal_exterieur, cote, log, note):
        heure = datetime.datetime.now().strftime("%H:%M")
        nouveau_log = Log(heure, None, terminal_exterieur, cote, log, note)
        for pats in self.quart.id_patrouilleurs:
            if self.quart.id_patrouilleurs[pats] is not None:
                self.quart.id_patrouilleurs[pats].position.heure_debut = self.cadres_patrouilleurs[pats].heure_position.get()
        for pat in patrouilleurs:
            self.quart.id_patrouilleurs[pat].nouveau_log(nouveau_log, True)
            self.afficher_logs(pat)
        self.quart.dernier_pat_log.insert(0, patrouilleurs)

        self.sauvegarder_quart(False)

    def updater_heures(self):
        for pats in self.quart.id_patrouilleurs:
            if self.quart.id_patrouilleurs[pats] is not None:
                self.quart.id_patrouilleurs[pats].position.heure_debut = self.cadres_patrouilleurs[pats].heure_position.get()
                if self.cadres_patrouilleurs[pats].labels_logs_precedents != []:
                    index = 1
                    for log in self.quart.id_patrouilleurs[pats].logs:
                        log.heure_debut = self.cadres_patrouilleurs[pats].labels_logs_precedents[index].get()
                        log.heure_fin = self.cadres_patrouilleurs[pats].labels_logs_precedents[index + 2].get()
                        index += 4

    def creer_log_existant(self, patrouilleur, log):
        self.quart.id_patrouilleurs[patrouilleur].nouveau_log(log, False)
        self.afficher_logs(patrouilleur)
        #self.quart.dernier_pat_log.insert(0, patrouilleur)

    def afficher_logs(self, patrouilleur):
        #On affiche d'abord la position actuelle dans le cadre prévu à cet effet
        self.cadres_patrouilleurs[patrouilleur].position_actuelle.config(
            text=self.quart.id_patrouilleurs[patrouilleur].position.afficher_log())
        self.cadres_patrouilleurs[patrouilleur].heure_position.delete(0, END)
        self.cadres_patrouilleurs[patrouilleur].heure_position.insert(
            END, self.quart.id_patrouilleurs[patrouilleur].position.heure_debut)

        #Ensuite on affiche les logs précédents dans le cadre juste en dessous
        self.creer_label_log(self.quart.id_patrouilleurs[patrouilleur].logs[0].heure_fin, patrouilleur, True)
        self.creer_label_log("-", patrouilleur, False)
        self.creer_label_log(self.quart.id_patrouilleurs[patrouilleur].logs[0].heure_debut, patrouilleur, True)
        self.creer_label_log(self.quart.id_patrouilleurs[patrouilleur].logs[0].afficher_log(), patrouilleur, False)

        colonne = 1
        ligne = 1
        for label in self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents:
            label.grid(row=ligne, column=colonne)
            colonne += 2
            if colonne == 9:
                colonne = 1
                ligne += 1

    def retirer_dernier_log(self, patrouilleur):
        #On affiche d'abord la position actuelle dans le cadre prévu à cet effet
        self.cadres_patrouilleurs[patrouilleur].position_actuelle.config(
            text=self.quart.id_patrouilleurs[patrouilleur].position.afficher_log())
        self.cadres_patrouilleurs[patrouilleur].heure_position.delete(0, END)
        self.cadres_patrouilleurs[patrouilleur].heure_position.insert(END, self.quart.id_patrouilleurs[patrouilleur].position.heure_debut)

        #Ensuite on retire le dernier log dans la liste
        nb_labels = 4
        while nb_labels != 0:
            self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents[0].grid_forget()
            self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents.pop(0)
            nb_labels -= 1

        colonne = 1
        ligne = 1
        for label in self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents:
            label.grid(row=ligne, column=colonne)
            colonne += 2
            if colonne == 9:
                colonne = 1
                ligne += 1

    def creer_label_log(self, texte, patrouilleur, entry):
        police = self.grosseurs_ref[self.grosseur]["Police"]
        if entry:
            self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents.insert(0, Entry(
                self.cadres_patrouilleurs[patrouilleur].cadre_logs,
                bg=self.quart.id_patrouilleurs[patrouilleur].theme[1],
                width=5, bd=0,
                justify=CENTER,
                font=("Arial", police-2)))
            self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents[0].insert(END, texte)
        else:
            self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents.insert(0, Label(
                self.cadres_patrouilleurs[patrouilleur].cadre_logs,
                text=texte,
                bg=self.quart.id_patrouilleurs[patrouilleur].theme[1],
                justify=CENTER,
                font=("Arial", police-2)))

    def sauvegarder_quart(self, excel):
        """ Ouvre une fenêtre qui demande l'emplacement et le nom désirés de la partie et sauvegarde la partie.
        """
        self.updater_heures()
        fichier = str(self.quart.nom_quart + ".txt")
        if fichier != "":
            self.quart.sauvegarder(fichier)
        if excel:
            fichier = filedialog.asksaveasfilename(parent=self, initialdir=os.getcwd() + "/Quarts format Excel/",
                                                   defaultextension='xlsx', title='Quart courant',
                                                   initialfile=str(self.quart.nom_quart))
            self.quart.sauvegarder_excel(fichier)

    def charger_quart(self, fichier=None, grosseur="Moyen"):
        """ Ouvre une fenêtre qui demande la partie à charger et charge cette partie.
        """
        if fichier is None:
            fichier = filedialog.askopenfilename(parent=self, defaultextension='txt', title='Charger une partie')
        if fichier != "":
            with open(fichier, 'r+') as f:
                self.quart.charger_dune_chaine(f.read())
                self.nouveau_quart_quitter(grosseur)

    def afficher_message(self, titre, message):
        """Affiche un message d'une certaine couleur en-dessous du damier.
        Arg:
            message: le message à afficher
            couleur: la couleur du texte du message
        """
        Message(titre, message)

    def nouveau_quart(self):
        Nouveau_quart()
        self.destroy()