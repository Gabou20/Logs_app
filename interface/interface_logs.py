__author__ = 'Gabrielle Martin-Fortier'

from tkinter import Tk, Label, Entry, Checkbutton, Button, W, N, Listbox, Frame, NSEW, Menu, filedialog, Radiobutton, StringVar
from logs.log import Log
from logs.agent import Agent
from logs.exceptions import ErreurDeplacement, ErreurPositionCible, ErreurPositionSource, PieceInexistante
from logs.patrouilleur import Patrouilleur
from logs.quart import Quart
from interface.fenetres_supplementaires import Fin_quart, Options, Tous_les_logs, Message
import datetime

class Cadre_nouveau_patrouilleur(Frame):
    def __init__(self, colonne, cadre_parent, patrouilleur, commande):
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
            "blanc": ["snow", "snow3"]
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

        self.cadre_pat = Frame(self.cadre)
        label_pat = Label(self.cadre_pat, text="Patrouilleur "+patrouilleur)
        bouton = Checkbutton(self.cadre_pat, command=commande)
        label_nom = Label(self.cadre, text=" Nom : ")
        self.entree_nom = Entry(self.cadre, width=20)
        label_titre = Label(self.cadre, text="  Titre : ")
        self.entree_titre = Listbox(self.cadre, height=3, exportselection=0)
        for item in ["Lieutenant(e)", "Sergent(e)", "Agent(e)"]:
            self.entree_titre.insert(0, item)
        self.entree_titre.select_set(0)
        label_indicatif = Label(self.cadre, text="Indicatif : ")
        self.entree_indicatif = Entry(self.cadre, width=20)
        self.cadre_couleurs = Frame(self.cadre)
        self.valeur_couleur = StringVar()
        self.valeur_couleur.set("rouge")
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
        bouton.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        self.entree_nom.grid(row=3, column=3, padx=5, pady=5, sticky=W)
        label_nom.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        label_titre.grid(row=5, column=1, sticky=W)
        self.entree_titre.grid(row=5, column=3, padx=5, pady=5, sticky=W)
        label_indicatif.grid(row=7, column=1, sticky=W, padx=5, pady=5)
        self.entree_indicatif.grid(row=7, column=3, padx=5, pady=5, sticky=W)
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

        activer_204 = lambda: self.options_dans_attributs("204")
        activer_205 = lambda: self.options_dans_attributs("205")
        activer_206 = lambda: self.options_dans_attributs("206")
        activer_207 = lambda: self.options_dans_attributs("207")

        self.cadres_patrouilleurs = {
            "204": Cadre_nouveau_patrouilleur(0, self.cadre_nouveau_quart, "204", activer_204),
            "205": Cadre_nouveau_patrouilleur(1, self.cadre_nouveau_quart, "205", activer_205),
            "206": Cadre_nouveau_patrouilleur(2, self.cadre_nouveau_quart, "206", activer_206),
            "207": Cadre_nouveau_patrouilleur(3, self.cadre_nouveau_quart, "207", activer_207)
        }
        self.patrouilleurs_actifs = {
            "204": False,
            "205": False,
            "206": False,
            "207": False
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
            "blanc": ["snow", "snow3"]
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

        # Lieutenant
        cadre_lieutenant = Frame(self.cadre_nouveau_quart, bd=3, relief='ridge')
        label_lieutenant = Label(cadre_lieutenant, text="Lieutenant")
        label_nom_lieutenant = Label(cadre_lieutenant, text="Nom : ")
        self.entree_nom_lieutenant = Entry(cadre_lieutenant, width=20)
        label_indicatif_lieutenant = Label(cadre_lieutenant, text="Indicatif : ")
        self.entree_indicatif_lieutenant = Entry(cadre_lieutenant, width=20)
        cadre_couleurs = Frame(cadre_lieutenant)
        self.valeur_couleur = StringVar()
        self.valeur_couleur.set("gris")
        for couleur in self.couleurs_possibles:
            self.boutons_couleurs[couleur] = Radiobutton(cadre_couleurs, bg=self.couleurs_possibles[couleur][0],
                                                         selectcolor=self.couleurs_possibles[couleur][0],
                                                         variable=self.valeur_couleur, value=couleur, bd=2,
                                                         indicatoron=0, width=2)

        cadre_lieutenant.grid(columnspan=4, row=0, column=0, padx=5, pady=5)
        label_lieutenant.grid(columnspan=3, row=0, column=2, padx=5, pady=5, sticky=W)
        label_nom_lieutenant.grid(columnspan=2, row=1, column=0, sticky=W, padx=5, pady=5)
        self.entree_nom_lieutenant.grid(columnspan=4, row=1, column=2, padx=5, pady=5)
        label_indicatif_lieutenant.grid(columnspan=2, row=2, column=0, sticky=W, padx=5, pady=5)
        self.entree_indicatif_lieutenant.grid(columnspan=3, row=2, column=3, padx=5, pady=5)
        cadre_couleurs.grid(row=3, column=0, columnspan=5)

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
        bouton_ok = Button(cadre_bouton, text="Nouveau quart", command=self.nouvelle_fenetre_quart, width=60)
        bouton_ok.grid(padx=5, pady=5, sticky=W)

    def nouvelle_fenetre_quart(self):
        nb_pat = 0
        patrouilleurs = {
            "204": None,
            "205": None,
            "206": None,
            "207": None
        }
        lieutenant = Agent(self.entree_nom_lieutenant.get(), "Lieutenant(e)", self.entree_indicatif_lieutenant.get())

        for pat in self.patrouilleurs_actifs:
            if self.patrouilleurs_actifs[pat]:
                agent = Agent(self.cadres_patrouilleurs[pat].entree_nom.get(), self.cadres_patrouilleurs[pat].entree_titre.get(self.cadres_patrouilleurs[pat].entree_titre.curselection()), self.cadres_patrouilleurs[pat].entree_indicatif.get())
                patrouilleurs[pat] = Patrouilleur(agent, pat, self.couleurs_possibles[self.cadres_patrouilleurs[pat].valeur_couleur.get()])
                nb_pat += 1
        if nb_pat == 0:
            self.afficher_message("Aucun patrouilleur!", "Il doit y avoir au moins un patrouilleur.")
        else:
            quart = Quart(lieutenant, self.couleurs_possibles[self.valeur_couleur.get()][1],
                        nb_pat, patrouilleurs["204"], patrouilleurs["205"], patrouilleurs["206"], patrouilleurs["207"])
            Fenetre(quart)
            self.destroy()

    def options_dans_attributs(self, patrouilleur):
        if self.patrouilleurs_actifs[patrouilleur]:
            self.patrouilleurs_actifs[patrouilleur] = False
        else:
            self.patrouilleurs_actifs[patrouilleur] = True

    def afficher_message(self, titre, message):
        """Affiche un message d'une certaine couleur en-dessous du damier.

        Arg:
            message: le message à afficher
            couleur: la couleur du texte du message
        """
        Message(titre, message)


class CadrePatrouilleur(Frame):
    def __init__(self, colonne, cadre_parent, poste, agent, couleur1, couleur2):
        #Création objets
        self.cadre = Frame(cadre_parent, height=500, width=400, bd=3, relief='ridge')
        self.cadre_position = Frame(self.cadre)
        self.cadre_logs = Frame(self.cadre)
        self.labels_logs_precedents = []

        self.label_poste = Label(self.cadre)
        self.label_titre = Label(self.cadre, width=8)
        self.label_nom = Label(self.cadre, width=8)
        self.label_indicatif = Label(self.cadre, width=8)

        self.position_actuelle = Label(self.cadre_position)
        self.heure_position = Label(self.cadre_position)

        #Configuration objets
        self.cadre.config(bg=couleur1)
        self.cadre_position.config(bd=3, relief="ridge", bg=couleur2, width=353, height=40)
        self.cadre_position.columnconfigure(0, weight=1)
        self.cadre_position.columnconfigure(2, weight=1)
        self.cadre_position.columnconfigure(4, weight=1)
        self.cadre_position.rowconfigure(0, weight=1)
        self.cadre_position.rowconfigure(2, weight=1)
        self.cadre_logs.config(bd=1, relief='ridge', bg=couleur2, width=353, height=342)
        self.cadre_logs.columnconfigure(0, weight=1)
        self.cadre_logs.columnconfigure(2, weight=1)
        self.cadre_logs.columnconfigure(4, weight=1)
        self.cadre_logs.columnconfigure(5, weight=1)
        self.cadre_logs.columnconfigure(7, weight=1)

        self.label_poste.config(text=poste, bg=couleur1, font=("Arial", 20, "bold"))
        self.label_titre.config(text=agent.titre, bg=couleur1, font=("Arial", 14, "bold"))
        self.label_nom.config(text=agent.nom, bg=couleur1, font=("Arial", 14, "bold"))
        self.label_indicatif.config(text=agent.indicatif, bg=couleur1, font=("Arial", 14, "bold"))

        self.position_actuelle.config(text="Début de quart", bg=couleur2, font=("Arial", 13, "bold"))
        self.heure_position.config(bd=1, text="00:00", bg=couleur2, font=("Arial", 13, "bold"))

        #Grid objets
        self.cadre.grid(row=4, column=colonne, sticky=NSEW)
        self.label_poste.grid(row=0, column=1, padx=10, pady=10)
        self.label_titre.grid(row=1, column=0, padx=10, pady=10)
        self.label_nom.grid(row=1, column=1, padx=10, pady=10)
        self.label_indicatif.grid(row=1, column=2, padx=10, pady=10)

        self.cadre_logs.grid(row=4, columnspan=3, column=0)
        self.cadre_logs.grid_propagate(0)
        self.cadre_position.grid(row=3, column=0, columnspan=3)
        self.cadre_position.grid_propagate(0)

        self.position_actuelle.grid(row=1, column=1, padx=5, pady=5)
        self.heure_position.grid(row=1, column=3, padx=5, pady=5)


class CadreLogs:
    def __init__(self, fenetre, cadre_parent, nb_patrouilleurs):
        self.cadre = Frame(cadre_parent, height=500, width=600)
        self.cadre.grid_propagate(0)
        largeur = 600
        hauteur = 60
        self.cadre_parent = cadre_parent
        self.cadre_parent.columnconfigure(nb_patrouilleurs, weight=1)
        self.cadre.grid(row=4, column=nb_patrouilleurs+1, sticky=NSEW)
        self.cadre_parent.columnconfigure(nb_patrouilleurs+2, weight=1)
        self.fenetre = fenetre
        self.types_logs = ["logs_terminal", "logs_exterieur_piste", "logs_exterieur_ville"]

        self.valeur_boutons = {
            "patrouilleurs": [],
            "terminal_exterieur": None,
            "cote": None,
        }

        self.cadres_par_section = {
            "patrouilleurs": Frame(self.cadre, height=hauteur, width=largeur, relief="groove", bd=1),
            "terminal_exterieur": Frame(self.cadre, height=hauteur, width=largeur, relief="groove", bd=1),
            "cote": Frame(self.cadre, height=hauteur, width=largeur, relief="groove", bd=1),
            "logs_terminal": Frame(self.cadre, height=hauteur*5.3, width=largeur, relief="groove", bd=1),
            "logs_exterieur_ville": Frame(self.cadre, height=hauteur * 5.3, width=largeur, relief="groove", bd=1),
            "logs_exterieur_piste": Frame(self.cadre, height=hauteur * 5.3, width=largeur, relief="groove", bd=1)
        }

        self.boutons_par_section = {
            "patrouilleurs": {},
            "terminal_exterieur": {},
            "cote": {},
            "logs_terminal": {},
            "logs_exterieur_ville": {},
            "logs_exterieur_piste": {}
        }

        self.logs_par_section = {
            "logs_terminal": ["Patrouille", "Intervention", "Ronde niveau 0",
                         "Ronde niveaux 1-2", "Ronde stat. étagé",
                         "Vol non fouillé", "Vol international"],
            "logs_exterieur_ville": ["Patrouille", "Intervention", "Ronde stationnements", "Ronde barrières",
                                "Opération CSR", "Interception", "Constat d'infraction"],
            "logs_exterieur_piste": ["Patrouille", "Intervention", "Opération DCZR/DAZR", "Ronde périmètre", "Infraction"]
        }

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
                bouton.grid(row=par_deux+1, column=col_log, padx=10, pady=10)
                if col_log == 1:
                    col_log = 3
                else:
                    col_log = 1
                if col_log == 1:
                    self.cadres_par_section[section].grid_rowconfigure(par_deux+2, weight=1)
                    par_deux += 2
            else:
                bouton.grid(row=1, column=colonne, padx=10, pady=10, sticky=NSEW)
                self.cadres_par_section[section].grid_columnconfigure(colonne + 1, weight=1)
            colonne += 2
        self.cadres_par_section[section].grid_rowconfigure(par_deux + 2, weight=1)

    def choisir_section_log(self):
        section = ""
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
        sections = ["patrouilleurs", "terminal_exterieur", "cote"] + self.types_logs
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
                                        self.valeur_boutons["cote"], bouton)
            self.all_clear("patrouilleurs")
            self.all_clear("terminal_exterieur")
            self.all_clear("cote")

        #Ensuite on ajuste les sections à afficher selon les valeurs courantes

        if section not in self.types_logs:
            self.cacher_section("logs")
            self.afficher_section("logs")

        else:
            self.cacher_section("logs")
            self.cacher_section("cote")
            self.valeur_boutons["terminal_exterieur"] = None
            self.valeur_boutons["patrouilleurs"] = []

        if self.valeur_boutons["terminal_exterieur"] == "Exterieur":
            self.afficher_section("cote")
        else:
            self.cacher_section("cote")

        if self.valeur_boutons["terminal_exterieur"] is None or (self.valeur_boutons["terminal_exterieur"] == "Exterieur" and self.valeur_boutons["cote"] is None):
            self.cacher_section("logs")
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
        for bouton in self.boutons_par_section[section].values():
            self.relacher_bouton(bouton)

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
            largeur = 20
        return Button(self.cadres_par_section[section], text=caption, font=("Arial", 14, "bold"),
                      height=1, width=largeur, bd=3, relief="raised", bg="gray70", command=appuyer)

    #def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.

        # Calcul de la nouvelle dimension des cases.
        #self.n_pixels_par_case = min(event.height // self.nb_lignes)

        # On supprime les anciennes cases et on ajoute les nouvelles.
        #self.delete('case')
        #self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        #self.delete('piece')
        #self.dessiner_pieces()


