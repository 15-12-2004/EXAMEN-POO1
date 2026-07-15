from models.person import Person
from exceptions.custom_exceptions import ValidationError


class Patient(Person):
    """
    Représente un patient de la clinique.
    Hérite de Person.
    """

    def __init__(self, person_id, first_name, last_name, phone, age, gender, address, blood_group="Non renseigné"):
        super().__init__(person_id, first_name, last_name, phone)
        self.age = age
        self.gender = gender
        self.address = address
        self.blood_group = blood_group

    # ============================================================
    # age
    # ============================================================
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("L'âge ne peut pas être vide.")

        if not value.isdigit():
            raise ValidationError("L'âge doit être un nombre entier positif.")

        age_int = int(value)

        if age_int <= 0:
            raise ValidationError("L'âge doit être supérieur à 0.")

        if age_int > 120:
            raise ValidationError("L'âge saisi est invalide.")

        self._age = age_int

    # ============================================================
    # gender
    # ============================================================
    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        value = str(value).strip()

        allowed = ["Masculin", "Féminin", "Autre"]
        if value not in allowed:
            raise ValidationError("Le sexe doit être : Masculin, Féminin ou Autre.")

        self._gender = value

    # ============================================================
    # address
    # ============================================================
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("L'adresse ne peut pas être vide.")

        if len(value) < 4:
            raise ValidationError("L'adresse est trop courte.")

        self._address = value

    # ============================================================
    # blood_group
    # ============================================================
    @property
    def blood_group(self):
        return self._blood_group

    @blood_group.setter
    def blood_group(self, value):
        value = str(value).strip()

        allowed = [
            "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-",
            "Non renseigné"
        ]

        if not value:
            value = "Non renseigné"

        if value not in allowed:
            raise ValidationError(
                "Le groupe sanguin doit être parmi : A+, A-, B+, B-, AB+, AB-, O+, O-."
            )

        self._blood_group = value

    def get_role(self):
        return "Patient"
    
# ============================================================
    # Implémentation  de la méthode abstraite
    # venant de Person
# ============================================================

    def display_info(self):
        """
        Affiche les informations d'un patient.
        """

        return (
            f"Patient : {self.full_name()}\n"
            f"Age : {self.age}\n"
            f"Sexe : {self.gender}\n"
            f"Groupe sanguin : {self.blood_group}"
        )