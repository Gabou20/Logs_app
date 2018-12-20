__author__ = 'Gabrielle Martin-Fortier'

from tkinter import Tk, Canvas, Label, Entry, Checkbutton, Button, W, N, Listbox, Frame, NSEW, S, Menu, filedialog
from logs.log import Log
from logs.agent import Agent
from logs.exceptions import ErreurDeplacement, ErreurPositionCible, ErreurPositionSource, PieceInexistante
from logs.patrouilleur import Patrouilleur
from logs.quart import Quart
from interface.fenetres_supplementaires import Fin_quart, Options, Tous_les_logs
import datetime

class Nouveau_quart(Tk):
    """ Crée la fenêtre demandant les informations pour créer un nouveau quart.

    Attribute:
    """
    actif_204 = False
    actif_205 = False
    actif_206 = False
    actif_207 = False

    def nouvelle_fenetre_quart(self, nom_lieutenant, indicatif_lieutenant,
                               nom_204="204", titre_204=None, indicatif_204=None,
                               nom_205="205", titre_205=None, indicatif_205=None,
                               nom_206="206", titre_206=None, indicatif_206=None,
                               nom_207="207", titre_207=None, indicatif_207=None):
        nb_pat = 0
        lieutenant = Agent(nom_lieutenant, "Lieutenant", indicatif_lieutenant)

        if self.actif_204:
            agent_204 = Agent(nom_204, titre_204, indicatif_204)
            patrouilleur_204 = Patrouilleur(agent_204, "204", ["yellow2", "yellow3"])
            nb_pat += 1
        else:
            patrouilleur_204 = None

        if self.actif_205:
            agent_205 = Agent(nom_205, titre_205, indicatif_205)
            patrouilleur_205 = Patrouilleur(agent_205, "205", ["IndianRed2", "IndianRed3"])
            nb_pat += 1
        else:
            patrouilleur_205 = None

        if self.actif_206:
            agent_206 = Agent(nom_206, titre_206, indicatif_206)
            patrouilleur_206 = Patrouilleur(agent_206, "206", ["DodgerBlue2", "DodgerBlue3"])
            nb_pat += 1
        else:
            patrouilleur_206 = None

        if self.actif_207:
            agent_207 = Agent(nom_207, titre_207, indicatif_207)
            patrouilleur_207 = Patrouilleur(agent_207, "207", ["Chartreuse3", "Chartreuse4"])
            nb_pat += 1
        else:
            patrouilleur_207 = None

        quart = Quart(lieutenant, nb_pat, patrouilleur_204, patrouilleur_205, patrouilleur_206, patrouilleur_207)
        Fenetre(quart)
        self.destroy()

    def options_dans_attributs(self, agent):
        if agent == 204:
            if self.actif_204:
                self.actif_204 = False
            else:
                self.actif_204 = True

        elif agent == 205:
            if self.actif_205:
                self.actif_205 = False
            else:
                self.actif_205 = True

        elif agent == 206:
            if self.actif_206:
                self.actif_206 = False
            else:
                self.actif_206 = True

        elif agent == 207:
            if self.actif_207:
                self.actif_207 = False
            else:
                self.actif_207 = True


    def __init__(self):
        """ Constructeur de la classe Nouveau_quart.
        """
        super().__init__()
        self.resizable(0, 0)
        self.title("Nouveau quart")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        cadre_nouveau_quart = Frame(self)

        activer_204 = lambda: self.options_dans_attributs(204)
        activer_205 = lambda: self.options_dans_attributs(205)
        activer_206 = lambda: self.options_dans_attributs(206)
        activer_207 = lambda: self.options_dans_attributs(207)

        cadre_nouveau_quart.grid(row=0, padx=5, pady=5)
        cadre_nouveau_quart.columnconfigure(0, weight=1)
        cadre_nouveau_quart.columnconfigure(2, weight=1)

        #Lieutenant
        cadre_lieutenant = Frame(self, bd=3, relief='ridge')
        label_lieutenant = Label(cadre_lieutenant, text="Lieutenant")
        label_nom_lieutenant = Label(cadre_lieutenant, text="Nom : ")
        entree_nom_lieutenant = Entry(cadre_lieutenant, width=20)
        label_indicatif_lieutenant = Label(cadre_lieutenant, text="Indicatif : ")
        entree_indicatif_lieutenant = Entry(cadre_lieutenant, width=20)

        cadre_lieutenant.grid(columnspan=2, row=0, column=1, padx=5, pady=5)
        label_lieutenant.grid(columnspan=3, row=0, column=2, padx=5, pady=5, sticky=W)
        label_nom_lieutenant.grid(columnspan=2, row=1, column=0, sticky=W, padx=5, pady=5)
        entree_nom_lieutenant.grid(columnspan=4, row=1, column=2, padx=5, pady=5)
        label_indicatif_lieutenant.grid(columnspan=2, row=2, column=0, sticky=W, padx=5, pady=5)
        entree_indicatif_lieutenant.grid(columnspan=3, row=2, column=3, padx=5, pady=5)

        #204
        cadre_204 = Frame(self, bd=3, relief='ridge')
        label_204 = Label(cadre_204, text="Patrouilleur 204")
        bouton_204 = Checkbutton(cadre_204, command=activer_204)
        label_nom_204 = Label(cadre_204, text="Nom : ")
        entree_nom_204 = Entry(cadre_204, width=20)
        label_titre_204 = Label(cadre_204, text="Titre : ")
        entree_titre_204 = Listbox(cadre_204, height=3, exportselection=0)
        for item in ["Lieutenant(e)", "Sergent(e)", "Agent(e)"]:
            entree_titre_204.insert(0, item)
        entree_titre_204.select_set(0)
        label_indicatif_204 = Label(cadre_204, text="Indicatif : ")
        entree_indicatif_204 = Entry(cadre_204, width=20)

        cadre_204.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        label_204.grid(columnspan=4, row=0, column=1)
        bouton_204.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        entree_nom_204.grid(columnspan=4, row=3, column=3, padx=5, pady=5)
        label_nom_204.grid(columnspan=2, row=3, column=0, sticky=W, padx=5, pady=5)
        label_titre_204.grid(row=5, column=0)
        entree_titre_204.grid(rowspan=3, columnspan=4, row=4, column=3, padx=5, pady=5)
        label_indicatif_204.grid(columnspan=3, row=7, column=0, sticky=W, padx=5, pady=5)
        entree_indicatif_204.grid(columnspan=3, row=7, column=3, padx=5, pady=5)

        #205
        cadre_205 = Frame(self, bd=3, relief='ridge')
        label_205 = Label(cadre_205, text="Patrouilleur 205")
        bouton_205 = Checkbutton(cadre_205, command=activer_205)
        label_nom_205 = Label(cadre_205, text="Nom : ")
        entree_nom_205 = Entry(cadre_205, width=20)
        label_titre_205 = Label(cadre_205, text="Titre : ")
        entree_titre_205 = Listbox(cadre_205, height=3, exportselection=0)
        for item in ["Lieutenant(e)", "Sergent(e)", "Agent(e)"]:
            entree_titre_205.insert(0, item)
        entree_titre_205.select_set(0)
        label_indicatif_205 = Label(cadre_205, text="Indicatif : ")
        entree_indicatif_205 = Entry(cadre_205, width=20)

        cadre_205.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        label_205.grid(columnspan=4, row=0, column=1)
        bouton_205.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        entree_nom_205.grid(columnspan=4, row=3, column=3, padx=5, pady=5)
        label_nom_205.grid(columnspan=2, row=3, column=0, sticky=W, padx=5, pady=5)
        label_titre_205.grid(row=5, column=0)
        entree_titre_205.grid(rowspan=3, columnspan=4, row=4, column=3, padx=5, pady=5)
        label_indicatif_205.grid(columnspan=3, row=7, column=0, sticky=W, padx=5, pady=5)
        entree_indicatif_205.grid(columnspan=3, row=7, column=3, padx=5, pady=5)

        #206
        cadre_206 = Frame(self, bd=3, relief='ridge')
        label_206 = Label(cadre_206, text="Patrouilleur 206")
        bouton_206 = Checkbutton(cadre_206, command=activer_206)
        label_nom_206 = Label(cadre_206, text="Nom : ")
        entree_nom_206 = Entry(cadre_206, width=20)
        label_titre_206 = Label(cadre_206, text="Titre : ")
        entree_titre_206 = Listbox(cadre_206, height=3, exportselection=0)
        for item in ["Lieutenant(e)", "Sergent(e)", "Agent(e)"]:
            entree_titre_206.insert(0, item)
        entree_titre_206.select_set(0)
        label_indicatif_206 = Label(cadre_206, text="Indicatif : ")
        entree_indicatif_206 = Entry(cadre_206, width=20)

        cadre_206.grid(row=1, column=2, sticky=W, padx=5, pady=5)
        label_206.grid(columnspan=4, row=0, column=1)
        bouton_206.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        entree_nom_206.grid(columnspan=4, row=3, column=3, padx=5, pady=5)
        label_nom_206.grid(columnspan=2, row=3, column=0, sticky=W, padx=5, pady=5)
        label_titre_206.grid(row=5, column=0)
        entree_titre_206.grid(rowspan=3, columnspan=4, row=4, column=3, padx=5, pady=5)
        label_indicatif_206.grid(columnspan=3, row=7, column=0, sticky=W, padx=5, pady=5)
        entree_indicatif_206.grid(columnspan=3, row=7, column=3, padx=5, pady=5)

        #207
        cadre_207 = Frame(self, bd=3, relief='ridge')
        label_207 = Label(cadre_207, text="Patrouilleur 207")
        bouton_207 = Checkbutton(cadre_207, command=activer_207)
        label_nom_207 = Label(cadre_207, text="Nom : ")
        entree_nom_207 = Entry(cadre_207, width=20)
        label_titre_207 = Label(cadre_207, text="Titre : ")
        entree_titre_207 = Listbox(cadre_207, height=3, exportselection=0)
        for item in ["Lieutenant(e)", "Sergent(e)", "Agent(e)"]:
            entree_titre_207.insert(0, item)
        entree_titre_207.select_set(0)
        label_indicatif_207 = Label(cadre_207, text="Indicatif : ")
        entree_indicatif_207 = Entry(cadre_207, width=20)

        cadre_207.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        label_207.grid(columnspan=4, row=0, column=1)
        bouton_207.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        entree_nom_207.grid(columnspan=4, row=3, column=3, padx=5, pady=5)
        label_nom_207.grid(columnspan=2, row=3, column=0, sticky=W, padx=5, pady=5)
        label_titre_207.grid(row=5, column=0)
        entree_titre_207.grid(rowspan=3, columnspan=4, row=4, column=3, padx=5, pady=5)
        label_indicatif_207.grid(columnspan=3, row=7, column=0, sticky=W, padx=5, pady=5)
        entree_indicatif_207.grid(columnspan=3, row=7, column=3, padx=5, pady=5)

        cadre_bouton = Frame(self)
        cadre_bouton.grid(columnspan=2, row=3, column=1, sticky=W)
        ok = lambda: self.nouvelle_fenetre_quart(entree_nom_lieutenant.get(), entree_indicatif_lieutenant.get(),
                                                 entree_nom_204.get(),
                                                 entree_titre_204.get(entree_titre_204.curselection()),
                                                 entree_indicatif_204.get(),
                                                 entree_nom_205.get(),
                                                 entree_titre_205.get(entree_titre_205.curselection()),
                                                 entree_indicatif_205.get(),
                                                 entree_nom_206.get(),
                                                 entree_titre_206.get(entree_titre_206.curselection()),
                                                 entree_indicatif_206.get(),
                                                 entree_nom_207.get(),
                                                 entree_titre_207.get(entree_titre_207.curselection()),
                                                 entree_indicatif_207.get())
        bouton_ok = Button(cadre_bouton, text="Nouveau quart", command=ok, width=60)
        bouton_ok.grid(padx=5, pady=5, sticky=W)

        #annuler = lambda: self.annuler(self, jouer_contre_ordinateur_avant, afficher_sources_avant,
                                       #afficher_cibles_avant)
        #bouton_annuler = Button(cadre_boutons, text="Annuler", command=annuler)
        #bouton_annuler.grid(row=6, column=2, padx=5, pady=5, sticky=E)


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
        self.cadre_logs.config(bd=1, relief='ridge', bg=couleur2, width=353, height=343)
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

        print(self.valeur_boutons)

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

        self.cadre_logs = CadreLogs(self, self.cadre_quart, self.quart.nb_patrouilleurs)

        # On crée le menu
        menu_jeu = Menu(self)
        menu_principal = Menu(menu_jeu, tearoff=0)
        nouveau_quart = lambda: self.nouveau_quart_quitter()
        sauvegarder_quart = lambda: self.sauvegarder_quart()
        charger_quart = lambda: self.charger_quart()
        annuler_dernier_log = lambda: self.nouveau_quart_quitter()
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
        cadre_lieutenant = Frame(cadre_quart, bd=3, relief='ridge', bg="gray40")
        label_lieutenant = Label(cadre_lieutenant, text="Lieutenant : ", bg="gray40", font=("Arial", 14, "bold"))
        label_nom_lieutenant = Label(cadre_lieutenant, text=self.quart.id_lieutenant.nom, bg="gray40", font=("Arial", 14, "bold"))
        label_indicatif = Label(cadre_lieutenant, text=self.quart.id_lieutenant.indicatif, bg="gray40", font=("Arial", 14, "bold"))

        cadre_lieutenant.grid(row=0, padx=10, pady=10)
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

    #def bouton_cote(self, bouton):

    def nouveau_quart_quitter(self):
        """ Initialise une fenêtre de nouveau quart avec les attributs de quart courant.
        """

        f = Fenetre(self.quart)

        for pat in f.quart.id_patrouilleurs:
            if f.quart.id_patrouilleurs[pat] is not None:
                logs = f.quart.id_patrouilleurs[pat].logs
                f.quart.id_patrouilleurs[pat].logs = []
                for log in logs:
                    print(log.log)
                    f.creer_log_existant(pat, log)

        self.destroy()

        #self.canvas_damier = CanvasDamier(self, 60, self.partie.damier)
        #self.canvas_damier.bind('<Button-1>', self.cliquer)
        #self.canvas_damier.grid(row=0, column=0, sticky=NSEW)
        #self.message_couleur.grid_forget()
        #self.messages.grid_forget()
        #self.creer_etiquettes()

    def tous_les_logs(self):
        """Crée une instance de la classeTous_les_logs.
        """
        Tous_les_logs()


    #def annuler_dernier_log(self):
        """ Déplace la dernière pièce déplacée à sa position d'origine.
        Si le dernier mouvement était une prise, la pièce prise est redessinée.
        """

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

    def afficher_message(self, message, couleur):
        """Affiche un message d'une certaine couleur en-dessous du damier.

        Arg:
            message: le message à afficher
            couleur: la couleur du texte du message
        """
        self.messages['foreground'] = couleur
        self.messages['text'] = message

    def afficher_erreur(self, message_erreur):
        """Affiche en rouge un message d'erreur en-dessous du damier.

        Arg:
            message_erreur: le message d'erreur à afficher
        """
        self.afficher_message("Erreur: {}.".format(message_erreur), 'red')

    """def jouer(self):
        Nouveau mouvement si le jeu n'est pas en attente d'un clic.

        if not self.attente_clic:
            self.mouvement()
    """
