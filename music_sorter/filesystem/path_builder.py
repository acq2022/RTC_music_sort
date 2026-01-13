import logging
from pathlib import Path
from config import UNKNOWN_ARTIST, UNKNOWN_YEAR, UNKNOWN_ALBUM
from utils.parser import Parser

logger = logging.getLogger("PathBuilder")

class PathBuilder:
    
    def artist_album_path(self, album, target):
        artist = Parser.sanitize_name(self.get_artist_name(album))
        folder_name, _ = self._album_folder_name(album)

        return Path(target) / "Artists" / artist / folder_name
    
    def decades_album_path(self, album, target):
        artist = Parser.sanitize_name(self.get_artist_name(album))
        folder_name, _ = self._album_folder_name(album)

        decade = (
            (int(album.year) // 10) * 10
            if album.year
            else "Unknown Decade"
        )

        return Path(target) / "Decades" / str(decade) / artist / folder_name
    
    def label_album_path(self, album, target):
        artist = Parser.sanitize_name(self.get_artist_name(album))
        folder_name, album_label = self._album_folder_name(album)

        label = Parser.sanitize_name(album_label or "Unknown Label")

        return Path(target) / "Labels" / label / artist / folder_name
    
    def _album_folder_name(self, album):
        album_year = album.year or UNKNOWN_YEAR
        album_title = album.title.title() or UNKNOWN_ALBUM

        album_label = album.label or ""
        if "Not On Label" in album_label:
            album_label = "Self-released"

        album_catno = album.catno or ""

        base = f"{album_year} - {album_title}"

        extras = []
        if album_label:
            extras.append(album_label)
        if album_catno:
            extras.append(album_catno)

        folder_name = base
        if extras:
            folder_name += f" [{' '.join(extras)}]"

        return Parser.sanitize_name(folder_name), album_label

    
    def get_artist_name(self, album):
        if album.artists:
            first = album.artists[0]
            if hasattr(first, "name"):
                return first.name.title()  # objet Artist
            else:
                return str(first).title()  # déjà une chaîne
        return str(album.artists[0]).title() if album.artists[0] else UNKNOWN_ARTIST
    

    def get_track_renamed(self, track):
        track_number = Parser.normalize_track_number(track.track_number)
        track_title = Parser.sanitize_track_title_name(track.title)
        if track_title:
            track_title = track_title.title()
        else:
            track_title = track.path.stem
        track_format = track.path.suffix.lower()
        if track_number:
            return f"{track_number} - {track_title}{track_format}"
        else:
            return f"{track_title}{track_format}"