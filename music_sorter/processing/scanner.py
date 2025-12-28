from pathlib import Path
from config import SUPPORTED_EXTENSIONS

class Scanner:
    
    def scan(self, root: Path, ignored_dirs=None):
        print("Scanner scan")
        ignored_dirs = set(ignored_dirs or [])
        files = []

        for path in root.rglob("*"):
            if path.is_dir() and path.name in ignored_dirs:
                continue
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)

        return files
