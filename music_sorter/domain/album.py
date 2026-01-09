from .artist import Artist
from collections import Counter
from config import VARIOUS_ARTISTS, VARIOUS_ALIASES, UNKNOWN_ALBUM, UNKNOWN_YEAR
from utils.parser import Parser

class Album:
    def __init__(                               # DONNEES DE DISCOGS :
        self,    
        title: str,                                 # str
        album_id: int | None = None,                # int
        artists: list | tuple | None = None,        # list
        year: str | None = None,                    # int
        label: str | None = None,                   # list -> ['labels'][0]['name'] => str
        catno: str | None = None,                   # list -> ['labels'][0]['catno'] => str
        tracklist: list[str] | None = None,         # list
        total_tracks: str | None = None,            # int => len(tracklist)
        style: list[str] | None = None,             # list
        website: str | None = None,                 # str
        disc_number: str | None = None,             # x NONE
        original_date: str | None = None,           # x NONE (= released? str)
        release_country: str | None = None,         # NoneType (str?)
        language: str | None = None,                # x NONE
    ):
        self.album_id = album_id
        self.year = year
        self.title = title
        self.label = label
        self.catno = catno
        self.tracklist = tracklist if tracklist is not None else []
        self.total_tracks = total_tracks
        self.style = style if style is not None else []
        self.website = website
        self.disc_number = disc_number
        self.original_date = original_date
        self.release_country = release_country
        self.language = language

        self._artists: list[Artist] = []
        if artists is not None:
            self.artists = artists
    

    # -------------------
    # Getter / Setter
    # -------------------
    @property
    def artists(self) -> tuple[Artist, ...]:
        return tuple(self._artists)   


    @artists.setter
    def artists(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("artists must be a list or tuple of str or Artist")

        normalized: list[Artist] = []
        for item in value:
            if isinstance(item, Artist):
                normalized.append(item)
            elif isinstance(item, str):
                normalized.append(Artist(name=item))
            else:
                raise TypeError("artist must contain only str or Artist")

        self._artists = normalized
    
    
    # -------------------
    # Ajout / suppression
    # -------------------
    def add_artist(self, artist: str | Artist):
        if isinstance(artist, Artist):
            self._artists.append(artist)
        elif isinstance(artist, str):
            self._artists.append(Artist(name=artist))
        else:
            raise TypeError("artist must be a str or Artist")
    

    def remove_artist(self, artist: str | Artist):
        if isinstance(artist, Artist):
            self._artists = [a for a in self._artists if a != artist]
        elif isinstance(artist, str):
            self._artists = [a for a in self._artists if a.name != artist]
        else:
            raise TypeError("artist must be a str or Artist")


    # -------------------
    # Gestion des pistes
    # -------------------
    def add_track(self, track):
        self.tracklist.append(track)


    # -------------------
    # Finalisation des données
    # -------------------
    def finalize(self):
        # ---- Artists ----
        artists = {
            artist
            for track in self.tracklist
            for artist in track.artists
        }

        normalized = {
            Parser.join_normalized_terms(artist) 
            for artist in artists
            if artist
        }
        
        artist = next(iter(normalized)) if len(normalized) == 1 else VARIOUS_ARTISTS
        
        self.artists = [
            Artist(name=VARIOUS_ARTISTS)
            if Parser.normalize_artist(artist) in VARIOUS_ALIASES
            else artist
        ]
        
        # ---- Year ----
        self.year = self._get_year()

        # ---- Autres attributs ----
        for attr in ["label", "catno", "total_tracks", "website", "disc_number", "original_date", "release_country", "language"]:
            self._set_var(attr)
        
        # ---- Styles ----
        style = {
            genre 
            for track in self.tracklist 
            if track.genre 
            for genre_list in track.genre
            if genre_list
            for genre in genre_list
            if genre
        }
        self.style = sorted(style)

    
    # -------------------
    # Méthodes privées
    # -------------------
    def _get_year(self):
            values = [getattr(track, "year") for track in self.tracklist if getattr(track, "year", None)]
            if not values:
                return UNKNOWN_YEAR
            if self.artists[0].name == VARIOUS_ARTISTS and self.title == UNKNOWN_ALBUM:
                return UNKNOWN_YEAR
            return Counter(values).most_common(1)[0][0]
    
    
    def _set_var(self, var_name: str):
            values = [getattr(track, var_name) for track in self.tracklist if getattr(track, var_name, None)]
            if values:
                setattr(self, var_name, Counter(values).most_common(1)[0][0])


    # -------------------
    # Représentation
    # -------------------
    def __repr__(self):
        return f"<Album {self.artists} - {self.year} {self.title} ({len(self.tracklist)} tracks)>"
