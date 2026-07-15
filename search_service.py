class SearchService:
    """
    Service de recherche dans les listes récupérées depuis la base.
    Ce service permet d'effectuer des recherches simples sur les patients et médecins.
    """

    @staticmethod
    def search_patients_by_name(patients, keyword):
        """
        Recherche des patients par mot-clé dans le prénom ou le nom.

        patients : liste de tuples provenant de la base
        keyword : texte à rechercher
        """
        keyword = keyword.lower().strip()
        results = []

        for patient in patients:
            # patient = (id, first_name, last_name, phone, age, gender, address, blood_group)
            first_name = patient[1].lower()
            last_name = patient[2].lower()

            if keyword in first_name or keyword in last_name:
                results.append(patient)

        return results

    @staticmethod
    def search_doctors_by_specialty(doctors, specialty):
        """
        Recherche des médecins par spécialité.

        doctors : liste de tuples provenant de la base
        specialty : spécialité à rechercher
        """
        specialty = specialty.lower().strip()
        results = []

        for doctor in doctors:
            # doctor = (person_id, first_name, last_name, phone, employee_id, salary, specialty)
            doctor_specialty = doctor[6].lower()

            if specialty in doctor_specialty:
                results.append(doctor)

        return results