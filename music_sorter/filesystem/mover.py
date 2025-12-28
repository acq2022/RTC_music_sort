import shutil
import logging
from filesystem.path_builder import PathBuilder
from config import DRY_RUN

logger = logging.getLogger("Mover")

class Mover:
    def __init__(self):
        self.builder = PathBuilder()

    def move_album(self, album, root):
        print("mover move_album")
        target_dir = self.builder.album_path(album, root)
        target_dir.mkdir(parents=True, exist_ok=True)
        print("mover move_album ALBUM: ", album)
        for track in album.tracklist:
            print("track.path : ", track.path, type(track.path))
            print("target_dir:", target_dir, type(target_dir))
            print("track.path:", track.path, type(track.path))
            print("track.path.name:", track.path.name, type(track.path.name))

            dest = target_dir / track.path.name

            if DRY_RUN:
                logger.info(f"[DRY-RUN] {track.path} → {dest}")
            else:
                shutil.move(track.path, dest)
