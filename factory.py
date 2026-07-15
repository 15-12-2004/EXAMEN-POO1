from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord


class ClinicFactory:
    """
    Factory Pattern :
    cette classe centralise la création des objets métier
    de la clinique (Patient, Doctor, Appointment, MedicalRecord).
    """

    @staticmethod
    def create_patient(person_id, first_name, last_name, phone, age, gender, address, blood_group):
        """
        Crée et retourne un objet Patient.
        """
        return Patient(
            person_id=person_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            age=age,
            gender=gender,
            address=address,
            blood_group=blood_group
        )

    @staticmethod
    def create_doctor(person_id, first_name, last_name, phone, employee_id, salary, specialty):
        """
        Crée et retourne un objet Doctor.
        """
        return Doctor(
            person_id=person_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            employee_id=employee_id,
            salary=salary,
            specialty=specialty
        )

    @staticmethod
    def create_appointment(appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status="Programmé"):
        """
        Crée et retourne un objet Appointment.
        """
        return Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status=status
        )

    @staticmethod
    def create_medical_record(record_id, patient_id, diagnosis, treatment, notes=""):
        """
        Crée et retourne un objet MedicalRecord.
        """
        return MedicalRecord(
            record_id=record_id,
            patient_id=patient_id,
            diagnosis=diagnosis,
            treatment=treatment,
            notes=notes
        )