import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsEnricher")

# TODO : paufiner le remplissage (+ de paramètres à remplir dans Album)
class DiscogsEnricher:
    def apply(self, album: Album, result) -> None:
        logger.info(f"[Discogs] Applying result {result.id} to '{album.title}'")

        album.artists = result.artists
        album.year = result.year
        album.title = result.title

        label_infos = result.data["labels"][0]

        def clean(value):
            if value is None or value.lower() == "none":
                return None
            return value
        
        album.label = clean(label_infos.get("name"))
        album.catno = clean(label_infos.get("catno"))
        
        album.style = result.styles
