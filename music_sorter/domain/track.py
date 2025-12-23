from pathlib import Path

class Track:
    def __init__(
        self,
        path: Path,
        title=None,
        artist=None,
        album=None,
        album_artist=None,
        year=None,
        track_number=None,
        disc_number=None,
    ):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album
        self.album_artist = album_artist
        self.year = year
        self.track_number = track_number
        self.disc_number = disc_number

        self.is_identified = False

    def __repr__(self):
        return f"<Track {self.artist} - {self.title}>"
