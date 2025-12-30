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
