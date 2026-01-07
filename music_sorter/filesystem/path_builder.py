from pathlib import Path
from config import UNKNOWN_ARTIST, UNKNOWN_YEAR, UNKNOWN_ALBUM
from utils.parser import Parser

class PathBuilder:
    def album_path(self, album, target):
        artist = Parser.sanitize_name(self.get_artist_name(album))
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

        folder_name = Parser.sanitize_name(folder_name)

        return Path(target) / artist / folder_name
    
    def get_artist_name(self, album):
        if isinstance(album.artists, list) and album.artists:
            first = album.artists[0]
            if hasattr(first, "name"):
                return first.name.title()  # objet Artist
            else:
                return str(first).title()  # déjà une chaîne
        return str(album.artist).title() if album.artist else UNKNOWN_ARTIST
    

    def get_track_path(self, track):
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