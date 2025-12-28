import logging
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

from domain.track import Track

logger = logging.getLogger("TagReader")


class TagReader:
    def read(self, path: str) -> Track:
        audio = None
        
        # mp3 → EasyID3
        if str(path).lower().endswith(".mp3"):
            try:
                audio = EasyID3(path)
            except ID3NoHeaderError:
                logger.warning(f"No ID3 tags in MP3: {path}")
            except Exception as e:
                logger.debug(f"EasyID3 failed on {path}: {e}")

        # Autres formats → easy=True
        if audio is None:
            try:
                audio = File(path, easy=True)
            except Exception as e:
                logger.debug(f"Mutagen File() failed on {path}: {e}")

        # Aucun tag
        if audio is None:
            return Track(path=path)

        def get(tag):
            value = audio.get(tag)
            return value[0] if value else None

        return Track(
            path=path,
            track_title=get("title"),
            track_artist=get("artist"),
            album_title=get("album"),
            album_artist=get("albumartist"),
            year=get("date"),
            track_number=self._normalize_number(get("tracknumber")),
        )
    
    @staticmethod
    # ex: "3/12" → "3"
    def _normalize_number(value):
        return value.split("/")[0] if value else None