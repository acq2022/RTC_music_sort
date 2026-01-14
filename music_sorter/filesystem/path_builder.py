import logging
from pathlib import Path
from config import UNKNOWN_ARTIST, UNKNOWN_YEAR, UNKNOWN_ALBUM
from utils.parser import Parser

logger = logging.getLogger("PathBuilder")


class PathBuilder:

    # --------------------
    # Méthodes publiques pour obtenir les chemins
    # --------------------

    def artist_album_path(self, album, artist, target):
        artist_sanitized = Parser.sanitize_name(artist).title()
        folder_name, _ = self._album_folder_name(album)
        return Path(target) / "Artists" / artist_sanitized / folder_name

    def alias_album_path(self, album, alias, target):
        alias_sanitized = Parser.sanitize_name(alias).title()
        folder_name, _ = self._album_folder_name(album)
        return Path(target) / "Artists" / alias_sanitized / folder_name

    def decade_album_path(self, album, target):
        artist = Parser.sanitize_name(self._get_artist_name(album))
        folder_name, _ = self._album_folder_name(album)
        decade = (int(album.year) // 10) * 10 if album.year else "Unknown Decade"
        return Path(target) / "Decades" / str(decade) / artist / folder_name

    def label_album_path(self, album, target):
        artist = Parser.sanitize_name(self._get_artist_name(album))
        folder_name, album_label = self._album_folder_name(album)
        label = Parser.sanitize_name(album_label or "Unknown Label")
        return Path(target) / "Labels" / label / artist / folder_name
    
    def style_album_path(self, album, style, target):
        artist = Parser.sanitize_name(self._get_artist_name(album))
        folder_name, _ = self._album_folder_name(album)
        style_sanitized = Parser.sanitize_name(style or "Unknown Style")
        return Path(target) / "Styles" / style_sanitized / artist / folder_name
    

    # Retourne le nom de la piste formaté : '01 - Track Title.flac'
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
        return f"{track_title}{track_format}"

    # --------------------
    # Méthodes internes
    # --------------------

    #Retourne un tuple (nom du dossier album, label original)
    def _album_folder_name(self, album):
        album_year = album.year or UNKNOWN_YEAR
        album_title = album.title.title() or UNKNOWN_ALBUM

        album_label = album.label or ""
        if "Not On Label" in album_label:
            album_label = "Self-released"

        album_catno = album.catno or ""

        # Construction du nom final
        base = f"{album_year} - {album_title}"
        extras = [e for e in [album_label, album_catno] if e]
        folder_name = f"{base} [{' '.join(extras)}]" if extras else base

        return Parser.sanitize_name(folder_name), album_label
    

    # Retourne le nom de l'artiste, formaté proprement
    def _get_artist_name(self, album):
        if album.artists:
            main_artist = album.artists[0]
            if hasattr(main_artist, "name"):
                return main_artist.name.title()  # objet Artist
            else:
                return str(main_artist).title()  # déjà une chaîne
        return UNKNOWN_ARTIST
