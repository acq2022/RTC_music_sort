import threading
from pathlib import Path
from processing.sorter import Sorter
import config


class GUIController:
    def __init__(self, window):
        self.window = window

    def start_sorting(self):
        source = self.window.source_var.get()
        target = self.window.target_var.get()
        ignored = self._get_ignored_dirs()
        is_moving = self.window.is_moving_var.get()

        if not source or not target:
            self.window.show_error("Veuillez sélectionner les dossiers source et cible.")
            return

        # Met à jour la config globale (simple et efficace ici)
        config.TARGET_ROOT = Path(target)

        # Lancer dans un thread pour éviter le gel de Tkinter
        thread = threading.Thread(
            target=self._run_sorter,
            args=(Path(source), Path(target), ignored, is_moving),
            daemon=True,
        )
        thread.start()

    def _run_sorter(self, source, target, ignored, is_moving):
        try:
            sorter = Sorter()
            sorter.process(source, target, ignored, is_moving)
            self.window.show_info("Tri terminé (ou DRY-RUN terminé).")
        except Exception as e:
            self.window.show_error(str(e))

    def _get_ignored_dirs(self):
        text = self.window.ignore_text.get("1.0", "end").strip()
        return [line.strip() for line in text.splitlines() if line.strip()]
