from pathlib import Path

class Track:
    def __init__(
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

        self.is_identified = False

    def __repr__(self):
        return f"<Track {self.track_artist} - {self.track_number} - {self.track_title}>"
