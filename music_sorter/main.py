import logging
from gui.main_window import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s"
)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()