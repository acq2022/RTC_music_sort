import tkinter as tk
from tkinter import filedialog, messagebox
from gui.controller import GUIController


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        print('MainWindow')

        self.title("Music Sorter")
        self.geometry("600x400")
        self.resizable(False, False)

        self.controller = GUIController(self)

        self._build_ui()

    def _build_ui(self):
        # Source folder
        tk.Label(self, text="Dossier source").pack(anchor="w", padx=10, pady=(10, 0))
        self.source_var = tk.StringVar()
        tk.Entry(self, textvariable=self.source_var, width=70).pack(padx=10)
        tk.Button(self, text="Parcourir", command=self.select_source).pack(pady=5)

        # Target folder
        tk.Label(self, text="Dossier cible").pack(anchor="w", padx=10, pady=(10, 0))
        self.target_var = tk.StringVar()
        tk.Entry(self, textvariable=self.target_var, width=70).pack(padx=10)
        tk.Button(self, text="Parcourir", command=self.select_target).pack(pady=5)

        # Ignored folders
        tk.Label(self, text="Dossiers à ignorer (un par ligne)").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.ignore_text = tk.Text(self, height=5, width=70)
        self.ignore_text.pack(padx=10)

        # Start button
        tk.Button(
            self,
            text="Lancer le tri",
            command=self.start_sorting,
            bg="#4CAF50",
            fg="white",
            height=2,
        ).pack(pady=20)

    def select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_var.set(path)

    def select_target(self):
        path = filedialog.askdirectory()
        if path:
            self.target_var.set(path)

    def start_sorting(self):
        self.controller.start_sorting()

    def show_error(self, message):
        messagebox.showerror("Erreur", message)

    def show_info(self, message):
        messagebox.showinfo("Information", message)
