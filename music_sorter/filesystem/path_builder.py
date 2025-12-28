from pathlib import Path
from config import UNKNOWN_ARTIST

class PathBuilder:
    def album_path(self, album, root):
        print("PathBuilder album_path")
        print("ALBUM : ", album, type(album))
        artist = self.get_artist_name(album)
        print("ARIST : ", artist, type(artist))
        print("FOLDER :", f"{album.year} - {album.title}", type(f"{album.year} - {album.title}"))
        #artist = album.artist or UNKNOWN_ARTIST
        folder = f"{album.year} - {album.title}"

        return Path(root) / artist / folder
    
    def get_artist_name(self, album):
        if isinstance(album.artist, list) and album.artist:
            first = album.artist[0]
            if hasattr(first, "name"):
                return first.name  # objet Artist
            else:
                return str(first)  # déjà une chaîne
        return str(album.artist) if album.artist else UNKNOWN_ARTIST

