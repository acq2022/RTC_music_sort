import threading
from pathlib import Path
from processing.sorter import Sorter
import config
import traceback  # <-- pour afficher les tracebacks


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

        # Met à jour la config globale
        config.TARGET_ROOT = Path(target)

        # Lancer dans un thread pour éviter le gel de Tkinter
        thread = threading.Thread(
            target=self._thread_wrapper,
            args=(Path(source), Path(target), ignored, is_moving),
            daemon=True,
        )
        thread.start()

    def _thread_wrapper(self, source, target, ignored, is_moving):
        """
        Wrapper pour exécuter le tri dans un thread et afficher
        correctement toutes les exceptions dans le terminal VS Code.
        """
        try:
            self._run_sorter(source, target, ignored, is_moving)
        except Exception:
            # Affiche le traceback complet dans le terminal VS Code
            traceback.print_exc()
            # Affiche un message générique à l'utilisateur
            self.window.show_error("Une erreur est survenue. Consultez le terminal pour plus de détails.")

    def _run_sorter(self, source, target, ignored, is_moving):
        """
        Exécution réelle du tri.
        """
        sorter = Sorter()
        sorter.process(source, target, ignored, is_moving)
        self.window.show_info("Tri terminé (ou DRY-RUN terminé).")

    def _get_ignored_dirs(self):
        text = self.window.ignore_text.get("1.0", "end").strip()
        return [line.strip() for line in text.splitlines() if line.strip()]
