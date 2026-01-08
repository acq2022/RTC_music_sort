import logging
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from utils.parser import Parser

logger = logging.getLogger("TagReader")


class TagsReader:
    def read(self, path: str) -> dict:
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
            return {}
        
        def get(tag):
            value = audio.get(tag)
            if not value:
                return None
            v=value[0]
            if v is None:
                return None
            if isinstance(v, str):
                v=v.strip()
            return v
        
        total_tracks = get("totaltracks") or get("tracktotal") or get("trackc")
        if not total_tracks:
            total_tracks = Parser.extract_second_part(get("tracknumber")) or Parser.extract_second_part(get("track"))

        return {
            "path": path,
            "album_artists": [get("albumartist")] or [get("album_artists")] or [get("album artist")],
            "artists": [get("artist")] or [get("artists")],
            "year": Parser.extract_year(get("date")) or Parser.extract_year(get("year")),
            "album_title": get("album"),
            "label": get("organization") or get("label"),
            "catno": get("catalognumber"),
            "track_number": Parser.extract_first_part(get("tracknumber")) or Parser.extract_first_part(get("track")),
            "total_tracks": total_tracks,
            "title": get("title"),
            "duration": str(audio.info.length) if audio and hasattr(audio, "info") and hasattr(audio.info, "length") else get("length"),
            "genre": [get("genre")],
            "bpm": get("bpm"),
            "website": get("website"),
            "disc_number": get("discnumber"),
            "original_date": get("originaldate"),
            "release_country": get("releasecountry"),
            "language": get("language")
        }