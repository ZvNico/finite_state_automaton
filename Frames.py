from Automate import Automate
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
        automaton.ecrire_automate_sur_fichier("temp/temp.txt")
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
    def __init__(self, parent: tk.Tk, automate: Callable):
        super().__init__(parent)
        self.automate = automate
        self.controller = parent
        self.operations = ("Determinisation", "Completion", "Minimisation", "Complémentarisation")
        self.var = tk.StringVar()
        self.button = tk.Button(self, text="►", command=lambda: self.run())
        self.option_menu = tk.OptionMenu(self, self.var, *self.operations)
        self.option_menu.pack(side="left")
        self.button.pack(side="right")

    def run(self) -> None:
        operation = self.var.get()
        automate = self.automate()
        operations = {
            "Determinisation": automate.determiniser,
            "Completion": automate.completion,
            "Minimisation": automate.minimiser,
            "Complémentarisation": automate.automate_complementaire
        }
        if operation in self.operations:
            operations[operation]()
            self.controller.refresh()
