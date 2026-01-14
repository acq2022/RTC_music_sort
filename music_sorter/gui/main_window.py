import tkinter as tk
import sys
import traceback
from tkinter import filedialog, messagebox
from gui.controller import GUIController


def tk_exception_handler(exc, val, tb):
    traceback.print_exception(exc, val, tb, file=sys.stderr)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.report_callback_exception = tk_exception_handler

        self.title("Music Sorter")
        self.geometry("600x760")
        self.resizable(False, False)

        self.controller = GUIController(self)

        # ─────────────── Variables ───────────────
        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()

        self.is_moving_var = tk.BooleanVar(value=False)

        self.is_aliases_var = tk.BooleanVar(value=False)
        self.is_styles_var = tk.BooleanVar(value=False)
        self.is_decades_var = tk.BooleanVar(value=False)
        self.is_labels_var = tk.BooleanVar(value=False)

        self.selections_var = tk.BooleanVar(value=False)
        self.ignore_var = tk.BooleanVar(value=False)

        self._build_ui()

    # ─────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────
    def _build_ui(self):
        TEXT_WIDTH = 68
        TEXT_HEIGHT = 4
        TEXT_PADX = 5

        # ─────────────── Dossiers ───────────────
        paths_frame = tk.LabelFrame(self, text="Dossiers")
        paths_frame.pack(fill="x", padx=10, pady=10)

        tk.Frame(paths_frame, height=6).pack()  # spacer sous le titre

        tk.Label(paths_frame, text="Dossier source").pack(anchor="w")
        tk.Entry(paths_frame, textvariable=self.source_var, width=70).pack(pady=2)
        tk.Button(paths_frame, text="Parcourir", command=self.select_source).pack(pady=2)

        tk.Label(paths_frame, text="Dossier cible").pack(anchor="w", pady=(10, 0))
        tk.Entry(paths_frame, textvariable=self.target_var, width=70).pack(pady=2)
        tk.Button(paths_frame, text="Parcourir", command=self.select_target).pack(pady=2)

        # ─────────────── Options de tri ───────────────
        options_frame = tk.LabelFrame(self, text="Options de tri")
        options_frame.pack(fill="x", padx=10, pady=10)

        tk.Frame(options_frame, height=6).pack()  # spacer sous le titre

        tk.Checkbutton(
            options_frame,
            text="Aliases (ajoute les alias des artistes - hardlinks)",
            variable=self.is_aliases_var,
        ).pack(anchor="w")

        tk.Checkbutton(
            options_frame,
            text="Styles (classement par styles - hardlinks)",
            variable=self.is_styles_var,
        ).pack(anchor="w")

        tk.Checkbutton(
            options_frame,
            text="Decades (classement par décennies - hardlinks)",
            variable=self.is_decades_var,
        ).pack(anchor="w")

        tk.Checkbutton(
            options_frame,
            text="Labels (classement par labels - hardlinks)",
            variable=self.is_labels_var,
        ).pack(anchor="w")

        # ─────────────── Sélections ───────────────
        tk.Checkbutton(
            options_frame,
            text="Sélections (copie de dossiers spécifiques)",
            variable=self.selections_var,
            command=self._toggle_selections_text,
        ).pack(anchor="w", pady=(6, 0))

        self.selections_text = tk.Text(
            options_frame,
            width=TEXT_WIDTH,
            height=TEXT_HEIGHT,
            state="disabled",
            bg="#f0f0f0",
            fg="gray",
            insertbackground="gray",
        )
        self.selections_text.pack(padx=TEXT_PADX, pady=3)

        self.selections_label = tk.Label(
            options_frame,
            text="Noms de dossiers (séparés par des virgules)",
            fg="gray",
        )
        self.selections_label.pack(anchor="w", padx=TEXT_PADX)

        # ─────────────── Ignorer des dossiers ───────────────
        tk.Checkbutton(
            options_frame,
            text="Ignorer des dossiers",
            variable=self.ignore_var,
            command=self._toggle_ignore_text,
        ).pack(anchor="w", pady=(10, 0))

        self.ignore_text = tk.Text(
            options_frame,
            width=TEXT_WIDTH,
            height=TEXT_HEIGHT,
            state="disabled",
            bg="#f0f0f0",
            fg="gray",
            insertbackground="gray",
        )
        self.ignore_text.pack(padx=TEXT_PADX, pady=3)

        self.ignore_label = tk.Label(
            options_frame,
            text="Noms de dossiers (séparés par des virgules)",
            fg="gray",
        )
        self.ignore_label.pack(anchor="w", padx=TEXT_PADX)

        # ─────────────── Mode ───────────────
        mode_frame = tk.LabelFrame(self, text="Mode")
        mode_frame.pack(fill="x", padx=10, pady=10)

        tk.Frame(mode_frame, height=6).pack()  # spacer sous le titre

        tk.Radiobutton(
            mode_frame,
            text="Copy",
            value=False,
            variable=self.is_moving_var,
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            mode_frame,
            text="Move",
            value=True,
            variable=self.is_moving_var,
        ).pack(side="left")

        # ─────────────── Bouton principal ───────────────
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=(8, 6))

        tk.Button(
            bottom_frame,
            text="Lancer le tri",
            command=self.start_sorting,
            bg="#4CAF50",
            fg="white",
            height=2,
            width=25,
        ).pack()

    # ─────────────────────────────────────────────
    # Callbacks
    # ─────────────────────────────────────────────
    def _toggle_selections_text(self):
        self._toggle_text_block(
            self.selections_var.get(),
            self.selections_text,
            self.selections_label,
        )

    def _toggle_ignore_text(self):
        self._toggle_text_block(
            self.ignore_var.get(),
            self.ignore_text,
            self.ignore_label,
        )

    def _toggle_text_block(self, enabled, text_widget, label_widget):
        if enabled:
            text_widget.config(
                state="normal",
                bg="white",
                fg="black",
                insertbackground="black",
            )
            label_widget.config(fg="black")
        else:
            text_widget.delete("1.0", tk.END)
            text_widget.config(
                state="disabled",
                bg="#f0f0f0",
                fg="gray",
                insertbackground="gray",
            )
            label_widget.config(fg="gray")

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

    # ─────────────────────────────────────────────
    # Popups
    # ─────────────────────────────────────────────
    def show_error(self, message):
        messagebox.showerror("Erreur", message)

    def show_info(self, message):
        messagebox.showinfo("Information", message)
