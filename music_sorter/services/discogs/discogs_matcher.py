import logging
import time

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
            try:
                title = getattr(track, "title", None)
            except Exception as e:
                if e.response.status_code == 429:
                    logger.warning("Limite de rate Discogs atteinte !")
                    time.sleep(60)
                else:
                    logger.warning(f"[Discogs] Erreur title: {e}")
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
