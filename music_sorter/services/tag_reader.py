import logging
from mutagen import File
from domain.track import Track

logger = logging.getLogger("TagReader")

class TagReader:
    def read(self, path):
        audio = File(path, easy=True)
        if audio is None:
            logger.warning(f"Unsupported file: {path}")
            return Track(path)

        def get(tag):
            return audio.get(tag, [None])[0]

        return Track(
            path=path,
            title=get("title"),
            artist=get("artist"),
            album=get("album"),
            album_artist=get("albumartist"),
            year=get("date"),
            track_number=get("tracknumber"),
            disc_number=get("discnumber"),
        )
