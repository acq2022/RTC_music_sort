import logging
import discogs_client
from typing import List
from discogs.discogs_result import DiscogsResult

logger = logging.getLogger("DiscogsService")

class DiscogsService:
    def __init__(self, user_token: str):
        self.client = discogs_client.Client(
            "MusicSorter/1.0",
            user_token=user_token
        )

    def search_album(self, album_title: str, artist: str | None) -> List[DiscogsResult]:
        query = album_title
        logger.info(f"[Discogs] Search: {query}")

        results = self.client.search(
            query,
            type="release",
            artist=artist
        )

        discogs_results = []

        for r in results[:10]:  # limite volontaire
            try:
                discogs_results.append(
                    DiscogsResult(
                        release_id=r.id,
                        title=r.title,
                        artist=r.artists[0].name if r.artists else None,
                        year=r.year,
                        label=r.labels[0].name if r.labels else None,
                        catno=r.labels[0].catno if r.labels else None,
                        formats=[f["name"] for f in r.formats],
                        track_count=len(r.tracklist) if r.tracklist else None,
                        styles=r.styles or [],
                        country=r.country,
                    )
                )
            except Exception as e:
                logger.debug(f"[Discogs] Skipped result: {e}")

        return discogs_results
