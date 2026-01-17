import os
import shutil
import logging
from pathlib import Path
from filesystem.path_builder import PathBuilder
from utils.parser import Parser
from config import DRY_RUN, UNKNOWN_YEAR

logger = logging.getLogger("Mover")


class Mover:
    def __init__(self):
        self.path_builder = PathBuilder()

    def move_album(self, album, target, is_aliases, is_styles, is_decades, is_labels, is_moving):

        # TEMP
        
        # --- Construction du dossier TEMP
        temp_dir = Path(target) / "TEMP"
        temp_dir.mkdir(parents=True, exist_ok=True)


        # DESTINATIONS

        # --- Construction dynamique des destinations ---
        destinations: dict[str, list[Path]] = {}

        # --- Artists ---
        artist_target_dir: list[Path] = []
        for artist in album.artists:
            artist_dir = self.path_builder.artist_album_path(album, artist.name, target)
            artist_dir.mkdir(parents=True, exist_ok=True)
            artist_target_dir.append(artist_dir)
        if artist_target_dir:
            destinations["artists"] = artist_target_dir

        # --- Aliases ---
        if is_aliases:
            alias_target_dir: list[Path] = []
            for artist in album.artists:
                for alias in artist.aliases:
                    alias_dir = self.path_builder.alias_album_path(album, alias.name, target)
                    alias_dir.mkdir(parents=True, exist_ok=True)
                    alias_target_dir.append(alias_dir)
            if alias_target_dir:
                destinations["aliases"] = alias_target_dir

        # --- Decades ---
        if is_decades:
            if album.year and album.year != UNKNOWN_YEAR:
                decade_target_dir = self.path_builder.decade_album_path(album, target)
                decade_target_dir.mkdir(parents=True, exist_ok=True)
                destinations["decades"] = [decade_target_dir]

        # --- Labels ---
        if is_labels:
            if album.label:
                label_target_dir = self.path_builder.label_album_path(album, target)
                label_target_dir.mkdir(parents=True, exist_ok=True)
                destinations["labels"] = [label_target_dir]

        # --- Styles ---
        if is_styles:
            style_target_dir: list[Path] = []
            for style in album.styles:
                style_dir = self.path_builder.style_album_path(album, style, target)
                style_dir.mkdir(parents=True, exist_ok=True)
                style_target_dir.append(style_dir)
            if style_target_dir:
                destinations["styles"] = style_target_dir


        # TRACKS

        # --- Boucle sur les pistes ---
        for track in album.tracklist:
            track_renamed = self.path_builder.get_track_renamed(track)

            try:
                # --- TEMP hardlink unique par piste
                temp_source = temp_dir / track_renamed
                if not temp_source.exists():
                    os.link(track.path, temp_source)

                # --- Copies vers toutes les destinations
                for category, dirs in destinations.items():
                    for dest_dir in dirs:
                        dest_path = dest_dir / track_renamed

                        if DRY_RUN:
                            logger.info(f"[DRY-RUN] {track.path} → {dest_path}")
                        else:
                            Parser.deplacer_fichier_sans_doublon(temp_source, dest_path, is_moving=is_moving)

                # --- Suppression de la source originale (si déplacement)
                if is_moving and not DRY_RUN:
                    track.path.unlink()

            except Exception as e:
                logger.error(f"[MOVE ERROR] {track.path} : {e}", exc_info=True)


        # NETTOYAGE TEMP

        if not DRY_RUN:
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Dossier TEMP supprimé : {temp_dir}")
            except Exception as e:
                logger.warning(f"Impossible de supprimer TEMP {temp_dir} : {e}")


    def move_folders(self, selectioned_dir_path, target, is_moving):
        for path in selectioned_dir_path:
            self._move_folder(path, target, is_moving)
        
    def _move_folder(self, path, target, is_moving):
        final_selection_dir = Path(target) / "Selections" / path.parent.name
        final_selection_dir.mkdir(parents=True, exist_ok=True)
        logger.info(Parser.deplacer_dossier(path, final_selection_dir, is_moving=is_moving))