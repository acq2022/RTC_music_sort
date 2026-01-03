from services.discogs.discogs_manager import DiscogsManager
from services.acoustid_service import AcoustIDService

class MetadataEnricher:
    def __init__(self):
        self.discogs_manager = DiscogsManager()
        #self.acoustid = AcoustIDService()
    
    def enrich_albums(self, albums):
        for album in albums:
            self.discogs_manager.apply(album)
