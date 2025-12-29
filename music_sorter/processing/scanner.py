from pathlib import Path
from config import SUPPORTED_EXTENSIONS

class Scanner:

    def scan(self, root: Path, ignored_dirs=None):
        ignored_dirs = set(ignored_dirs or [])
        files = []

        for path in root.iterdir():
            if path.is_dir():
                if path.name in ignored_dirs:
                    continue  # on n'entre pas dans ce dossier
                files.extend(self.scan(path, ignored_dirs))
            else:
                if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(path)

        return files