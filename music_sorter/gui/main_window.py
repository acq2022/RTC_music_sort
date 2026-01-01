import tkinter as tk
import sys
import traceback
from tkinter import filedialog, messagebox
from gui.controller import GUIController


def tk_exception_handler(exc, val, tb):
    """
    Handler global pour toutes les exceptions Tkinter
    - Affiche le traceback complet dans le terminal
    - Permet de debuguer facilement dans VS Code
    """
    traceback.print_exception(exc, val, tb, file=sys.stderr)
    # Optionnel : affiche aussi un popup générique à l'utilisateur
    # messagebox.showerror("Erreur", "Une erreur est survenue. Consultez le terminal pour plus de détails.")


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # 🔹 Attache le handler global
        self.report_callback_exception = tk_exception_handler

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

        # Selection 'copy' or 'move'
        self.is_moving_var = tk.BooleanVar(value=False)
        tk.Radiobutton(self, text="copy", value=False, variable=self.is_moving_var).pack(side="left", padx=5)
        tk.Radiobutton(self, text="move", value=True, variable=self.is_moving_var).pack(side="left", padx=5)

        # Start button
        tk.Button(
            self,
            text="Lancer le tri",
            command=self.start_sorting,
            bg="#4CAF50",
            fg="white",
            height=2,
        ).pack(pady=20)

    # ─────────────── Sélecteurs de dossier ───────────────
    def select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_var.set(path)

    def select_target(self):
        path = filedialog.askdirectory()
        if path:
            self.target_var.set(path)

    # ─────────────── Lancer le tri ───────────────
    def start_sorting(self):
        """
        Lancement du tri via le controller
        - Toutes les exceptions dans le main thread Tk sont capturées par tk_exception_handler
        """
        self.controller.start_sorting()

    # ─────────────── Popups utilisateur ───────────────
    def show_error(self, message):
        """Afficher un message d'erreur pour l'utilisateur"""
        messagebox.showerror("Erreur", message)

    def show_info(self, message):
        """Afficher un message d'information pour l'utilisateur"""
        messagebox.showinfo("Information", message)