class Fenetre(Tk):
    def __init__(self, quart):
        super().__init__()
        #Quart courant
        self.quart = quart
        if self.quart.nb_patrouilleurs == 0:
            self.afficher_message("Aucun patrouilleur!", "Vous n'avez ajouté aucun patrouilleur!")
            Nouveau_quart()
            #self.destroy()
        largeur = 600 + self.quart.nb_patrouilleurs*400
        self.title("Gestion des logs")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(0, 0)
        self.config(height=565, width=largeur)
        self.grid_propagate(0)
        self.cadre_quart = Frame(self, height=555, width=largeur)
        self.cadre_quart.grid(columnspan=2, row=0, column=1, padx=5, pady=5)
        self.cadre_quart.grid_propagate(0)

        #Cadres des patrouilleurs
        self.cadres_patrouilleurs = {
            204: None,
            205: None,
            206: None,
            207: None
        }

        # Création des cadres pour les patrouilleurs
        self.dessiner_cadres(self.cadre_quart)
        #Et pour les boutons
        self.cadre_logs = CadreLogs(self, self.cadre_quart, self.quart.nb_patrouilleurs)

        # On crée le menu
        menu_jeu = Menu(self)
        menu_principal = Menu(menu_jeu, tearoff=0)
        nouveau_quart = lambda: self.nouveau_quart_quitter()
        sauvegarder_quart = lambda: self.sauvegarder_quart()
        charger_quart = lambda: self.charger_quart()
        annuler_dernier_log = lambda: self.annuler_dernier_log()
        logs_effectues = lambda: self.nouveau_quart_quitter()
        options = lambda: self.nouveau_quart_quitter()

        menu_principal.add_command(label="Nouveau quart", command=nouveau_quart)
        menu_principal.add_command(label="Sauvegarder le quart", command=sauvegarder_quart)
        menu_principal.add_command(label="Charger un quart", command=charger_quart)
        menu_principal.add_command(label="Annuler le dernier log", command=annuler_dernier_log)
        menu_principal.add_command(label="Voir tous les logs", command=logs_effectues)
        menu_principal.add_command(label="Options", command=options)
        menu_principal.add_command(label="Quitter", command=self.quit)
        menu_jeu.add_cascade(label="Menu", menu=menu_principal)
        self.config(menu=menu_jeu)

    def dessiner_cadres(self, cadre_quart):
        """Initialise un quart avec les cadres pour chaque patrouilleur. Dépend du nombre de patrouilleurs.
        """
        cadre_lieutenant = Frame(cadre_quart, bd=3, relief='ridge', bg=self.quart.couleur_lieutenant)
        label_lieutenant = Label(cadre_lieutenant, text="Lieutenant(e) : ", bg=self.quart.couleur_lieutenant, font=("Arial", 14, "bold"))
        label_nom_lieutenant = Label(cadre_lieutenant, text=self.quart.id_lieutenant.nom, bg=self.quart.couleur_lieutenant, font=("Arial", 14, "bold"))
        label_indicatif = Label(cadre_lieutenant, text=self.quart.id_lieutenant.indicatif, bg=self.quart.couleur_lieutenant, font=("Arial", 14, "bold"))
        if self.quart.nb_patrouilleurs !=0:
            cadre_lieutenant.grid(columnspan=self.quart.nb_patrouilleurs, row=0, column=0, padx=10, pady=10)
        label_lieutenant.grid(row=0, column=1)
        label_nom_lieutenant.grid(row=0, column=2, sticky=N)
        label_indicatif.grid(row=0, column=3)

        colonne = 0
        for pat in sorted(self.quart.id_patrouilleurs):
            if self.quart.id_patrouilleurs[pat] is not None:
                self.cadres_patrouilleurs[pat] = CadrePatrouilleur(colonne, cadre_quart, pat,
                                                                   self.quart.id_patrouilleurs[pat].agent,
                                                                   self.quart.id_patrouilleurs[pat].theme[0],
                                                                   self.quart.id_patrouilleurs[pat].theme[1])
                colonne += 1

    def dessiner_boutons_cote(self, cadre):
        cadre_boutons_cote = Frame(cadre)
        cadre_boutons_cote.grid(row=6, column=self.quart.nb_patrouilleurs)

        bouton_piste = self.creer_bouton_log("Piste", cadre_boutons_cote, 7)
        bouton_ville = self.creer_bouton_log("Ville", cadre_boutons_cote, 7)
        bouton_piste.grid(row=0, column=0, padx=10, pady=10)
        bouton_piste.grid(row=0, column=1, padx=10, pady=10)

    def nouveau_quart_quitter(self):
        """ Initialise une fenêtre de nouveau quart avec les attributs de quart courant.
        """

        f = Fenetre(self.quart)

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
        Tous_les_logs()

    def annuler_dernier_log(self):
        """ Déplace la dernière pièce déplacée à sa position d'origine.
        Si le dernier mouvement était une prise, la pièce prise est redessinée.
        """
        if self.quart.dernier_pat_log == []:
            self.afficher_message("Erreur", "Le dernier log a déjà été effacé!")
        else:
            self.quart.effacer_dernier_log()
            for pat in self.quart.dernier_pat_log:
                self.retirer_dernier_log(pat)
            self.quart.dernier_pat_log = []

    def options(self):
        """ Crée la fenêtre d'options et les cadres et boutons appropriés.

            Args:

        """
        Options(self)

    def creer_log(self, patrouilleurs, terminal_exterieur, cote, log):
        heure = datetime.datetime.now().strftime("%H:%M")
        nouveau_log = Log(heure, None, terminal_exterieur, cote, log)
        for pat in patrouilleurs:
            self.quart.id_patrouilleurs[pat].nouveau_log(nouveau_log)
            self.afficher_logs(pat)
        self.quart.dernier_pat_log = patrouilleurs

    def creer_log_existant(self, patrouilleur, log):
        self.quart.id_patrouilleurs[patrouilleur].nouveau_log(log)
        self.afficher_logs(patrouilleur)
        self.quart.dernier_pat_log = [patrouilleur]

    def afficher_logs(self, patrouilleur):
        #On affiche d'abord la position actuelle dans le cadre prévu à cet effet
        self.cadres_patrouilleurs[patrouilleur].position_actuelle.config(
            text=self.quart.id_patrouilleurs[patrouilleur].position.afficher_log())
        self.cadres_patrouilleurs[patrouilleur].heure_position.config(
            text=self.quart.id_patrouilleurs[patrouilleur].position.heure_debut)

        #Ensuite on affiche les logs précédents dans le cadre juste en dessous
        self.creer_label_log(self.quart.id_patrouilleurs[patrouilleur].logs[0].heure_fin, patrouilleur)
        self.creer_label_log("-", patrouilleur)
        self.creer_label_log(self.quart.id_patrouilleurs[patrouilleur].logs[0].heure_debut, patrouilleur)
        self.creer_label_log(self.quart.id_patrouilleurs[patrouilleur].logs[0].afficher_log(), patrouilleur)

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
        self.cadres_patrouilleurs[patrouilleur].heure_position.config(
            text=self.quart.id_patrouilleurs[patrouilleur].position.heure_debut)

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

    def creer_label_log(self, texte, patrouilleur):
        self.cadres_patrouilleurs[patrouilleur].labels_logs_precedents.insert(0, Label(
            self.cadres_patrouilleurs[patrouilleur].cadre_logs,
            text=texte,
            bg=self.quart.id_patrouilleurs[patrouilleur].theme[1],
            font=("Arial", 12)))

    def sauvegarder_quart(self):
        """ Ouvre une fenêtre qui demande l'emplacement et le nom désirés de la partie et sauvegarde la partie.
        """
        fichier = filedialog.asksaveasfilename(defaultextension='txt', title='Quart courant')
        if fichier != "":
            self.quart.sauvegarder(fichier)

    def charger_quart(self):
        """ Ouvre une fenêtre qui demande la partie à charger et charge cette partie.
        """
        fichier = filedialog.askopenfilename(defaultextension='txt', title='Charger une partie')
        if fichier != "":
            f = open(fichier, 'r')
            self.quart.charger_dune_chaine(f.read())
            self.nouveau_quart_quitter()

            #f.readline()
            #dimensions = [int(f.readline()), int(f.readline()), int(f.readline())]
            #self.nouvelle_partie(dimensions[0], dimensions[1], dimensions[2], self.delai,
                                 #self.nom_joueur_blanc, self.nom_joueur_noir, self.afficher_sources)
            #self.partie.charger(fichier)
            #self.partie.damier.liste_mouvements = []
            #self.attente_clic = True
            #self.nombre_prises_par_tour = [0]
            #self.partie.numero_tour = 0
            #self.canvas_damier.delete(self, 'piece')
            #self.canvas_damier.dessiner_pieces()
            #self.afficher_couleur_courante()

    def afficher_message(self, titre, message):
        """Affiche un message d'une certaine couleur en-dessous du damier.

        Arg:
            message: le message à afficher
            couleur: la couleur du texte du message
        """
        Message(titre, message)
