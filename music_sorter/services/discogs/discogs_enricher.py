import logging
from discogs.discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsEnricher")


class DiscogsEnricher:
    def apply(self, album: Album, result: DiscogsResult) -> None:
        logger.info(
            f"[Discogs] Applying result {result.release_id} to '{album.title}'"
        )

        if result.artist:
            album.artist = result.artist

        if result.year:
            album.year = str(result.year)

        album.label = result.label
        album.catno = result.catno
        album.style = result.styles
