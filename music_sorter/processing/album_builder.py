from collections import defaultdict
from domain.album import Album
from config import UNKNOWN_ALBUM

class AlbumBuilder:
    def build(self, tracks):
        albums = defaultdict(lambda: Album(UNKNOWN_ALBUM))

        for track in tracks:
            title = track.album_title or UNKNOWN_ALBUM
            album = albums[title]
            album.title = title
            album.add_track(track)

        for album in albums.values():
            album.finalize()

        return list(albums.values())
