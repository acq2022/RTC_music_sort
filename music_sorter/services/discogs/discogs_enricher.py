import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsEnricher")

class DiscogsEnricher:
    def apply(self, album: Album, result) -> None:
        logger.info(f"[Discogs] Applying result {result.id} to '{album.title}'")

        def clean(value):
            if value is None or value.lower() == "none":
                return None
            return value

        album.title = result.title
        album.album_id = result.id
        album.artists = result.artists
        album.year = result.year

        label_infos = result.data["labels"][0]
        album.label = clean(label_infos.get("name"))
        album.catno = clean(label_infos.get("catno"))

        album.total_tracks = clean(str(len(result.tracklist)))
        album.style = result.styles
        album.website = clean(result.url)
        album.original_date = clean(result.data["released"])
        album.release_country = clean(result.country)

