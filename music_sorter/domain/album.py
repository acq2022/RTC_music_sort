from collections import Counter
from config import VARIOUS_ARTISTS, VARIOUS_ALIASES, UNKNOWN_ALBUM, UNKNOWN_YEAR
from utils.parser import Parser

class Album:
    def __init__(                           # DONNEES DE DISCOGS :
        self,    
        title: str,                             # str
        album_id: int | None = None,            # int
        artists: list[str] | None = None,       # list
        year: str | None = None,                # int
        label: str | None = None,               # list -> ['labels'][0]['name'] => str
        catno: str | None = None,               # list -> ['labels'][0]['catno'] => str
        tracklist: list[str] | None = None,     # list
        total_tracks: str | None = None,        # int => len(tracklist)
        style: list[str] | None = None,         # list
        website: str | None = None,             # str
        disc_number: str | None = None,         # x NONE
        original_date: str | None = None,       # x NONE (= released? str)
        release_country: str | None = None,     # NoneType (str?)
        language: str | None = None,            # x NONE
    ):
        self.album_id = album_id
        self.artists = artists if artists is not None else []
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


    def add_track(self, track):
        self.tracklist.append(track)

    def finalize(self):
        print("#Album 1 : ", self.artists, " - ", self.title, " - ", self.year, type(self.year))
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
            VARIOUS_ARTISTS
            if Parser.normalize_artist(artist) in VARIOUS_ALIASES
            else artist
        ]

        def _get_year(self):
            values = [getattr(track, "year") for track in self.tracklist if getattr(track, "year")]
            if values:
                if self.artists[0] == VARIOUS_ARTISTS and self.title == UNKNOWN_ALBUM:
                    return UNKNOWN_YEAR
                else:
                    return Counter(values).most_common(1)[0][0]
        
        self.year = _get_year(self)

        def _set_var(self, var_name: str):
            values = [getattr(track, var_name) for track in self.tracklist if getattr(track, var_name)]
            if values:
                setattr(self, var_name, Counter(values).most_common(1)[0][0])

        for attr in ["label", "catno", "total_tracks", "website", "disc_number", "original_date", "release_country", "language"]:
            _set_var(self, attr)
        
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

        print("#Album 2 : ", self.artists, " - ", self.title, " - ", self.year, type(self.year))


    def __repr__(self):
        return f"<Album {self.artists} - {self.year} {self.title} ({len(self.tracklist)} tracks)>"
