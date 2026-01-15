from pathlib import Path
from config import SUPPORTED_EXTENSIONS
from processing.scan_result import ScanResult

class Scanner:

    def scan(self, root: Path, ignored_dirs=None, selectioned_dir=None):
        ignored_dirs = set(ignored_dirs or [])
        selectioned_dir = set(selectioned_dir or [])

        files = []
        selectioned_dir_paths = []

        for path in root.iterdir():
            if path.is_dir():

                if path.name in ignored_dirs:
                    continue  # on n'entre pas dans ce dossier

                if path.name in selectioned_dir:
                    selectioned_dir_paths.append(path)
                    continue  # on n'entre pas dans ce dossier

                result = self.scan(path, ignored_dirs, selectioned_dir)
                files.extend(result.file_paths)
                selectioned_dir_paths.extend(result.selectioned_dir_paths)
                
            else:
                if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(path)

        return ScanResult(files, selectioned_dir_paths)