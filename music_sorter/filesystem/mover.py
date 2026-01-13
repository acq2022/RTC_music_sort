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

    def move_album(self, album, target, is_moving):
        
        # --- Construction des dossiers cibles ---
        artist_target_dir = self.path_builder.artist_album_path(album, target)
        artist_target_dir.mkdir(parents=True, exist_ok=True)

        temp_dir = Path(album.tracklist[0].path).parent / "TEMP"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # --- Construction dynamique des destinations ---
        destinations = {
            "artist": [artist_target_dir],
        }

        if album.year and album.year != UNKNOWN_YEAR:
            decade_target_dir = self.path_builder.decade_album_path(album, target)
            decade_target_dir.mkdir(parents=True, exist_ok=True)
            destinations["decade"] = [decade_target_dir]

        if album.label:
            label_target_dir = self.path_builder.label_album_path(album, target)
            label_target_dir.mkdir(parents=True, exist_ok=True)
            destinations["label"] = [label_target_dir]

        if album.styles:
            style_target_dir = []
            for style in album.styles:
                print("--- STYLE --- ", style)
                style_dir = self.path_builder.style_album_path(album, style, target)
                style_dir.mkdir(parents=True, exist_ok=True)
                style_target_dir.append(style_dir)
            if style_target_dir:
                destinations["style"] = style_target_dir

        # --- Boucle sur les pistes ---
        for track in album.tracklist:
            try:
                track_renamed = self.path_builder.get_track_renamed(track)

                # --- Construire tous les chemins finaux (aplatis) ---
                dest_paths = []
                for category, dirs in destinations.items():
                    for index, dir_path in enumerate(dirs):
                        dest_paths.append(
                            (category, index, dir_path / track_renamed)
                        )

                if DRY_RUN:
                    for _, _, dest_path in dest_paths:
                        logger.info(f"[DRY-RUN] {track.path} → {dest_path}")
                    continue

                # --- Copies via hardlinks temporaires ---
                for category, index, dest_path in dest_paths:
                    temp_link = self._link_to_temp(
                        track.path,
                        temp_dir,
                        suffix=category,
                        index=index
                    )
                    Parser.deplacer_fichier_sans_doublon(
                        temp_link,
                        dest_path,
                        False
                    )

                # --- Déplacement final vers Artists ---
                artist_dest_path = artist_target_dir / track_renamed
                Parser.deplacer_fichier_sans_doublon(
                    track.path,
                    artist_dest_path,
                    is_moving
                )

            except Exception as e:
                logger.warning(
                    f"[MOVE ERROR] {track.path} → {artist_dest_path} : {e}"
                )

        # --- Nettoyage du dossier TEMP ---
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Dossier TEMP supprimé : {temp_dir}")
        except Exception as e:
            logger.warning(f"Impossible de supprimer TEMP {temp_dir} : {e}")

    # --------------------
    # Méthode utilitaire interne
    # --------------------

    # Crée un hardlink temporaire unique pour une piste
    def _link_to_temp(
        self,
        source_path,
        temp_dir: Path,
        suffix: str = "",           # permet de différencier les destinations (decade, label, style)
        index: int | None = None    # permet de différencier les différents styles d'un même album
    ) -> Path:
        track_name = Path(source_path).name

        parts = [suffix]
        if index is not None:
            parts.append(str(index))
        parts.append(track_name)

        link_name = temp_dir / "_".join(parts)

        if not link_name.exists():
            os.link(source_path, link_name)

        return link_name
