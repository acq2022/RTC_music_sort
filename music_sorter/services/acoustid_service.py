import logging
import os
import time
import acoustid
import musicbrainzngs

logger = logging.getLogger("AcoustIDService")

# --- Configuration ---
# Clé API AcoustID
ACOUSTID_API_KEY = os.getenv("ACOUSTID_API_KEY")
if not ACOUSTID_API_KEY:
    raise RuntimeError("Clé API AcoustID manquante. Mets-la dans la variable d'environnement ACOUSTID_API_KEY.")

# UserAgent MusicBrainz (remplace par ton mail)
musicbrainzngs.set_useragent("MonApp", "1.0", "ton.email@example.com")

class AcoustIDService:
    # Identifier un fichier audio et retourner Titre, Artiste, Album, Année et Score
    def identify(self, file_path):
        try:
            # Appel AcoustID
            results = acoustid.match(ACOUSTID_API_KEY, file_path)

            for score, recording_id, title, artist in results:
                # Récupérer infos détaillées via MusicBrainz
                album = ""
                date = ""
                for attempt in range(3):
                    try:
                        time.sleep(1.1)
                        mb_result = musicbrainzngs.get_recording_by_id(recording_id, includes=["releases"])
                        recording = mb_result.get("recording", {})
                        
                        # Artiste (plus fiable via MusicBrainz)
                        if "artist-credit" in recording and recording["artist-credit"]:
                            artist = recording["artist-credit"][0]["artist"]["name"]
                        
                        # Album et année
                        releases = recording.get("release-list", [])
                        if releases:
                            album = releases[0].get("title", "")
                            date = releases[0].get("date", "")
                        break

                    
                    except musicbrainzngs.NetworkError as e:
                        logger.warning(f"Erreur réseau MusicBrainz pour {file_path} (tentative {attempt+1}/{3}) : {e}")
                        time.sleep(2)
                    except musicbrainzngs.ResponseError as e:
                        logger.warning(f"Erreur réponse MusicBrainz pour {file_path} :", e)
                        break
                    except Exception as e:
                        logger.warning(f"Erreur inattendue MusicBrainz pour {file_path} : {e}")
                        break

                # Retourner les infos
                return {
                    "path": file_path,
                    "title": title or None,
                    "artists": [artist] or None,
                    "album_title": album or None,
                    "year": date or None,
                    "score": score
                }

        except acoustid.NoBackendError:
            logger.warning(f"Erreur : Chromaprint non trouvé pour {file_path}")
        except acoustid.FingerprintGenerationError:
            logger.warning(f"Erreur de génération d'empreinte pour {file_path}")
        except acoustid.WebServiceError as e:
            logger.warning(f"Erreur API AcoustID pour {file_path} : {e}")
        except Exception as e:
            logger.warning(f"Erreur Musicbrainzngs: {e} - tpe {type(e)}")

        # En cas d'erreur, renvoyer un dictionnaire vide pour ce fichier
        return {
            "path": file_path,
            "title": None,
            "artists": None,
            "album_title": None,
            "year": None,
            "score": None
        }