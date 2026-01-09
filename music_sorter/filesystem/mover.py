import shutil
import logging
from filesystem.path_builder import PathBuilder
from utils.parser import Parser
from config import DRY_RUN

logger = logging.getLogger("Mover")

class Mover:
    def __init__(self):
        self.path_builder = PathBuilder()

    def move_album(self, album, target, is_moving):
        target_dir = self.path_builder.album_path(album, target)
        target_dir.mkdir(parents=True, exist_ok=True)
        for track in album.tracklist:
            try:
                track_path = self.path_builder.get_track_path(track)
                dest_path = target_dir / track_path

                if DRY_RUN:
                    logger.info(f"[DRY-RUN] {track.path} → {dest_path}")
                else:
                    logger.info(f"{track.path} {Parser.deplacer_fichier_sans_doublon(track.path, dest_path, is_moving)} {dest_path}")
            except Exception as e:
                logger.warning(f"[MOVE ERROR] {track.path} → {dest_path} : {e}")
