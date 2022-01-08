import hashlib
import re


def est_une_adresse_email_valide(email):
    """
    Fonction permettant de vérifier si l'adresse email passée en entrée
    est valide.

    Args:
        email (str): Adresse email à valider.

    Returns:
        bool: True si l'adresse email passée en argument est valide, False sinon.
    """
    # https://www.c-sharpcorner.com/article/how-to-validate-an-email-address-in-python/
    return bool(re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email))


class HacheurDeMotDePasse:
    """
    Classe rajoutant une couche de sécurité à notre application
    en permettant le hachage et la vérification de mot de passe.

    Si vous êtes curieux, vous pouvez jeter un coup d'oeil sur
    https://fr.wikipedia.org/wiki/Fonction_de_hachage 
    afin d'en apprendre davantage sur l'utilité du hachage de mot de passe.
    """
    SEL_CRYPTO = "7f99fb781a504bb69b12fc4b58ce3414"

    @classmethod
    def hacher(cls, mot_de_passe_en_clair):
        """
        Méthode permettant de hacher un mot de passe.

        Args:
            mot_de_passe_en_clair (str): Mot de passe en clair à hacher.

        Returns:
            str: Mot de passe haché 
        """
        return hashlib.sha512(mot_de_passe_en_clair.encode("utf-8") + cls.SEL_CRYPTO.encode("utf-8")).hexdigest()

    @classmethod
    def verifier(cls, hash_mot_de_passe, mot_de_passe_en_clair):
        """
        Méthode permettant de vérifier que le hachage fourni correspond 
        bien au mot de passe fourni.

        Args:
            hash_mot_de_passe (str): Version hachée du mot de passe.
            mot_de_passe_en_clair (str): Mot de passe en clair.

        Returns:
            bool: True si le mot de passe est valide, False sinon. 
        """
        return cls.hacher(mot_de_passe_en_clair) == hash_mot_de_passe
