import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsMatcher")


class DiscogsMatcher:
    def select(
        self,
        album: Album,
        results: list[DiscogsResult],
        min_score: float = 0.7,
    ) -> DiscogsResult | None:

        scored = []

        for result in results:
            score = self.score(album, result)
            scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)

        if not scored:
            return None

        best_score, best_result = scored[0]

        logger.info(
            f"[Discogs] Best score for '{album.title}': {best_score:.2f}"
        )

        if best_score >= min_score:
            return best_result

        return None

    def score(self, album: Album, result: DiscogsResult) -> float:
        score = 0.0

        # Titre
        if album.title.lower() in result.title.lower():
            score += 0.4

        # Artiste
        if album.artist and result.artist:
            if album.artist.lower() in result.artist.lower():
                score += 0.3

        # Année
        if album.year and result.year:
            try:
                if abs(int(album.year) - int(result.year)) <= 1:
                    score += 0.2
            except ValueError:
                pass

        # Nombre de pistes
        if result.track_count:
            if abs(result.track_count - len(album.tracks)) <= 1:
                score += 0.1

        logger.debug(
            f"[DiscogsScore] {result.title} → {score:.2f}"
        )

        return score
