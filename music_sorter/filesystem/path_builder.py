from pathlib import Path
from config import UNKNOWN_ARTIST

class PathBuilder:
    def album_path(self, album, root):
        artist = album.artist or UNKNOWN_ARTIST
        folder = f"{album.year} - {album.title}"

        return Path(root) / artist / folder
