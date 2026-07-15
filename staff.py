from models.person import Person
from exceptions.custom_exceptions import ValidationError


class Staff(Person):
    """
    Représente un membre du personnel.
    Hérite de Person.
    """

    def __init__(self, person_id, first_name, last_name, phone, employee_id, salary):
        super().__init__(person_id, first_name, last_name, phone)
        self.employee_id = employee_id
        self.salary = salary

    # ============================================================
    # employee_id
    # ============================================================
    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("L'identifiant employé ne peut pas être vide.")

        self._employee_id = value

    # ============================================================
    # salary
    # ============================================================
    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("Le salaire ne peut pas être vide.")

        try:
            salary_float = float(value)
        except ValueError:
            raise ValidationError("Le salaire doit être un nombre valide.")

        if salary_float <= 0:
            raise ValidationError("Le salaire doit être supérieur à 0.")

        self._salary = salary_float

    def get_role(self):
        return "Personnel"

    # ============================================================
    # Implémentation de display_info()
    # imposée par la classe abstraite Person
    # ============================================================

    def display_info(self):
        """
        Affiche les informations du personnel.
        """

        return (
            f"Personnel : {self.full_name()}\n"
            f"Matricule : {self.employee_id}\n"
            f"Salaire : {self.salary}"
        )