import logging
from processing.scanner import Scanner
from processing.track_builder import TrackBuilder
from processing.album_builder import AlbumBuilder
from processing.metadata_enricher import MetadataEnricher
from filesystem.mover import Mover

logger = logging.getLogger("Sorter")

class Sorter:
    def process(self, source_dir, target_dir, is_aliases=False, is_styles=False, is_decades=False, is_labels=False, selectioned_dir=None, ignored_dirs=None, is_moving=False):
        scanner = Scanner()
        track_builder = TrackBuilder()
        album_builder = AlbumBuilder()
        enricher = MetadataEnricher()
        mover = Mover()

        paths = scanner.scan(source_dir, ignored_dirs)
        tracks = track_builder.build(paths)
        albums = album_builder.build(tracks)
        enricher.enrich_albums(albums)

        for album in albums:
            mover.move_album(album, target_dir, is_aliases, is_styles, is_decades, is_labels, selectioned_dir, is_moving)