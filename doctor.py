from models.staff import Staff
from exceptions.custom_exceptions import ValidationError


class Doctor(Staff):
    """
    Représente un médecin de la clinique.
    Hérite de Staff.
    """

    def __init__(self, person_id, first_name, last_name, phone, employee_id, salary, specialty):
        super().__init__(person_id, first_name, last_name, phone, employee_id, salary)
        self.specialty = specialty

    @property
    def specialty(self):
        return self._specialty

    @specialty.setter
    def specialty(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("La spécialité du médecin ne peut pas être vide.")

        if len(value) < 3:
            raise ValidationError("La spécialité est trop courte.")

        self._specialty = value

    def get_role(self):
        return "Médecin"
    
    # ============================================================
    # Surcharge (override) de display_info()
    #
    # Doctor hérite de Staff mais propose
    # son propre affichage.
    # ============================================================


    def display_info(self):

        return (
            f"Médecin : {self.full_name()}\n"
            f"Spécialité : {self.specialty}\n"
            f"Salaire : {self.salary}"
        )