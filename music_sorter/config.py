from pathlib import Path

SUPPORTED_EXTENSIONS = {".mp3", ".flac", ".ogg", ".m4a", ".aac", ".aiff", ".dsf", ".opus", ".wav", ".wv"}
DRY_RUN = False

UNKNOWN_ARTIST = "(0) UNKNOWN ARTIST"
VARIOUS_ARTISTS = "(0) VA"
UNKNOWN_YEAR = "XXXX"
UNKNOWN_ALBUM = "Unknown Album"
UNKNOWN_FOLDER = "(0) UNKNOWN FOLDER"

VARIOUS_ALIASES = {"various", "various artist", "various artists", "va", "v-a", "v.a", "v.a."}

TARGET_ROOT = Path("sorted_music")

WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1F]'