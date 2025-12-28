from services.discogs.discogs_service import DiscogsService
from services.discogs.discogs_matcher  import DiscogsMatcher
from services.discogs.discogs_enricher import DiscogsEnricher
from services.acoustid_service import AcoustIDService

class MetadataEnricher:
    def __init__(self):
        print("MetadataEnricher init")
        self.discogs_service = DiscogsService()
        self.discogs_matcher = DiscogsMatcher()
        self.discogs_enricher = DiscogsEnricher()
        #self.acoustid = AcoustIDService()
    
    def enrich_albums(self, albums):
        for album in albums:
            results = self.discogs_service.search_release(album)
            match = self.discogs_matcher.find(album, results)

            if match:
                match = self.discogs_service.get_main_release(match)
                self.discogs_enricher.apply(album, match)
                print("MetadataEnricher enrich_albums END")

    '''def enrich_tracks(self, tracks):
        for track in tracks:
            if not track.is_identified:
                self.acoustid.identify(track)'''
