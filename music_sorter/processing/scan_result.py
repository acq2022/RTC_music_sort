# processing/scan_result.py
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class ScanResult:
    file_paths: List[Path]
    selectioned_dir_paths: List[Path]
