class ClinicError(Exception):
    """
    Exception de base du projet.
    Toutes les autres exceptions personnalisées héritent de cette classe.
    """
    pass


class ValidationError(ClinicError):
    """
    Erreur levée lorsqu'une donnée saisie par l'utilisateur est invalide.
    Exemple :
    - nom vide
    - téléphone avec lettres
    - âge négatif
    - date incorrecte
    """
    pass


class NotFoundError(ClinicError):
    """
    Erreur levée lorsqu'un élément recherché n'existe pas.
    Exemple :
    - patient introuvable
    - médecin introuvable
    """
    pass


class AppointmentConflictError(ClinicError):
    """
    Erreur levée lorsqu'un rendez-vous entre en conflit
    avec un autre rendez-vous existant.
    """
    pass


class DatabaseError(ClinicError):
    """
    Erreur levée lors d'un problème de base de données.
    """
    pass


class BillingError(ClinicError):
    """
    Erreur levée lors d'un problème de facturation.
    Exemple :
    - montant invalide
    - stratégie inconnue
    """
    pass