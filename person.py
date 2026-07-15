import re
from abc import ABC, abstractmethod
from exceptions.custom_exceptions import ValidationError


class Person(ABC):
    """
    Classe abstraite représentant une personne dans la clinique.
    Sert de base pour Patient et Staff.
    """

    def __init__(self, person_id, first_name, last_name, phone):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    # ============================================================
    # person_id
    # ============================================================
    @property
    def person_id(self):
        return self._person_id

    @person_id.setter
    def person_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant ne peut pas être vide.")
        self._person_id = value

    # ============================================================
    # first_name
    # ============================================================
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("Le prénom ne peut pas être vide.")

        # Autorise lettres, espaces et tirets
        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s\-]+", value):
            raise ValidationError(
                "Le prénom ne doit contenir que des lettres, espaces ou tirets."
            )

        # Empêcher un prénom fait uniquement d'espaces après strip
        if len(value) < 2:
            raise ValidationError("Le prénom doit contenir au moins 2 caractères.")

        self._first_name = value

    # ============================================================
    # last_name
    # ============================================================
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("Le nom ne peut pas être vide.")

        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s\-]+", value):
            raise ValidationError(
                "Le nom ne doit contenir que des lettres, espaces ou tirets."
            )

        if len(value) < 2:
            raise ValidationError("Le nom doit contenir au moins 2 caractères.")

        self._last_name = value

    # ============================================================
    # phone
    # ============================================================
    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("Le numéro de téléphone ne peut pas être vide.")

        # Supprimer les espaces internes si l'utilisateur tape "099 123 4567"
        normalized = value.replace(" ", "")

        # Autoriser uniquement les chiffres
        if not normalized.isdigit():
            raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")

        # Longueur minimale et maximale raisonnable
        if len(normalized) < 9 or len(normalized) > 15:
            raise ValidationError("Le numéro de téléphone doit contenir entre 9 et 15 chiffres.")

        self._phone = normalized

    # ============================================================
    # Méthodes utiles
    # ============================================================
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @abstractmethod
    def get_role(self):
        """
        Retourne le rôle de la personne dans le système.
        """
        pass

    @abstractmethod
    def display_info(self):
        """
        Affiche les informations principales.

        Chaque classe fille doit fournir
        sa propre manière d'afficher ses données.
        """
        pass