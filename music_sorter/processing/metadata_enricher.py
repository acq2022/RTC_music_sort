from services.discogs.discogs_service import DiscogsService
from services.discogs.discogs_service import DiscogsMatcher
from services.discogs.discogs_service import DiscogsEnricher
from services.acoustid_service import AcoustIDService

class MetadataEnricher:
    def __init__(self):
        self.discogs_service = DiscogsService()
        self.discogs_matcher = DiscogsMatcher()
        self.discogs_enricher = DiscogsEnricher()
        self.acoustid = AcoustIDService()
    
    def enrich_albums(self, albums):
        for album in albums:
            results = self.discogs_service.search(album)
            match = self.discogs_matcher.select(album, results)

            if match:
                self.discogs_enricher.apply(album, match)

    def enrich_tracks(self, tracks):
        for track in tracks:
            if not track.is_identified:
                self.acoustid.identify(track)
