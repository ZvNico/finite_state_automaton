from graphviz import Digraph
from string import ascii_lowercase
from prettytable import PrettyTable
from typing import *


class Automate:
    def __init__(self, filename: str = None):
        self.alphabet = []
        self.etats = []
        self.initial = []
        self.terminal = []
        self.historique = []
        self.transitions = {}
        if filename:
            self.filename = filename
            self.lire_automate_sur_fichier(self.filename)

    def __str__(self) -> str:
        """equivalent à 'afficher_automate' mais implementer joliment en python, affiche l'automate"""
        tab = PrettyTable()
        asynchrone = self.est_un_automate_asynchrone()
        if asynchrone:
            self.alphabet.insert(0, "*")
        tab.field_names = [""] + [i for i in self.alphabet]
        x = [[" " for i in range(len(self.alphabet) + 1)] for j in range(len(self.etats))]
        for i, depart in enumerate(self.etats):
            x[i][0] = ""
            if depart in self.initial:
                x[i][0] += "E"
            if depart in self.terminal:
                x[i][0] += "S"
            if x[i][0]:
                x[i][0] += " - "
            x[i][0] += depart
            if depart in self.transitions:
                for symbole, arriver in self.transitions[depart].items():
                    if isinstance(arriver, list):
                        x[i][self.alphabet.index(symbole) + 1] = ".".join(arriver)
                    else:
                        x[i][self.alphabet.index(symbole) + 1] = arriver
        tab.add_rows(x)
        if asynchrone:
            self.alphabet.pop(0)
        return str(tab)

    def lire_automate_sur_fichier(self, nom_fichier: str) -> None:
        """fonction pour restranscrit un automate dans la classe depuis un fichier"""
        with open(nom_fichier) as automatetxt:
            lines = automatetxt.readlines()
            n0 = lambda x: int(lines[x][0])
            n = lambda x: int(lines[x])
            for i in range(n(0)):
                self.alphabet.append(ascii_lowercase[i])
            for i in range(n(1)):
                self.etats.append(str(i))
            for i in range(n0(2)):
                self.initial.append(lines[2][2 * (1 + i)])
            for i in range(n0(3)):
                self.terminal.append(lines[3][2 * (1 + i)])
            for i in range(n(4)):
                depart = lines[5 + i][0]
                symbole = lines[5 + i][1]
                arrive = lines[5 + i][2]
                self.ajouter_transition(depart, symbole, arrive)

    def ecrire_automate_sur_fichier(self, filename: str) -> None:
        """fonction pour retranscrire un automate dans un fichier depuis les attributs de cette classe"""
        i = 1
        automate_w = open(filename, 'w')
        automate_w.write(str(len(self.alphabet)))
        automate_w.write('\n')
        automate_w.write(str(len(self.initial) + len(self.terminal) + 1))
        automate_w.write('\n')
        automate_w.write(str(len(self.initial)) + " ")
        for i in range(len(self.initial)):
            automate_w.write(str(self.initial[i]) + " ")
        automate_w.write('\n')
        automate_w.write(str(len(self.terminal)) + " ")
        for i in range(len(self.terminal)):
            automate_w.write(str(self.terminal[i]) + " ")
        automate_w.write('\n')
        somme_len_transitions = 0
        for elem_a in self.transitions.items():
            for elem_b in elem_a[1].items():
                somme_len_transitions += len(elem_b[1])
        automate_w.write(str(somme_len_transitions))
        automate_w.write('\n')

        for elem_a in self.transitions.items():
            for elem_b in elem_a[1].items():
                for elem_c in elem_b[1]:
                    automate_w.write(str(elem_a[0]))
                    automate_w.write(str(elem_b[0]))
                    automate_w.write(str(elem_c))
                    automate_w.write('\n')
        automate_w.close()

    def generer_graphe(self, filename: str = 'temp/temp'):
        """génération de graph, nécessite graphviz"""
        f = Digraph(filename=filename, format="png")
        f.attr(rankdir="LR")
        if filename == "temp/temp":
            f.attr(bgcolor="transparent")
        for node in self.etats:
            if node in self.initial and node in self.terminal:
                f.node(node, style="wedged", fillcolor="lightblue:lightcoral")
            elif node in self.initial:
                f.node(node, style="filled", fillcolor="lightblue")
            elif node in self.terminal:
                f.node(node, style="filled", fillcolor="lightcoral")
            else:
                f.node(node, shape="circle", style="filled", fillcolor="white")
        for depart, value in self.transitions.items():
            for symbole, arriver in value.items():
                if isinstance(arriver, list):
                    for etat in arriver:
                        f.edge(depart, etat, label=symbole)
                else:
                    f.edge(depart, arriver, label=symbole)
        try:
            f.render()
        except:
            raise Exception("Graphviz not installed : https://graphviz.org/")

    def reconnaitre_mot(self, mot: str) -> int:
        """reconnaissance de mot pour automate deterministe"""
        if self.est_un_automate_deterministe():
            pos = self.initial[0]
            for lettre in mot:
                try:
                    pos = self.transitions[pos][lettre]
                except:
                    break
            return pos in self.terminal
        return -1
        # print_or_tk("Erreur ... l'automate n'est pas deterministe", "ERROR")

    def ajouter_transition(self, depart: str, symbole: str, arriver: str):
        if depart not in self.transitions:
            self.transitions[depart] = {}
        if symbole not in self.transitions[depart]:
            self.transitions[depart][symbole] = arriver
        elif isinstance(self.transitions[depart][symbole], list):
            self.transitions[depart][symbole].append(arriver)
        else:
            self.transitions[depart][symbole] = [self.transitions[depart][symbole], arriver]

    def est_un_automate_deterministe(self) -> bool:
        if len(self.initial) > 1:
            return False
        for value in self.transitions.values():
            for arriver in value.values():
                if isinstance(arriver, list):
                    return False
        return True

    def est_un_automate_complet(self) -> bool:
        for depart in self.etats:
            if depart not in self.transitions:
                return False
            value = self.transitions[depart]
            transitions = list(value.keys())
            for symbole in self.alphabet:
                if symbole not in transitions:
                    return False
        return True

    def est_un_automate_standart(self) -> bool:
        if len(self.initial) > 1:
            return False
        for value in self.transitions.values():
            for arriver in value.values():
                if arriver in self.initial:
                    return False
        return True

    def est_un_automate_asynchrone(self) -> bool:
        """Vérifie si un automate est asynchrone ou non"""
        for depart in self.transitions:
            for key in self.transitions[depart].keys():
                if key == "*":
                    return True
        return False

    def elimination_epsilon(self) -> None:
        """"""
        supprimer = []
        chercher_depuis_etat_a = lambda etat_a: [(key1, key2) for key1, value1 in self.transitions.items() for
                                                 key2, value2 in value1.items() if key2 == etat_a]
        for depart, value in self.transitions.items():
            for symbole in value.keys():
                if symbole == "*":
                    fermeture_epsilon = value[symbole]
                    supprimer.append(depart)
                    for depart, transition2 in chercher_depuis_etat_a(fermeture_epsilon):
                        self.ajouter_transition(depart, symbole, fermeture_epsilon)
        for etat in supprimer:
            del self.transitions[etat]['*']

    def completion(self) -> None:
        """Construction  de  l’automate  déterministe  et  complet  à  partir  de  l’automate synchrone et déterministe AF"""
        complet = True
        for depart in self.etats:
            if depart not in self.transitions:
                self.transitions[depart] = {}
            value = self.transitions[depart]
            transitions = list(value.keys())
            for symbole in self.alphabet:
                if symbole not in transitions:
                    complet = False
                    self.ajouter_transition(depart, symbole, 'p')
        if not complet:
            self.transitions['p'] = {symbole: 'p' for symbole in self.alphabet}
            self.etats.append('p')

    def determiniser(self) -> None:
        new_transitions = {}
        queue = []
        self.etats = []
        self.historique.append({})
        new_terminal = []
        if len(self.initial) > 1:
            new_initial = "".join(self.initial)
            self.historique[-1][new_initial] = [etat for etat in self.initial]
            self.initial = [new_initial]
        queue.append(self.initial[0])
        while queue:
            depart = queue.pop(0)
            if depart not in self.etats:
                self.etats.append(depart)
            sub_dict = {}
            for etat in depart:
                if etat in self.terminal and etat not in new_terminal:
                    new_terminal.append(depart)
                if etat in self.transitions:
                    for symbole, arriver in self.transitions[etat].items():
                        if isinstance(arriver, list):
                            arriver = "".join(arriver)
                        if symbole in sub_dict.keys():
                            if arriver not in sub_dict[symbole]:
                                sub_dict[symbole] += arriver
                        else:
                            sub_dict[symbole] = arriver
            new_transitions[depart] = sub_dict
            if depart not in self.historique[-1]:
                self.historique[-1][depart] = []
            for arriver in new_transitions[depart].values():
                self.historique[-1][depart].append(arriver)
                if arriver not in new_transitions.keys():
                    queue.append(arriver)

        self.terminal = new_terminal
        self.transitions = new_transitions

    def determinisation_et_completion_asynchrone(self) -> None:
        if self.est_un_automate_asynchrone():
            self.elimination_epsilon()
        self.determinisation_et_completion_synchrone()

    def determinisation_et_completion_synchrone(self) -> None:
        if not self.est_un_automate_deterministe():
            self.determiniser()
        if not self.est_un_automate_complet():
            self.completion()

    def automate_complementaire(self) -> None:
        """transformation de l'automate deterministe complet pour que celui ci reconnaisse le langage complémentaire à celui actuel"""
        self.terminal = [etat for etat in self.etats if etat not in self.terminal]

    def automate_standard(self) -> None:
        """transformation de l'automate en automate standart"""
        if len(self.initial) > 1:
            new_transitions = {}
            self.historique.append({})
            queue = []
            self.etats = []
            new_terminal = []
            if len(self.initial) > 1:
                new_initial = "".join(self.initial)
                self.historique[-1][new_initial] = [etat for etat in self.initial]
                self.initial = [new_initial]
            queue.append(self.initial[0])
            while queue:
                depart = queue.pop(0)
                if depart not in self.etats:
                    self.etats.append(depart)
                sub_dict = {}
                for etat in depart:
                    if etat in self.terminal and etat not in new_terminal:
                        new_terminal.append(depart)
                    if etat in self.transitions:
                        for symbole, arriver in self.transitions[etat].items():
                            if isinstance(arriver, list):
                                if symbole in sub_dict.keys():
                                    sub_dict[symbole] = [elt for elt in sub_dict[symbole]]
                                    sub_dict[symbole].extend(arriver)
                                else:
                                    sub_dict[symbole] = arriver
                            else:
                                if symbole in sub_dict.keys():
                                    if arriver not in sub_dict[symbole]:
                                        sub_dict[symbole] += arriver
                                else:
                                    sub_dict[symbole] = arriver
                new_transitions[depart] = sub_dict
                if depart not in self.historique[-1]:
                    self.historique[-1][depart] = []
                for arriver in new_transitions[depart].values():
                    if isinstance(arriver, list):
                        for etat in arriver:
                            self.historique[-1][depart].append(etat)
                            if etat not in new_transitions.keys():
                                queue.append(etat)
                    else:
                        if arriver not in new_transitions.keys():
                            self.historique[-1][depart].append(arriver)
                            queue.append(arriver)
            self.terminal = new_terminal
            self.transitions = new_transitions
        if not self.est_un_automate_standart():
            self.transitions['i'] = self.transitions[self.initial[0]].copy()
            if self.initial[0] in self.terminal:
                self.terminal.append('i')
            self.initial = ['i']
