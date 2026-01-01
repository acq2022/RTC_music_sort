from pathlib import Path

class Track:
    def __init__(
            self,
            path: Path | None,
            album_artists: list[str] | None,
            artists: list[str] | None,
            year: str | None,
            album_title: str | None,
            label: str | None,
            catno: str | None,
            track_number: str | None,
            total_tracks: str | None,
            title: str | None,
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
        self.album_artists=album_artists
        self.artists=artists
        self.year=year
        self.album_title=album_title
        self.label=label
        self.catno=catno
        self.track_number=track_number
        self.total_tracks=total_tracks
        self.title=title
        self.duration=duration
        self.genre=genre
        self.bpm=bpm
        self.website=website
        self.disc_number=disc_number
        self.original_date=original_date
        self.release_country=release_country
        self.language=language

    def __repr__(self):
        return f"<Track {self.artists} - {self.track_number} - {self.title}>"
