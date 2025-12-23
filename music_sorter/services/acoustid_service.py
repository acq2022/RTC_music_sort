import logging

logger = logging.getLogger("AcoustIDService")

class AcoustIDService:
    def identify(self, track):
        logger.info(f"[AcoustID] Skipped identification for track: {track.path.name}")
        return track
