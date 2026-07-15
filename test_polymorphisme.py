"""
Test du polymorphisme et du duck typing.

Ce fichier montre que plusieurs objets différents
peuvent utiliser la même interface.
"""


import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from models.patient import Patient
from models.doctor import Doctor


def show_information(person):
    """
    Exemple de duck typing.

    La fonction ne vérifie pas le type de l'objet.
    Elle vérifie seulement que l'objet possède
    la méthode display_info().
    """

    print(person.display_info())
    print(person.get_role())
    print("------------------------")


def main():

    # Création d'un patient
    patient = Patient(
        person_id="P001",
        first_name="Jean",
        last_name="Kabila",
        phone="099999999",
        age=30,
        gender="Masculin",
        address="Lubumbashi",
        blood_group="O+"
    )


    # Création d'un médecin
    doctor = Doctor(
        person_id="D001",
        first_name="Paul",
        last_name="Mukendi",
        phone="098888888",
        employee_id="EMP001",
        salary=2500,
        specialty="Cardiologie"
    )


    # Même fonction utilisée pour deux objets différents
    show_information(patient)
    show_information(doctor)


if __name__ == "__main__":
    main()