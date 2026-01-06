class Parser:

    @staticmethod
    def nettoyer(valeur) -> str | None:
        if not valeur or not isinstance(valeur, str):
            return None
        valeur = valeur.strip()
        return valeur or None
    

    @staticmethod
    def pipeline(valeur, *etapes):
        for etape in etapes:
            if valeur is None:
                return None
            valeur = etape(valeur)
        return valeur
    

    @staticmethod
    def extract_first_part(valeur: str) -> str | None:
        return Parser.pipeline(
            valeur,
            Parser.nettoyer,
            Parser.extraire_partie(0, retourner_si_absent=True)
        )
    

    @staticmethod
    def extract_second_part(valeur: str) -> str | None:
        return Parser.pipeline(
            valeur,
            Parser.nettoyer,
            Parser.extraire_partie(1)
        )
    

    @staticmethod
    def extraire_partie(index: int, separateurs=("/", "-"), retourner_si_absent: bool = False):
        def etape(valeur: str) -> str | None:
            for sep in separateurs:
                if sep in valeur:
                    parties = [p.strip() for p in valeur.split(sep)]
                    return parties[index] if index < len(parties) else None
            return valeur if retourner_si_absent and index == 0 else None
        return etape
    

    @staticmethod
    def extract_year(date_str):
        from datetime import datetime
        import re

        formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y", "%d - %m - %Y", "%Y - %m - %d"]
        
        def annee_par_datetime(val):
            for fmt in formats:
                try:
                    return datetime.strptime(val, fmt).strftime("%Y")
                except ValueError:
                    pass
            return None

        def annee_par_regex(val):
            match = re.search(r"\b(19|20)\d{2}\b", val)
            return match.group() if match else None

        def tenter(*etapes):
            for e in etapes:
                resultat = e(date_str)
                if resultat is not None:
                    return resultat
            return None

        return Parser.pipeline(
            date_str,
            Parser.nettoyer,
            lambda v: tenter(annee_par_datetime, annee_par_regex)
        )
    
    
    @staticmethod
    def normalize_artist(name: str) -> str:
        return (
            name.strip()
                .lower()
                .replace("_", " ")
        )
    

    @staticmethod
    def normalize_track_number(value: str | None) -> str | None:
        import re
        if not value:
            return None

        value = str(value).strip()
        
        # Recherche un pattern disque-piste : "1-1", "2/3", "1.04", ou juste "1"
        match = re.match(r"(\d+)([-/.])?(\d+)?", value)
        if match:
            first = match.group(1)      # disque ou premier nombre
            sep = match.group(2) or ""  # séparateur ou vide
            second = match.group(3)     # piste

            # Si second existe, on le met sur 2 chiffres
            if second and second.isdigit():
                second = f"{int(second):02d}"
                return f"{first}{sep}{second}"

            # Sinon, on met first sur 2 chiffres
            return f"{int(first):02d}"

        return value



    @staticmethod
    def join_normalized_terms(txt_in: str) -> str:
        import re
        s = txt_in.lower()                                          # passage en minuscule
        s = s.replace("-", " ")                                     # remplace les tirets
        s = re.sub(r"\s*(?:&|,|\band\b|\+)\s*", ",", s)             # remplace les & , and + par une virgule 
        s = re.sub(r"\s+", " ", s)                                  # évite les espaces multiples ("a   b" → "a b")
        txt_out = [a.strip() for a in s.split(",") if a.strip()]    # découpe sur les virgules, enlève les espaces en trop, supprime les éléments vides ("a,b,, c " → ["a", "b", "c"])
        txt_out.sort()                                              # tri alphabétique
        return " & ".join(txt_out)
    

    # Nettoie une chaîne pour l'utiliser comme nom de fichier ou dossier
    @staticmethod
    def sanitize_path(name, replacement="_", max_length=255):
        import re
        import unicodedata
        from config import WINDOWS_RESERVED_NAMES, INVALID_CHARS, UNKNOWN_FOLDER     
        if name is None:
            return UNKNOWN_FOLDER     
        name = str(name)                                                        # Conversion explicite en str
        name = unicodedata.normalize("NFKD", name)                              # Normalisation Unicode (é → e, etc.)
        name = "".join(c for c in name if not unicodedata.combining(c))      
        name = re.sub(INVALID_CHARS, replacement, name)                         # Suppression des caractères interdits      
        name = re.sub(r"\s+", " ", name)                                        # Suppression des espaces multiples      
        name = name.strip(" .")                                                 # Trim espaces et points (Windows)
        if name.upper() in WINDOWS_RESERVED_NAMES:                              # Éviter les noms réservés Windows
            name = f"_{name}"
        if len(name) > max_length:                                              # Longueur maximale (sécurité)
            name = name[:max_length].rstrip(" .")
        return name or "Unknown"
    

    @staticmethod
    def sanitize_name(name: str | None) -> str:
        import re
        from config import UNKNOWN_FOLDER
        if not name:
            return UNKNOWN_FOLDER
        name = name.strip()   # CRUCIAL
        name = re.sub(r'[<>:"/\\|?*]', "_", name)
        return name
    
    
    @staticmethod
    def sanitize_track_title_name(name: str | None) -> str | None:
        import re
        if not name:
            return None
        name = name.strip()   # CRUCIAL
        name = re.sub(r'[<>:"/\\|?*]', "_", name)
        return name