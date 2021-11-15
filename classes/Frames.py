from .Automate import Automate
import tkinter as tk
from PIL import ImageTk, Image
from typing import Callable


class AutomatonList(tk.Frame):
    def __init__(self, controller, filename, **kw):
        super().__init__(**kw)
        self.controller = controller
        self.filenames = [filename]
        self.automates = {filename: Automate(filename)}
        self.var = tk.StringVar()
        self.var.set(filename)
        self.var.trace("w", lambda *args, **kwargs: controller.frame.refresh(self.current()))
        self.option_menu = tk.OptionMenu(self, self.var, *self.filenames)
        self.option_menu.pack()

    def add_automaton(self, filename: str) -> None:
        self.automates[f"{filename}"] = Automate(filename)
        self.filenames.append(filename)
        self.option_menu['menu'].delete(0, 'end')
        for choice in self.filenames:
            self.option_menu['menu'].add_command(label=choice, command=tk._setit(self.var, choice))
        self.var.set(filename)

    def current(self) -> Automate:
        return self.automates[self.var.get()]


class PrettyTableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.var, font=("Courier", 11))
        self.label.pack()

    def refresh(self, automaton) -> None:
        self.var.set(str(automaton))


class RawAutomateFrame(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.var = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.var, font=("Courier", 11))
        self.label.pack()

    def refresh(self, automaton: Automate) -> None:
        automaton.ecrire_automate_sur_fichier("../temp/temp.txt")
        with open("temp/temp.txt") as fichier:
            self.var.set(fichier.read())


class GraphvizFrame(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.parent = parent
        self.label = tk.Label(self)
        self.label.pack()

    def refresh(self, automaton: Automate):
        automaton.generer_graphe()
        img = Image.open("temp/temp.png")
        self.tkimage = ImageTk.PhotoImage(img)
        self.label.configure(image=self.tkimage)


class NavFrame(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.page = ("Raw Automate", "Table", "Graphviz")
        self.buttons = []
        for i in range(3):
            self.buttons.append(
                tk.Button(self, text=self.page[i], command=lambda i=i: parent.show_frame(self.page[i])))
            self.buttons[i].grid(row=0, column=i)

    def step_button(self, page_name: str) -> None:
        button = self.buttons[self.page.index(page_name)]
        a = 1 if 1 > 2 else 3
        if button["state"] == "normal" or button["state"] == "active":
            button["state"] = "disabled"
            button["relief"] = "flat"
        elif button["state"] == "disabled":
            button["state"] = "normal"
            button["relief"] = "raised"


class OperationFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, automate: Callable, output: Callable):
        super().__init__(parent)
        self.automate = automate
        self.output = output
        self.controller = parent
        self.operations = (
        "Determinisation", "Completion", "Complémentarisation", "Standardisation", "retirer mot vide",
        "ajouter mot vide")
        self.var = tk.StringVar()
        self.button = tk.Button(self, text="►", command=lambda: self.run())
        self.option_menu = tk.OptionMenu(self, self.var, *self.operations)
        self.label = tk.Label(self, text="Lancer l'opération de")
        self.label.pack(side="left")
        self.option_menu.pack(side="left")
        self.button.pack(side="right")

    def run(self) -> None:
        operation = self.var.get()
        automate = self.automate()
        operations = {
            "Determinisation": automate.determiniser,
            "Completion": automate.completion,
            "Complémentarisation": automate.automate_complementaire,
            "Standardisation": automate.automate_standard,
            "retirer mot vide": automate.retirer_mot_vide,
            "ajouter mot vide": automate.ajout_mot_vide,
        }
        if operation in self.operations:
            operations[operation]()
            self.output(f"L'opération de {operation} a été effectué")
            self.controller.refresh()


class ConditionFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, automate: Callable, output: Callable):
        super().__init__(parent)
        self.automate = automate
        self.output = output
        self.controller = parent
        self.conditions = ("standart", "complet", "deterministe")
        self.var = tk.StringVar()
        self.button = tk.Button(self, text="►", command=lambda: self.run())
        self.option_menu = tk.OptionMenu(self, self.var, *self.conditions)
        self.label = tk.Label(self, text="Vérifier que l'automate est")
        self.label.pack(side="left")
        self.option_menu.pack(side="left")
        self.button.pack(side="right")

    def run(self) -> None:
        condition = self.var.get()
        automate = self.automate()
        conditions = {
            "standart": automate.est_un_automate_standart,
            "complet": automate.est_un_automate_complet,
            "deterministe": automate.est_un_automate_deterministe,
        }
        if condition in self.conditions:
            res = conditions[condition]()
            if res:
                self.output(f"L'automate est {condition}")
            else:
                self.output(f"L'automate n'est pas {condition}")
            self.controller.refresh()


class OutputFrame(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.var = tk.StringVar()
        self.var.set("")
        self.label1 = tk.Label(self, text="Sortie:")
        self.label2 = tk.Label(self, textvariable=self.var)
        self.label1.pack(side="left")
        self.label2.pack(side="right")

    def output(self, output: str):
        self.var.set(output)


class InputFrame(tk.Frame):
    def __init__(self, parent: tk.Tk, automate: Callable, output: Callable):
        super().__init__(parent)
        self.automate = automate
        self.output = output
        self.label = tk.Label(self, text="Lancer la reconnaissance du mot ")
        self.input = tk.Entry(self)
        self.button = tk.Button(self, text="►", command=self.enter)
        self.label.pack(side="left")
        self.input.pack(side="left")
        self.button.pack(side="right")

    def enter(self):
        res = self.automate().reconnaitre_mot(self.input.get())
        if res:
            self.output(f"Le mot {self.input.get()} a été reconnu")
        else:
            self.output(f"Le mot {self.input.get()} n'a pas été reconnu")
        self.input.delete(0, tk.END)
