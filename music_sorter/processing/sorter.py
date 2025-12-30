import logging
from processing.scanner import Scanner
from services.tag_reader import TagReader
from processing.album_builder import AlbumBuilder
from processing.metadata_enricher import MetadataEnricher
from filesystem.mover import Mover
from config import TARGET_ROOT

logger = logging.getLogger("Sorter")

class Sorter:
    def process(self, source_dir, target_dir, ignored_dirs=None, is_moving=False):
        scanner = Scanner()
        tags_reader = TagReader()
        builder = AlbumBuilder()
        enricher = MetadataEnricher()
        mover = Mover()

        paths = scanner.scan(source_dir, ignored_dirs)
        tracks = [tags_reader.read(p) for p in paths]
        print("tracks :", tracks)
        albums = builder.build(tracks)

        enricher.enrich_albums(albums)

        for album in albums:
            mover.move_album(album, target_dir, is_moving)
