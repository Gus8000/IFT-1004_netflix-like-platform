from mediatheque import Mediatheque
from show import Show
from utilisateur import AnnuaireUtilisateur


def afficher_menu_accueil_et_choisir_action():
    """
    Fonction permettant d'afficher le menu d'accueil, les choix disponibles
    et récupérer le choix de l'utilisateur.

    Returns:
        int: Le choix de l'utilisateur (une valeur entière entre 1 et 3).
    """
    choix_menu = None
    while choix_menu is None:
        try:
            print("Menu d'acceuil")
            print("1 - S'inscrire")
            print("2 - S'authentifier")
            print("3 - Quitter l'application")
            choix_menu = int(input("Veuillez entrer votre choix: "))
            assert 1 <= choix_menu <= 3
        except (ValueError, AssertionError):
            print("Votre choix n'est pas dans la liste des options. Veuillez réessayer.")
            choix_menu = None
    return choix_menu


def afficher_menu_utilisateur_et_choisir_action():
    """
    Fonction permettant d'afficher le menu utilisateur
    et récupérer le choix de l'utilisateur.

    Returns:
        int: Le choix de l'utilisateur (une valeur entière entre 1 et 7).
    """
    choix_menu = None
    while choix_menu is None:
        try:
            print("Menu utilisateur")
            print("1 - Rechercher des films ou séries avec une expression")
            print("2 - Rechercher des films ou séries selon le genre")
            print("3 - Rechercher des films ou séries selon les acteurs")
            print("4 - Afficher la médiathèque par ordre des shows les plus récemment ajoutés")
            print("5 - Afficher la médiathèque par ordre des shows les plus populaires")
            print("6 - Afficher la médiathèque par ordre des shows les mieux évalués")
            print("7 - Quitter l'application")
            choix_menu = int(input("Veuillez entrer votre choix: "))
            assert 1 <= choix_menu <= 7
        except (ValueError, AssertionError):
            print("Votre choix n'est pas dans la liste des options. Veuillez réessayer.")
            choix_menu = None
    return choix_menu


if __name__ == "__main__":
    fichier_des_utilisateurs = "ulflix-utilisateurs.txt"
    fichier_des_shows = "ulflix.txt"

    print("#" * 80, "###{:^74s}###".format("Bienvenue dans ULFlix"), "#" * 80, sep="\n")
    annuaire_utilisateur = AnnuaireUtilisateur(fichier_des_utilisateurs)
    choix = afficher_menu_accueil_et_choisir_action()
    if choix == 1:
        utilisateur = annuaire_utilisateur.inscrire()
    elif choix == 2:
        utilisateur = annuaire_utilisateur.authentifier()
    else:
        utilisateur = None

    if utilisateur is not None:
        mediatheque = Mediatheque(fichier_des_shows)

        selection_ids = mediatheque.filtrer_ids_sur_age(utilisateur.age)
        if utilisateur.abonnement == 1:
            temp = mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string("pays", utilisateur.pays)
            selection_ids = list(set(selection_ids).intersection(temp))

        mediatheque.reduire_liste_des_shows(selection_ids)

        print(f"Salut {utilisateur.nom.title()}! Tu as accès à {len(mediatheque)} films et séries télés.")

        continuer_programme = True
        while continuer_programme:
            choix_menu = afficher_menu_utilisateur_et_choisir_action()
            if choix_menu == 1:  # Rechercher des films ou séries avec une expression
                recherche = input("Veuillez entrer les termes de votre recherche: ")
                titre_ids = mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_string("titre", recherche)
                desc_ids = mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_string("description", recherche)
                selection_ids = list(set(titre_ids).union(desc_ids))
                print(f"{len(selection_ids)} résultats trouvés.")
                mediatheque.afficher_avec_pagination(
                    selection_ids,
                    nombre_de_shows_par_page=10,
                    attribut_pour_trier="popularite",
                )
                
            elif choix_menu == 2:  # Rechercher des films ou séries selon le genre
                genres = mediatheque.lister_valeurs_uniques_par_attribut("categories")

                print("Catégories disponibles:")
                for i, genre in enumerate(genres):
                    print(f"{i+1:>2} - {genre}")

                choix_categorie = None
                while choix_categorie is None:
                    try:
                        choix_categorie = int(input("Entrer votre choix de catégorie: "))
                        assert choix_categorie in range(1, len(genres) + 1)
                    except (ValueError, AssertionError):
                        print("Le choix de catégorie est invalide. Réessayer svp.")
                        choix_categorie = None
                
                choix_categorie = genres[choix_categorie - 1]
                selection_ids = mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string("categories", choix_categorie)
                print(f"{len(selection_ids)} résultats trouvés.")
                mediatheque.afficher_avec_pagination(
                    selection_ids,
                    nombre_de_shows_par_page=10,
                    attribut_pour_trier="popularite",
                )

            elif choix_menu == 3:  # Rechercher des films ou séries selon les acteurs
                recherche = input("Veuillez entrer le nom ou prénom d'un acteur: ")
                selection_ids = mediatheque.filtrer_ids_sur_attribut_par_inclusion_de_liste_de_string("acteurs", recherche)
                print(f"{len(selection_ids)} résultats trouvés.")
                mediatheque.afficher_avec_pagination(
                    selection_ids,
                    nombre_de_shows_par_page=10,
                    attribut_pour_trier="popularite",
                )

            elif choix_menu == 4:  # Afficher les films ou séries les plus récents
                mediatheque.afficher_avec_pagination(
                    nombre_de_shows_par_page=10, attribut_pour_trier="date_ajout"
                )

            elif choix_menu == 5:  # Afficher les films ou séries les plus populaires
                mediatheque.afficher_avec_pagination(
                    nombre_de_shows_par_page=10, attribut_pour_trier="popularite"
                )

            elif choix_menu == 6:  # Afficher les films ou séries les plus mieux évalués
                mediatheque.afficher_avec_pagination(
                    nombre_de_shows_par_page=10, attribut_pour_trier="note"
                )

            else:
                continuer_programme = False
