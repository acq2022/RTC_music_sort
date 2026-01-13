import os
import logging
from pathlib import Path
from filesystem.path_builder import PathBuilder
from utils.parser import Parser
from config import DRY_RUN, UNKNOWN_YEAR

logger = logging.getLogger("Mover")

class Mover:
    def __init__(self):
        self.path_builder = PathBuilder()

    def move_album(self, album, target, is_moving):
        artist_target_dir = self.path_builder.artist_album_path(album, target)
        artist_target_dir.mkdir(parents=True, exist_ok=True)

        temp_dir = Path(os.path.dirname(album.tracklist[0].path)) / "TEMP"
        temp_dir.mkdir(parents=True, exist_ok=True)

        if album.year and album.year != UNKNOWN_YEAR:
            decade_target_dir = self.path_builder.decades_album_path(album, target)
            decade_target_dir.mkdir(parents=True, exist_ok=True)

        if album.label:
            label_target_dir = self.path_builder.label_album_path(album, target)
            label_target_dir.mkdir(parents=True, exist_ok=True)

        for track in album.tracklist:
            try:
                track_renamed = self.path_builder.get_track_renamed(track)

                artist_dest_path = artist_target_dir / track_renamed
                
                if album.year and album.year != UNKNOWN_YEAR:
                    decade_dest_path = decade_target_dir / track_renamed
                
                if album.label:
                    label_dest_path = label_target_dir / track_renamed

                if DRY_RUN:
                    logger.info(f"[DRY-RUN] {track.path} → {artist_dest_path}")
                else:
                    source = track.path
                    link_name = temp_dir / track_renamed
                    try:
                        os.link(source, link_name)
                    except:
                        logger.info(f"{link_name} existe déjà")
                    
                    if album.year and album.year != UNKNOWN_YEAR:
                        logger.info(f"{link_name} {Parser.deplacer_fichier_sans_doublon(link_name, decade_dest_path, False)} {decade_dest_path}")
                    
                    if album.label:
                        logger.info(f"{track.path} {Parser.deplacer_fichier_sans_doublon(link_name, label_dest_path, False)} {label_dest_path}")

                    logger.info(f"{track.path} {Parser.deplacer_fichier_sans_doublon(track.path, artist_dest_path, is_moving)} {artist_dest_path}")
            except Exception as e:
                logger.warning(f"[MOVE ERROR] {track.path} → {artist_dest_path} : {e}")
