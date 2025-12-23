import logging
import sys
from pathlib import Path
from processing.sorter import Sorter
from gui.main_window import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s"
)


def run_cli():
    source = Path("music_to_sort")
    sorter = Sorter()
    sorter.process(source, ignored_dirs=["_ignore"])


def run_gui():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_gui()
