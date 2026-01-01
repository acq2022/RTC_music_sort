import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsEnricher")

# TOTO : paufiner le remplissage (+ de paramètres à remplir dans Album)
class DiscogsEnricher:
    def apply(self, album: Album, result) -> None:
        logger.info(f"[Discogs] Applying result {result.id} to '{album.title}'")

        album.artists = result.artists
        album.year = result.year
        album.title = result.title

        label_infos = result.data['labels'][0]
        album.label = label_infos['name']
        album.catno = label_infos['catno']

        album.style = result.styles
