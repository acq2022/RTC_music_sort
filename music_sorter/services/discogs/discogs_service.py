import logging
import time
import discogs_client
from typing import List
from config import USER_AGENT, USER_TOKEN

logger = logging.getLogger("DiscogsService")

class DiscogsService:
    MIN_INTERVAL = 1.0  # secondes entre chaque requête
    _last_request = 0   # timestamp de la dernière requête

    def __init__(self):
        self.client = discogs_client.Client(USER_AGENT, user_token=USER_TOKEN)

    
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
                logger.info(f' {params} : non trouvé sur discogs :(')
                return []
            logger.info(f' {params} : trouvé sur discogs :)')
            return results
        except Exception as e:
            logger.debug(f"[Discogs] Skipped result: {e}")
            return []
    
    
    def get_release(self, id):
        self._throttle()
        try:
            return self.client.release(id)
        except Exception as e:
            logger.debug(f"[Discogs] Release {id} inaccessible {e}")
            return []
    
    
    def get_master(self, id):
        self._throttle()
        try:
            return self.client.master(id)
        except Exception as e:
            logger.debug(f"[Discogs] Master {id} inaccessible {e}")
            return []
    