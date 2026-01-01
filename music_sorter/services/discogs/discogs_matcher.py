import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsMatcher")


class DiscogsMatcher:

    def find(self, album, release):
        if not release or not hasattr(release, "tracklist"):
            return None

        try:
            release_tracklist = list(release.tracklist)
        except Exception as e:
            logger.debug(f"[Discogs] Unable to load tracklist: {e}")
            return None

        for track in album.tracklist:
            title = getattr(track, "title", None)
            if not title:
                return None

            try:
                if not any(
                    release_track.title and release_track.title.lower() == title.lower()
                    for release_track in release_tracklist
                ):
                    return None
            except Exception as e:
                logger.debug(f"[Discogs] Track comparison error: {e}")
                return None

        return release
