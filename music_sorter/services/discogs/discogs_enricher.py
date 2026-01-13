import logging
from domain.album import Album
from domain.artist import Artist

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
        album.artists = [Artist(name=artist.name, aliases=artist.aliases) for artist in result.artists]
        for artist in album.artists:
            logger.info(f"ARTIST {artist}, {type(artist)} - NAME {artist.name}, {type(artist.name)}")
        album.year = result.year

        label_infos = result.data["labels"][0]
        album.label = clean(label_infos.get("name"))
        album.catno = clean(label_infos.get("catno"))

        album.total_tracks = clean(str(len(result.tracklist)))
        album.styles = result.styles
        album.website = clean(result.url)
        album.original_date = clean(result.data["released"])
        album.release_country = clean(result.country)

