import math

from show import Show


class Mediatheque:
    def __init__(self, chemin_fichier):
        """
        Cette méthode permet d'initialiser une médiathue en chargeant
        en mémoire la base de données des shows.

        Args:
            chemin_fichier (str): Le chemin menant au fichier
            contenant la médiathèque.
        """
        self.shows = self.charger_shows_depuis_fichier(chemin_fichier)

    def charger_shows_depuis_fichier(self, chemin_fichier):
        """
        Cette fonction permet de lire et charger en mémoire la médiathèque.
        Elle retourne un dictionnaire où chaque clé représente l'identifiant
        d'un show et la valeur associée représente un objet Show.
        L'objet show est obtenu en se servant de la méthode de classe
        Show.creer_show_via_ligne_et_ligne_des_titres que vous devez implémenter.
        
        Args:
            chemin_fichier (str): Le chemin menant au fichier contenant la médiathèque.

        Returns:
            dict: Dictionnaire des shows de la médiathèque.
                  Les clés sont des show_ids et les valeurs sont des objets de
                  type Show.
        """
        shows = {}

        with open(chemin_fichier, encoding="utf-8") as fichier:
            ligne_des_titres, *lignes_des_shows = [ligne.strip() for ligne in fichier]

            for ligne in lignes_des_shows:
                show = Show.creer_show_via_ligne_et_ligne_des_titres(ligne, ligne_des_titres)
                shows[show.identifiant] = show

        return shows

    def __len__(self):
        """
        Retourne le nombre de shows dans la médiatheque.
        
        Voici un exemple d'utilisation en supposant que la variable mediatheque
        fait référence à un objet de type Mediatheque: len(mediatheque)
        """
        return len(self.shows)

    def __getitem__(self, index):
        return self.shows[index]

    def reduire_liste_des_shows(self, identifiants_a_garder):
        """
        Méthode permettant de supprimer de la médiathèque, les shows dont
        les identifiants ne font pas partie de la liste des identifiants à 
        garder (liste fournie par le paramètre identifiants_a_garder).

        Pour la suppresion, cela ressemblera à quelque chose comme:
        del self.shows[show_id]
        (À adapter bien évidemment!)

        Args:
            identifiants_a_garder (list): Liste des identifiants des shows
            à ne pas supprimer de la médiathèque.
        """
        identifiants_a_eliminer = set(list(self.shows.keys())).difference(identifiants_a_garder)
        for show_id in identifiants_a_eliminer:
            del self.shows[show_id]

    def filtrer_ids_sur_attribut_par_inclusion_de_string(self, attribut, valeur):
        """
        Méthode permettant de récupérer uniquement les identifiants des
        shows de la médiathèque où la valeur de l'attribut passé
        en argument contient la valeur passée en argument.
        Le filtre est insensible à la casse.

        Args:
            attribut (str): Attribut de filtre
            valeur (str): Valeur de filtre.

        Returns:
            list: Liste des show_ids respectant les critères du filtre.
        """
        val = valeur.lower() if isinstance(valeur, str) else valeur
        return [show_id for show_id, show in self.shows.items() if val in getattr(show, attribut).lower()]

    def filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string(self, attribut, valeur):
        """
        Méthode permettant de récupérer uniquement les identifiants des 
        shows de la médiathèque où la valeur de l'attribut passé en 
        argument contient la valeur passée en argument.
        Cette méthode est différente de la précédente dans
        le sens où la valeur de l'attribut contient des listes
        de chaine de charactères. Le filtre est insensible à la casse.

        Args:
            attribut (str): Attribut de filtre
            valeur (str): Valeur de filtre.

        Returns:
            list: Liste des show_ids respectant les critères du filtre.
        """
        filtered_shows = []
        val = valeur.lower() if isinstance(valeur, str) else valeur
        for show_id in self.shows:
            show = self.shows[show_id]
            show_value = getattr(show, attribut)
            if not isinstance(show_value, list): show_value = [show_value]
            if val in [p.lower() for p in show_value]:
                filtered_shows.append(show_id)
        return filtered_shows

    def filtrer_ids_sur_age(self, age_utilisateur):
        """
        Méthode permettant de récupérer uniquement les shows de
        la médiathèque où la limite d'âge est respectée (i.e des shows
        où le classement permet à l'utilisateur de regarder).

        Args:
            age_utilisateur (int): Âge de l'utilisateur

        Returns:
            list: Liste des show_ids respectant la limite d'âge.
        """
        return [show_id for show_id, show in self.shows.items() if age_utilisateur >= show.age_minimum_requis]

    def trier_ids_par_attribut(self, show_ids, attribut):
        """
        Méthode permettant de trier les show_ids d'une médiathèque
        en ordre décroissant en se basant sur un attribut particulier
        des shows. Nous utilisons la méthode native sorted qui
        opère sur les listes.

        Args:
            show_ids (list): Identifiants des shows à trier
            attribut (str): Attribut de tri

        Returns:
            list: Liste des show_ids triée en ordre décroissant 
                  de l'attribut d'intérêt.
        """
        return sorted(show_ids, key=lambda show_id: getattr(self.shows[show_id], attribut), reverse=True)

    def lister_valeurs_uniques_par_attribut(self, attribut):
        """
        Méthode permettant de récupérer un attribut de type liste
        de la médiathèque. En gros, vous devez retourner les valeurs
        uniques contenues dans toutes les listes de cet attribut.
        Ces valeurs devront être triées par ordre croissant.

        Args:
            attribut (str): Attribut dont le contenu devra contenir
            des valeurs uniques.

        Returns:
            list: Liste des valeurs uniques de l'attribut de type list.
        """
        return sorted(list(set([el for show in self.shows.values() for el in getattr(show, attribut)])))

    def afficher_avec_pagination(
        self,
        identifiants=None,
        nombre_de_shows_par_page=10,
        attribut_pour_trier="date_ajout",
    ):
        """
        Méthode permettant d'afficher l'ensemble des shows présents dans la
        médiathèque. Cette méthode offre la pagination de l'affichage s'il
        y a trop de shows dans la médiathèque.

        Args:
            identifiants (list): Liste des show_ids à afficher.
            nombre_de_shows_par_page (int, optional): Nombre de shows
            à afficher par page. La valeur par défaut est de 10.

            attribut_pour_trier (str): Attribut de tri.
        """
        show_ids = list(self.shows.keys()) if identifiants is None else identifiants
        show_ids = self.trier_ids_par_attribut(show_ids, attribut_pour_trier)
        nb_pages = int(math.ceil(len(show_ids) / nombre_de_shows_par_page))
        i = 0
        while i < nb_pages:
            print(f"Page: {i+1} sur {nb_pages}")
            for j in range(i * nombre_de_shows_par_page, min(len(show_ids), (i + 1) * nombre_de_shows_par_page)):
                print(self.shows[show_ids[j]])
            print(f"Page: {i+1} sur {nb_pages}")
            choix = input("Entrer s [page suivante], p [page précédente], q [quitter]: ")
            if choix.lower() == "s":
                if i < nb_pages - 1:
                    i += 1
            elif choix.lower() == "p":
                if i > 0:
                    i -= 1
            else:
                break

