import logging
from processing.scanner import Scanner
from services.tag_reader import TagReader
from processing.album_builder import AlbumBuilder
from processing.metadata_enricher import MetadataEnricher
from filesystem.mover import Mover
from config import TARGET_ROOT

logger = logging.getLogger("Sorter")

class Sorter:
    def process(self, source_dir, ignored_dirs=None):
        scanner = Scanner()
        reader = TagReader()
        builder = AlbumBuilder()
        enricher = MetadataEnricher()
        mover = Mover()

        paths = scanner.scan(source_dir, ignored_dirs)
        tracks = [reader.read(p) for p in paths]
        albums = builder.build(tracks)

        enricher.enrich_albums(albums)

        for album in albums:
            mover.move_album(album, TARGET_ROOT)
