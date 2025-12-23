from collections import defaultdict
from domain.album import Album

class AlbumBuilder:
    def build(self, tracks):
        albums = defaultdict(lambda: Album("Unknown Album"))

        for track in tracks:
            title = track.album or "Unknown Album"
            album = albums[title]
            album.title = title
            album.add_track(track)

        for album in albums.values():
            album.finalize()

        return list(albums.values())
