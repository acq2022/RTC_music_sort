from pathlib import Path
from config import UNKNOWN_ARTIST

class PathBuilder:
    def album_path(self, album, target):
        artist = self.get_artist_name(album)
        folder = f"{album.year} - {album.title}"

        return Path(target) / artist / folder
    
    def get_artist_name(self, album):
        if isinstance(album.artists, list) and album.artists:
            first = album.artists[0]
            if hasattr(first, "name"):
                return first.name  # objet Artist
            else:
                return str(first)  # déjà une chaîne
        return str(album.artist) if album.artist else UNKNOWN_ARTIST

