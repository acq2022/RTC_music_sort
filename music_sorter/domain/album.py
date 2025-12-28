from collections import Counter
from config import VARIOUS_ARTISTS, UNKNOWN_YEAR

class Album:
    def __init__(self, title):
        self.artist = None
        self.year = 'XXXX'
        self.title = title
        self.label = None
        self.catno = None
        self.tracklist = []
        self.total_tracks = None
        self.style = []

    def add_track(self, track):
        self.tracklist.append(track)

    def finalize(self):
        artists = {t.album_artist or t.track_artist for t in self.tracklist if t.track_artist}
        years = [t.year for t in self.tracklist if t.year]

        self.artist = (
            artists.pop() if len(artists) == 1 else VARIOUS_ARTISTS
        )

        if years:
            self.year = Counter(years).most_common(1)[0][0]

    def __repr__(self):
        return f"<Album {self.artist} - {self.title} ({len(self.tracklist)} tracks)>"
