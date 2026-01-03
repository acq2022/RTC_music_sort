import shutil
import logging
from filesystem.path_builder import PathBuilder
from config import DRY_RUN

logger = logging.getLogger("Mover")

class Mover:
    def __init__(self):
        self.builder = PathBuilder()

    def move_album(self, album, target, is_moving):
        target_dir = self.builder.album_path(album, target)
        target_dir.mkdir(parents=True, exist_ok=True)
        for track in album.tracklist:
            try:
                track_name = self.builder.get_track_name(track)
                dest = target_dir / track_name

                if DRY_RUN:
                    logger.info(f"[DRY-RUN] {track.path} → {dest}")
                else:
                    if(is_moving):
                        shutil.move(track.path, dest)
                    else:
                        shutil.copy(track.path, dest)
            except Exception as e:
                logger.warning(f"[MOVE ERROR] {track.path} → {dest} : {e}")
