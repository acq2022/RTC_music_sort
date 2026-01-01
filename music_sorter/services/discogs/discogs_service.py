import logging
import discogs_client
from typing import List
from config import USER_AGENT, USER_TOKEN
#from .discogs_result import DiscogsResult

logger = logging.getLogger("DiscogsService")

class DiscogsService:
    def __init__(self):
        self.client = discogs_client.Client(USER_AGENT, user_token=USER_TOKEN)

    
    def search(self, params):
        try:
            results = self.client.search(**params)
            if not results:
                logger.info(f' {params} : non trouvé sur discogs :(')
            else:
                logger.info(f' {params} : trouvé sur discogs :)')
        except Exception as e:
            logger.debug(f"[Discogs] Skipped result: {e}")
            return None
        
        return results
    
    
    def get_release(self, id):
        try:
            release = self.client.release(id)
        except Exception as e:
            logger.debug(f"[Discogs] Release {id} inaccessible {e}")
            return None
        return release
    
    
    def get_master(self, id):
        try:
            master = self.client.master(id)
        except Exception as e:
            logger.debug(f"[Discogs] Master {id} inaccessible {e}")
            return None
        return master
    