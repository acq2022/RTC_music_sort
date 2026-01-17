import logging
import time
from discogs_client.exceptions import HTTPError
from json import JSONDecodeError
from .discogs_service import DiscogsService
from .discogs_matcher  import DiscogsMatcher
from .discogs_enricher import DiscogsEnricher
from config import UNKNOWN_ARTIST, VARIOUS_ARTISTS, UNKNOWN_ALBUM

logger = logging.getLogger("DiscogsManager")


class DiscogsManager:
    def __init__(self):
        self.discogs_service = DiscogsService()
        self.discogs_matcher = DiscogsMatcher()
        self.discogs_enricher = DiscogsEnricher()
    
    def apply(self, album):
        album_artists = album.artists
        artist = album_artists[0] if album_artists else None
        album_title = album.title
        album_year = album.year
        album_tracklist = album.tracklist
        track = album_tracklist[0].title if album_tracklist else None

        if (artist.name != UNKNOWN_ARTIST or artist.name != VARIOUS_ARTISTS) and album_title != UNKNOWN_ALBUM : # bypass unknown artist & album
            search_attempts = [
                dict(artist=artist, release_title=album_title, year=album_year, track=track),
                dict(release_title=album_title, year=album_year, track=track)
            ]

            for params in search_attempts:
                params = {k: v for k, v in params.items() if v} # filtre les valeurs vides

                results = self.discogs_service.search(params)

                if not results:
                    logger.info(f"[Discogs] Aucun résultat pour : {params['artist'].name if 'artist' in params else UNKNOWN_ARTIST} - {params['release_title']} - {params['year']} - {params['track']}")
                    continue
                
                for result in results:
                    if not result:
                        continue

                    try:
                        main_release = self._resolve_main_release(result)
                        if not main_release:
                            continue

                        match = self.discogs_matcher.find(album, main_release)
                        if match:
                            self.discogs_enricher.apply(album, match)
                            break

                    except HTTPError as e:
                        logger.warning(f"[Discogs] HTTPError avec un résultat: {e}")
                        if e.status_code == 429:
                            time.sleep(60)
                            continue
                    except JSONDecodeError as e:
                        logger.warning(f"[Discogs] JSONDecodeError réponse invalide (JSON): {e}")
                        time.sleep(60)
                        continue
                    except Exception as e:
                        logger.warning(f"[Discogs] Exception erreur avec un résultat: {e} - tpe {type(e)}")
                        continue
                    '''except Exception as e:
                        logger.warning(f"[Discogs] Exception erreur avec un résultat: {e} - tpe {type(e)}")
                        time.sleep(60)
                        break'''


    def _resolve_main_release(self, result):
        release_id = getattr(result, "id", None)
        if not release_id:
            return None

        release = self.discogs_service.get_release(release_id)

        master_id = release.data.get("master_id") if release and release.data else None
        if not master_id:
            return release

        master = self.discogs_service.get_master(master_id)
        if not master or not hasattr(master, "data"):
            return release  # fallback

        main_release_id = master.data.get("main_release")
        return self.discogs_service.get_release(main_release_id) or release
