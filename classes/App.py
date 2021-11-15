from tkinter import filedialog
from tkinter import messagebox
from .Frames import *


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.frames = {}
        self.container = tk.Frame(self)
        temp = self.open_automaton_txt()
        if not temp:
            exit(1)
        self.frame = None
        self.automaton_list = AutomatonList(self, temp)
        self.navigation_frame = NavFrame(self)
        self.frames["Graphviz"] = GraphvizFrame(self.container)
        self.frames["Raw Automate"] = RawAutomateFrame(self.container)
        self.frames["Table"] = PrettyTableFrame(self.container)
        for frame in self.frames.values():
            frame.grid(row=0, column=0, columnspan=1, rowspan=1, sticky="nsew")
        self.output_frame = OutputFrame(self)
        self.operations_frame = OperationFrame(self, self.automaton_list.current, self.output_frame.output)
        self.conditions_frame = ConditionFrame(self, self.automaton_list.current, self.output_frame.output)
        self.input_frame = InputFrame(self, self.automaton_list.current, self.output_frame.output)
        self.automaton_list.pack()
        self.navigation_frame.pack()
        self.container.pack()
        self.operations_frame.pack()
        self.conditions_frame.pack()
        self.input_frame.pack()
        self.output_frame.pack()
        self.create_menu_bar()
        self.show_frame("Raw Automate")

    def show_frame(self, frame_name: str) -> None:
        for key, value in self.frames.items():
            if value == self.frame:
                self.navigation_frame.step_button(key)
                break
        self.frame = self.frames[frame_name]
        self.navigation_frame.step_button(frame_name)
        self.refresh()
        self.frame.tkraise()

    def refresh(self):
        self.frame.refresh(self.automaton_list.current())

    def create_menu_bar(self) -> None:
        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Open",
                              command=lambda: self.automaton_list.add_automaton(self.open_automaton_txt()))
        menu_file.add_command(label="Save", command=self.save)
        menu_file.add_command(label="Save as", command=self.save_as)
        menu_file.add_command(label="Render", command=self.render)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)
        menu_bar.add_command(label="Edit", command=self.about)
        menu_bar.add_command(label="Help", command=self.about)

        self.config(menu=menu_bar)

    def open_automaton_txt(self) -> str:
        return filedialog.askopenfilename(title="Choose the automaton txt file to open", initialdir="automates/",
                                          filetypes=[("text file", ".txt")])

    def render(self) -> None:
        filename = filedialog.asksaveasfilename(title="Save the graph", initialdir="graphes/")
        if filename:
            self.automaton_list.current().generer_graphe(filename)

    def save(self):
        self.automaton_list.current().ecrire_automate_sur_fichier(self.automaton_list.current().filename)

    def save_as(self) -> None:
        filename = filedialog.asksaveasfilename(title="Save the automaton", initialdir="automates/",
                                                filetypes=[("text file", ".txt")])
        if filename:
            self.automaton_list.current().ecrire_automate_sur_fichier(filename)
            self.automaton_list.add_automaton(filename)

    def about(self) -> None:
        messagebox.showinfo(title="About",
                            message="This Desktop app Help you working with finite state automaton.\n\nHow to use:\n\nOpen a new automaton:\nfile -> open -> choose your automate txt files\nSave an automaton:\nfile -> save -> new file name\nRender Graphviz graph:\nfile -> render -> new file name\n\nDeveloped by Nicolas Baconnier, Rania dahane, Nelson Amorim Branco & Alain Chea")


"""
    def run(self, mot: str) -> bool:
        mot = askstring_or_tk(f'Saisissez un mot ("fin" pour arrêter)\nAlphabet:{", ".join(self.alphabet)}')
        while mot != "fin":
            res = self.reconnaitre_mot(mot)
            if res:
                print_or_tk(f"Le mot '{mot}' a été reconnu par l'automate :D", "INFO")
            else:
                print_or_tk(f"Le mot '{mot}' n'a été reconnu par l'automate :/", "INFO")
            mot = askstring_or_tk(f'Saisissez un mot ("fin" pour arrêter)\nAlphabet:{", ".join(self.alphabet)}')
"""
