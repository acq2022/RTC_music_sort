from pathlib import Path

class Track:
    '''def __init__(
        self,
        path: Path,
        track_title=None,
        track_artist=None,
        album_title=None,
        album_artist=None,
        year=None,
        track_number=None,
    ):
        self.path = path
        self.track_title = track_title
        self.track_artist = track_artist
        self.album_title = album_title
        self.album_artist = album_artist
        self.year = year
        self.track_number = track_number

        self.is_identified = False'''
    def __init__(
            self,
            path: Path | None,
            album_artists: list[str] | None,
            track_artists: list[str] | None,
            year: str | None,
            album_title: str | None,
            label: str | None,
            catno: str | None,
            track_number: str | None,
            total_tracks: str | None,
            track_title: str | None,
            duration: str | None,
            genre: list[str] | None,
            bpm: str | None,
            website: str | None,
            disc_number: str | None,
            original_date: str | None,
            release_country: str | None,
            language: str | None
    ):
        self.path=path
        self.album_artists=album_artists,
        self.track_artists=track_artists,
        self.year=year,
        self.album_title=album_title,
        self.label=label,
        self.catno=catno,
        self.track_number=track_number,
        self.total_tracks=total_tracks,
        self.track_title=track_title,
        self.duration=duration,
        self.genre=genre,
        self.bpm=bpm,
        self.website=website,
        self.disc_number=disc_number,
        self.original_date=original_date,
        self.release_country=release_country,
        self.language=language

    def __repr__(self):
        return f"<Track {self.track_artists} - {self.track_number} - {self.track_title}>"
