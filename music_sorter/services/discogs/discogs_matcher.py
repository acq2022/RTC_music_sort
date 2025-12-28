import logging
from .discogs_result import DiscogsResult
from domain.album import Album

logger = logging.getLogger("DiscogsMatcher")


class DiscogsMatcher:

    def find(self, album, results):
        print('DiscogsMatcher find')

        for release in results:
            try:
                # Skip si release invalide ou n'a pas de tracklist
                if not release or not hasattr(release, "tracklist"):
                    continue

                # Force la récupération de la tracklist (lazy loading)
                tracklist = list(release.tracklist)

            except Exception as e:
                # Ignore les releases qui déclenchent une 404 ou autre erreur
                print(f"Skipping release due to error: {e}")
                continue

            # Vérification que tous les titres de l'album sont présents
            all_tracks_match = True
            for track_title in album.tracklist:
                if not getattr(track_title, "track_title", None):
                    all_tracks_match = False
                    break

                try:
                    # Recherche d'au moins un titre correspondant dans la release
                    track_found = any(
                        t.title and t.title.lower() == track_title.track_title.lower()
                        for t in tracklist
                    )
                except Exception as e:
                    print(f"Skipping track due to error: {e}")
                    track_found = False

                if not track_found:
                    all_tracks_match = False
                    break

            if all_tracks_match:
                return release  # Release trouvée

        return None  # Aucune release ne correspond





    def findZZZZ(self, album, results):
        print('DiscogsMatcher find')

        '''for release in results:
            if not release or not hasattr(release, "tracklist"):
                continue'''
        
        for release in results:
            # Ignore les releases invalides
            try:
                if not release or not hasattr(release, "tracklist"):
                    continue
                tracklist = list(release.tracklist)  # force la récupération
            except Exception as e:
                print(f"Skipping release due to error: {e}")
                continue


            for track_title in album.tracklist:
                if not track_title.track_title:
                    break

                if not any(
                    t.title
                    and t.title.lower() == track_title.track_title.lower()
                    for t in release.tracklist
                ):
                    break
            else:
                return release  # tous les titres matchent

        return None


    def findXXX(self, album, results):
        print('DiscogsMatcher find')
        match_release = None
        for i in range(results.count):
            release = results[i]
            if release:
                for track_title in album.tracklist:
                    track = next((t for t in release.tracklist if t.title.lower() == track_title.track_title.lower()), None) # Recherche si titres de morceaux similaires
                    if track:
                        match_release = release
                    else:
                        match_release = None
                        break
                    '''if track:
                        print("discogsMatcher...; album : ", album, type(album))
                        print("tracklist : ", album.tracklist, type(album.tracklist))
                        print("1e track : ", album.tracklist[0], type(album.tracklist[0]))
                        print("title : ", album.tracklist[0].track_title, type(album.tracklist[0].track_title))
                        print("track_number : ", album.tracklist[0].track_number, type(album.tracklist[0].track_number))

                        print("POSITION : ", album.tracklist.index(track_title))
                        print("track.position : ", track.position)



                        if track.position == str(album.index(track_title)): # Recherche si position des morceaux similaires
                            match_release = release
                        else:
                            break'''
            else:
                break
        return match_release
