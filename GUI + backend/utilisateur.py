import os

from utils import HacheurDeMotDePasse, est_une_adresse_email_valide

from exceptions import *

class Utilisateur:
    def __init__(self, nom, email, age, pays, abonnement, mot_de_passe):
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.age = int(age)
        self.pays = pays
        self.abonnement = int(abonnement)


class AnnuaireUtilisateur:
    def __init__(self, chemin_base_de_donnees):
        self.chemin_base_de_donnees = chemin_base_de_donnees
        
        if os.path.exists(self.chemin_base_de_donnees):
            with open(self.chemin_base_de_donnees, encoding="utf-8") as fichier:
                lignes = [ligne.strip() for ligne in fichier if ligne != '\n']
        else:
            lignes = []

        self.utilisateurs = [Utilisateur(*ligne.split(",")) for ligne in lignes]

    def inscrire(self, nom, email, mot_de_passe, age, pays, abonnement):                            # reste à faire exceptions: si rien est écrit pour age et abonnement
                                                                                        # quand les infos de l'utilisateur sont récupérées par get(), elle sont toutes des str, donc, ici,
        if len(nom) == 0 or nom.isspace():                                              #      toutes les infos sont des str (peut causer problèmes pour age et abonnement)
            raise ErreurInscription("le champ 'nom' ne peut pas être vide")

        if len(email) == 0 or email.isspace():
            raise ErreurInscription("le champ 'email' ne peut pas être vide")
        adresses_emails_existantes = set([u.email for u in self.utilisateurs])
        if not est_une_adresse_email_valide(email):
            raise ErreurInscription("L'adresse email entrée est invalide.")
        if email in adresses_emails_existantes:
            raise ErreurInscription(
                "Un utilisateur est déjà inscrit avec cette adresse email. "
                "Veuillez vous connecter si vous êtes cet utilisateur ou utilisez une autre adresse email."
            )

        if len(mot_de_passe) == 0 or mot_de_passe.isspace():
            raise ErreurInscription("le champ 'mot de passe' ne peut pas être vide")
        if len(mot_de_passe) < 6 or mot_de_passe.isspace():
            raise ErreurInscription("Le mot de passe doit faire au minimum 6 caractères.")

        hash_mot_de_passe = HacheurDeMotDePasse.hacher(mot_de_passe)

        if age is None:
            raise ErreurInscription("le champ 'âge' ne peut pas être vide")                             # ne semble pas fonctionner
        ages = ""
        for x in range(1, 100):
            x = str(x)
            ages += x
        if age not in ages:
            raise ErreurInscription("L'âge doit être un entier positif.")
        else:
            age = int(age)
            if age <= 0:
                raise ErreurInscription("L'âge doit être un entier positif.")


        if len(pays) == 0 or pays.isspace():
            raise ErreurInscription("Vous devez entrer un pays valide.")


        if age is None:
            raise ErreurInscription("le champ 'abonnement' ne peut pas être vide")                      # ne semble pas fonctionner
        abonnement = int(abonnement)
        if abonnement == 1 or abonnement ==2:
            pass
        else:
            raise ErreurInscription("Le type d'abonement doit être 1 pour régional ou 2 pour international.")

        utilisateur = Utilisateur(
            nom=nom,
            email=email,
            age=age,
            pays=pays,
            abonnement=abonnement,
            mot_de_passe=hash_mot_de_passe,
        )

        with open(self.chemin_base_de_donnees, mode="a", encoding="utf-8") as fichier:
            fichier.write(",".join([nom, email, str(age), pays, str(abonnement), hash_mot_de_passe]) + "\n")

        return utilisateur

    def authentifier(self, email, password):

        adresses_emails_existantes = set([u.email for u in self.utilisateurs])

        if not est_une_adresse_email_valide(email):
            raise ErreurAuthentifier("L'adresse e-mail entrée est non valide")

        if email not in adresses_emails_existantes:
            raise ErreurAuthentifier("Nous n'avons trouvé aucun utilisateur avec cette adresse email au niveau de notre système.")

        utilisateur = [u for u in self.utilisateurs if u.email == email][0]

        if not HacheurDeMotDePasse.verifier(utilisateur.mot_de_passe, password):
            raise ErreurAuthentifier("Mot de passe incorrect.")

        return utilisateur
