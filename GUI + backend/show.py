import datetime
import textwrap


class Show:
    LIMITE_MINIMUM_D_AGE_PAR_CLASSEMENT = {
        # Pour regarder un film ou série d'une catégorie, votre âge doit être supérieur à la limite.
        "TV-Y": 0,  # Le programme est évalué comme étant approprié aux enfants.
        "TV-Y7": 7,  # Le programme est destiné aux enfants âgés de 7 ans et plus.
        "TV-Y7-FV": 7,  # Le programme est destiné aux enfants âgés de 7 ans et plus.
        "TV-G": 10,  # La plupart des parents peuvent considérer ce programme comme approprié pour les enfants.
        "TV-PG": 14,  # Contient des éléments que les parents peuvent considérer inappropriés pour les enfants
        "TV-14": 14,  # Contient des éléments pouvant être inappropriés pour les enfants de moins de 14 ans
        "TV-MA": 17,  # Uniquement réservé aux adultes et inapproprié pour la jeune audience de moins de 17 ans.
        "G": 0,  # Tous les âges sont admis. Rien qui offenserait les parents pour le visionnage par les enfants.
        "PG": 7,  # Certains matériaux peuvent ne pas convenir aux jeunes enfants
        "PG-13": 13,  # Certains contenus peuvent ne pas convenir aux enfants de moins de 13 ans.
        "R": 17,  # Les moins de 17 ans doivent être accompagnés d'un parent ou d'un tuteur adulte.
        "NC-17": 18,  # Personne de 17 ans et moins admis. Clairement adulte. Les enfants ne sont pas admis.
        "NR": 13,  # Non-rated donc par défaut, il doit être considéré comme PG-13
        "UR": 13,  # Unrated donc par défaut, il doit être considéré comme PG-13
        "": 13,  # Si la valeur est manquante, donc par défaut, il doit être considéré comme PG-13
    }

    def __init__(self, identifiant, titre, description, langue, popularite, note, type_, directeurs, acteurs, pays, date_ajout, annee_sortie, classement, duree, categories):
        """
        Construit un show à partir des valeurs passées en argument.

        show = Show(identifiant="s1", titre="3%", description="In a future where the elite inhabit an island paradise far from the crowded slums, you get one chance to join the 3% saved from squalor.", langue="pt", popularite=64.066, note=7.4, type="TV Show", directeurs=[], acteurs=["João Miguel", "Bianca Comparato", "Michel Gomes", "Rodolfo Valente", "Vaneza Oliveira", "Rafael Lozano", "Viviane Porto", "Mel Fronckowiak", "Sergio Mamberti", "Zezé Motta", "Celso Frateschi"], pays="Brazil", date_ajout=datetime.datetime(2020, 8, 14, 0, 0), annee_sortie=2020, classement="TV-MA", duree="4 Seasons", categories=['International TV Shows', 'TV Dramas', 'TV Sci-Fi & Fantasy'])
        """
        self.identifiant = identifiant
        self.titre = titre
        self.description = description
        self.langue = langue
        self.popularite = popularite
        self.note = note
        self.type = type_
        self.directeurs = directeurs
        self.acteurs = acteurs
        self.pays = pays
        self.date_ajout = date_ajout
        self.annee_sortie = annee_sortie
        self.classement = classement
        self.duree = duree
        self.categories = categories

    @classmethod
    def creer_show_via_ligne_et_ligne_des_titres(cls, ligne, ligne_des_titres):
        """
        Méthode permettant de convertir une chaîne de caractères représentant un show
        en un objet de type Show.
        Vous pourrez utiliser le paramètre ligne_des_titres afin de faire
        correspondre les valeurs aux attributs du show.
        Les valeurs sont fournies par le paramètre ligne et le séparateur des éléments
        de la ligne est '|'.

        Args:
            ligne (str): La ligne à convertir en un objet Show.
            ligne_des_titres (str): La première ligne contenant l'ensemble des titres.

        Returns:
            Show: Un objet Show représentant le show.
        """
        data = {
            cle: valeur
            for cle, valeur in zip(ligne_des_titres.split("|"), ligne.split("|"))
        }
        data["identifiant"] = data.pop("show_id")
        data["type_"] = data.pop("type")
        data["acteurs"] = [] if len(data["acteurs"]) == 0 else data["acteurs"].split(", ")
        data["pays"] = data["pays"].split(", ")
        data["directeurs"] = [] if len(data["directeurs"]) == 0 else data["directeurs"].split(", ")
        data["categories"] = [] if len(data["categories"]) == 0 else data["categories"].split(", ")
        data["popularite"] = float(data["popularite"])
        data["note"] = float(data["note"])
        data["annee_sortie"] = int(data["annee_sortie"])
        date = data["date_ajout"] if (data["date_ajout"] != "") else "January 1, 2000"
        # La chaîne de format "%B %d, %Y" équivaut à des dates sous la forme "August 14, 2020"
        data["date_ajout"] = datetime.datetime.strptime(date.strip(), "%B %d, %Y")

        return cls(**data)

    def __str__(self):
        """
        Cette méthode vous permet de faire print(show) pour un objet de type Show
        """
        sdate = "Ajouté le " + self.date_ajout.strftime("%d %B %Y")
        pop = f"Note: [{self.note:.1f}/10] Popularité: {self.popularite:.1f}"
        repr_ = f"""
        {self.type:<10s} - {self.titre:>50s} ({self.langue.upper()}) {pop:>100s}
        Année: {str(self.annee_sortie):<10s} Durée: {self.duree:<10s} {sdate:>130s}
        Synopsis: {textwrap.shorten(self.description, width=150, placeholder="..."):<}
        Acteurs: {"Inconnus" if len(self.acteurs) == 0 else ", ".join(self.acteurs):<50s}
        Directeurs: {"Inconnus" if len(self.directeurs) == 0 else ", ".join(self.directeurs):<50s}
        """
        return repr_

    @property
    def age_minimum_requis(self):
        """
        Cette méthode permet de récupérer l'âge minimum requis pour le show.
        Vous allez devoir utiliser la constante de classe
        LIMITE_MINIMUM_D_AGE_PAR_CLASSEMENT et l'attribut d'instance classement.

        Returns:
            int: Âge minimum requis pour le show.
        """
        return Show.LIMITE_MINIMUM_D_AGE_PAR_CLASSEMENT[self.classement]
