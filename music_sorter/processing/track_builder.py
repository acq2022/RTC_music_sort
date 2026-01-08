from services.tags_reader import TagsReader
from services.acoustid_service import AcoustIDService
from domain.track import Track

class TrackBuilder:
    def build(self, paths):
        tags_reader = TagsReader()
        acoustid = AcoustIDService()

        tags = []
        paths_tracks_to_shazam = []
        infos_from_shazam = []
        tracks = []

        # récupération des tags => TAG_READER
        for path in paths:
            tags.append(tags_reader.read(path))
        
        # récupération des paths des tracks dont l'album est inconnu
        for tag in tags:
            if tag["album_title"] == None:
                paths_tracks_to_shazam.append(tag["path"])

        # récupération des infos shazam des albums inconnus => ACOUSTID
        for path in paths_tracks_to_shazam:
            info = acoustid.identify(path)
            score = info["score"]
            if score and score >= 0.9:  # seulement si infos fiables
                infos_from_shazam.append(info)

        # création d'un dictionnaire pour lookup rapide
        lookup = {tag["path"]: tag for tag in infos_from_shazam}
        
        # mise à jour de tags
        # création des Track
        for tag in tags:
            if tag["path"] in lookup:
                tag.update(lookup[tag["path"]])

            tracks.append(Track(
                path = tag["path"],
                album_artists = tag["album_artists"],
                artists = tag["artists"],
                year = tag["year"],
                album_title = tag["album_title"],
                label = tag["label"],
                catno = tag["catno"],
                track_number = tag["track_number"],
                total_tracks = tag["total_tracks"],
                title = tag["title"],
                duration = tag["duration"],
                genre = tag["genre"],
                bpm = tag["bpm"],
                website = tag["website"],
                disc_number = tag["disc_number"],
                original_date = tag["original_date"],
                release_country = tag["release_country"],
                language = tag["language"],
            ))
        
        return tracks