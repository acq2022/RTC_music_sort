from services.discogs.discogs_manager import DiscogsManager
from services.discogs.discogs_service import DiscogsService
from services.discogs.discogs_matcher  import DiscogsMatcher
from services.discogs.discogs_enricher import DiscogsEnricher
from services.acoustid_service import AcoustIDService

class MetadataEnricher:
    def __init__(self):
        self.discogs_manager = DiscogsManager()
        self.discogs_service = DiscogsService()
        self.discogs_matcher = DiscogsMatcher()
        self.discogs_enricher = DiscogsEnricher()
        #self.acoustid = AcoustIDService()
    
    def enrich_albums(self, albums):
        for album in albums:
            self.discogs_manager.apply(album)
