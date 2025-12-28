import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsMatcher")


class DiscogsMatcher:

    def find(self, album, results):

        for release in results:
            try:
                # Skip si release invalide ou n'a pas de tracklist
                if not release or not hasattr(release, "tracklist"):
                    continue

                # Force la récupération de la tracklist (lazy loading)
                tracklist = list(release.tracklist)

            except Exception as e:
                # Ignore les releases qui déclenchent une 404 ou autre erreur
                print(f"Skipping release due to error: {e}")
                continue

            # Vérification que tous les titres de l'album sont présents
            all_tracks_match = True
            for track_title in album.tracklist:
                if not getattr(track_title, "track_title", None):
                    all_tracks_match = False
                    break

                try:
                    # Recherche d'au moins un titre correspondant dans la release
                    track_found = any(
                        t.title and t.title.lower() == track_title.track_title.lower()
                        for t in tracklist
                    )
                except Exception as e:
                    print(f"Skipping track due to error: {e}")
                    track_found = False

                if not track_found:
                    all_tracks_match = False
                    break

            if all_tracks_match:
                return release  # Release trouvée

        return None  # Aucune release ne correspond
