from services.discogs.discogs_manager import DiscogsManager

class MetadataEnricher:
    def __init__(self):
        self.discogs_manager = DiscogsManager()
    
    def enrich_albums(self, albums):
        for album in albums:
            self.discogs_manager.apply(album)
