from patterns.factory import ClinicFactory
from persistence.data_manager import DataManager
from services.billing_service import BillingService
from services.notification_service import NotificationService
from services.search_service import SearchService
from exceptions.custom_exceptions import (
    ValidationError,
    NotFoundError,
    AppointmentConflictError,
    DatabaseError,
    BillingError
)


class ClinicManager:
    """
    Classe centrale de l'application.
    Elle relie :
    - les modèles via la Factory
    - la base SQLite via DataManager
    - la facturation via BillingService
    - les notifications via NotificationService
    - la recherche via SearchService
    """

    def __init__(self):
        self.data_manager = DataManager()
        self.billing_service = BillingService()
        self.notification_service = NotificationService()
        self.search_service = SearchService()

    # ============================================================
    # GESTION DES PATIENTS
    # ============================================================

    def register_patient(self, person_id, first_name, last_name, phone, age, gender, address, blood_group="Non renseigné"):
        """
        Crée un patient puis l'enregistre en base.
        """
        try:
            patient = ClinicFactory.create_patient(
                person_id=person_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                age=age,
                gender=gender,
                address=address,
                blood_group=blood_group
            )
            self.data_manager.add_patient(patient)

        except ValidationError:
            raise
        except DatabaseError:
            raise
        except Exception as e:
            raise Exception(f"Erreur lors de l'enregistrement du patient : {e}")
        else:
            return patient

    def get_all_patients(self):
        """
        Retourne tous les patients.
        """
        return self.data_manager.get_all_patients()

    def get_patient_by_id(self, patient_id):
        """
        Retourne un patient selon son identifiant.
        """
        return self.data_manager.get_patient_by_id(patient_id)

    # ============================================================
    # GESTION DES MEDECINS
    # ============================================================

    def register_doctor(self, person_id, first_name, last_name, phone, employee_id, salary, specialty):
        """
        Crée un médecin puis l'enregistre en base.
        """
        try:
            doctor = ClinicFactory.create_doctor(
                person_id=person_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                employee_id=employee_id,
                salary=salary,
                specialty=specialty
            )
            self.data_manager.add_doctor(doctor)

        except ValidationError:
            raise
        except DatabaseError:
            raise
        except Exception as e:
            raise Exception(f"Erreur lors de l'enregistrement du médecin : {e}")
        else:
            return doctor

    def get_all_doctors(self):
        """
        Retourne tous les médecins.
        """
        return self.data_manager.get_all_doctors()

    def get_doctor_by_id(self, doctor_id):
        """
        Retourne un médecin selon son identifiant.
        """
        return self.data_manager.get_doctor_by_id(doctor_id)

    # ============================================================
    # GESTION DES RENDEZ-VOUS
    # ============================================================

    def _check_appointment_conflict(self, doctor_id, appointment_date, appointment_time):
        """
        Vérifie si un médecin a déjà un rendez-vous à la même date et à la même heure.
        """
        appointments = self.data_manager.get_all_appointments()

        for appointment in appointments:
            # appointment = (
            #   appointment_id, patient_id, doctor_id, appointment_date,
            #   appointment_time, reason, status
            # )
            existing_doctor_id = appointment[2]
            existing_date = appointment[3]
            existing_time = appointment[4]
            existing_status = appointment[6]

            if (
                existing_doctor_id == doctor_id
                and existing_date == appointment_date
                and existing_time == appointment_time
                and existing_status != "Annulé"
            ):
                raise AppointmentConflictError(
                    "Ce médecin a déjà un rendez-vous à cette date et cette heure."
                )

    def schedule_appointment(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason,
        status="Programmé"
    ):
        """
        Programme un rendez-vous après vérification :
        - patient existant
        - médecin existant
        - absence de conflit horaire
        """
        try:
            # Vérifier que le patient existe
            self.data_manager.get_patient_by_id(patient_id)

            # Vérifier que le médecin existe
            self.data_manager.get_doctor_by_id(doctor_id)

            # Vérifier les conflits de rendez-vous
            self._check_appointment_conflict(doctor_id, appointment_date, appointment_time)

            # Créer l'objet rendez-vous
            appointment = ClinicFactory.create_appointment(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status=status
            )

            # Sauvegarder en base
            self.data_manager.add_appointment(appointment)

        except (ValidationError, NotFoundError, AppointmentConflictError, DatabaseError):
            raise
        except Exception as e:
            raise Exception(f"Erreur lors de la programmation du rendez-vous : {e}")
        else:
            return appointment

    def get_all_appointments(self):
        """
        Retourne tous les rendez-vous.
        """
        return self.data_manager.get_all_appointments()

    # ============================================================
    # DOSSIERS MEDICAUX
    # ============================================================

    def add_medical_record(self, record_id, patient_id, diagnosis, treatment, notes=""):
        """
        Ajoute un dossier médical à un patient.
        """
        try:
            # Vérifier que le patient existe
            patient = self.data_manager.get_patient_by_id(patient_id)

            record = ClinicFactory.create_medical_record(
                record_id=record_id,
                patient_id=patient_id,
                diagnosis=diagnosis,
                treatment=treatment,
                notes=notes
            )

            self.data_manager.add_medical_record(record)

            # Notification simulée
            patient_name = f"{patient[1]} {patient[2]}"
            notification = self.notification_service.send_medical_record_notification(patient_name)

        except (ValidationError, NotFoundError, DatabaseError):
            raise
        except Exception as e:
            raise Exception(f"Erreur lors de l'ajout du dossier médical : {e}")
        else:
            return record, notification

    def get_all_medical_records(self):
        """
        Retourne tous les dossiers médicaux.
        """
        return self.data_manager.get_all_medical_records()

    # ============================================================
    # FACTURATION
    # ============================================================

    def create_invoice(self, invoice_id, patient_id, base_amount, invoice_type="normal"):
        """
        Crée une facture pour un patient :
        - vérifie que le patient existe
        - applique une stratégie de facturation
        - enregistre la facture
        """
        try:
            patient = self.data_manager.get_patient_by_id(patient_id)

            invoice = self.billing_service.create_invoice(
                invoice_id=invoice_id,
                patient_id=patient_id,
                base_amount=base_amount,
                invoice_type=invoice_type
            )

            self.data_manager.add_invoice(invoice)

            patient_name = f"{patient[1]} {patient[2]}"
            notification = self.notification_service.send_invoice_notification(
                patient_name,
                invoice.amount
            )

        except (NotFoundError, BillingError, DatabaseError):
            raise
        except Exception as e:
            raise Exception(f"Erreur lors de la création de la facture : {e}")
        else:
            return invoice, notification

    def get_all_invoices(self):
        """
        Retourne toutes les factures.
        """
        return self.data_manager.get_all_invoices()

    # ============================================================
    # RECHERCHE
    # ============================================================

    def search_patients_by_name(self, keyword):
        """
        Recherche un patient par nom ou prénom.
        """
        patients = self.data_manager.get_all_patients()
        return self.search_service.search_patients_by_name(patients, keyword)

    def search_doctors_by_specialty(self, specialty):
        """
        Recherche un médecin par spécialité.
        """
        doctors = self.data_manager.get_all_doctors()
        return self.search_service.search_doctors_by_specialty(doctors, specialty)

    # ============================================================
    # FERMETURE
    # ============================================================

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.data_manager.close()