import logging
import os
import time
import discogs_client

logger = logging.getLogger("DiscogsService")

USER_AGENT = os.getenv("USER_AGENT")
if not USER_AGENT:
            raise RuntimeError("USER_AGENT discogs manquant. Mets-la dans la variable d'environnement USER_AGENT.")
USER_TOKEN = os.getenv("USER_TOKEN")
if not USER_TOKEN:
            raise RuntimeError("USER_TOKEN discogs manquant. Mets-la dans la variable d'environnement USER_TOKEN.")


class DiscogsService:
    MIN_INTERVAL = 1.0  # secondes entre chaque requête
    _last_request = 0   # timestamp de la dernière requête

    def __init__(self):
        self.client = discogs_client.Client(USER_AGENT, user_token=USER_TOKEN)


        ACOUSTID_API_KEY = os.getenv("ACOUSTID_API_KEY")
        if not ACOUSTID_API_KEY:
            raise RuntimeError("Clé API AcoustID manquante. Mets-la dans la variable d'environnement ACOUSTID_API_KEY.")

    
    def _throttle(self):
        elapsed = time.time() - self._last_request
        if elapsed < self.MIN_INTERVAL:
            time.sleep(self.MIN_INTERVAL - elapsed)
        self._last_request = time.time()

    
    def search(self, params):
        self._throttle()
        try:
            results = self.client.search(**params)
            if not results:
                #logger.info(f' {params} : non trouvé sur discogs :(')
                return []
            #logger.info(f' {params} : trouvé sur discogs :)')
            return results
        except Exception as e:
            logger.warning(f"[Discogs] Skipped result: {e}")
            return []
    
    
    def get_release(self, id):
        self._throttle()
        try:
            return self.client.release(id)
        except Exception as e:
            logger.warning(f"[Discogs] Release {id} inaccessible {e}")
            return []
    
    
    def get_master(self, id):
        self._throttle()
        try:
            return self.client.master(id)
        except Exception as e:
            logger.debug(f"[Discogs] Master {id} inaccessible {e}")
            return []
    