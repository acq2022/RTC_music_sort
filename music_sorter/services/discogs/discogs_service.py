import logging
import discogs_client
from typing import List
#from .discogs_result import DiscogsResult

logger = logging.getLogger("DiscogsService")

class DiscogsService:
    def __init__(self):
        self.client = discogs_client.Client(
            "MusicSort",
            user_token="gBvGbGazBqsXgXblCHFqaLSdtctFHXTHPfnFyiSV"
        )
        print('DiscogsService init')
    
    def search_release(self, album):
        print('DiscogsService search_release')
        album_artist = album.artist
        album_title = album.title
        album_year = album.year

        params = dict(artist=album_artist, year=album_year, title=album_title)
        params["type"] = "release"
        params = {k: v for k, v in params.items() if v}

        try:
            results = self.client.search(**params)
            if not results:
                logging.info(f'album non trouvé sur discogs')
        except Exception as e:
            logger.debug(f"[Discogs] Skipped result: {e}")
            return None
        
        return results
    
    def get_main_releaseXXX(self, release):
        print('get_main_release')
        main_release = release
        master_id = release.data['master_id']
        master = self.client.master(master_id)

        if master:
            main_release_id = master.main_release.id
            main_release = self.client.release(main_release_id)

        return main_release
    
    def get_main_release(self, release):
        print('get_main_release')
        main_release = release

        master_id = release.data.get('master_id')
        if not master_id:
            return main_release

        try:
            master = self.client.master(master_id)
        except Exception as e:
            print(f"Master {master_id} inaccessible : {e}")
            return main_release

        if master and getattr(master, "main_release", None):
            try:
                main_release = self.client.release(master.main_release.id)
            except Exception as e:
                print(f"Main release inaccessible : {e}")

        return main_release
