from datetime import datetime
from exceptions.custom_exceptions import ValidationError


class Appointment:
    """
    Représente un rendez-vous entre un patient et un médecin.
    """

    def __init__(self, appointment_id, patient_id, doctor_id, appointment_date, appointment_time, reason, status="Programmé"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status

    # ============================================================
    # appointment_id
    # ============================================================
    @property
    def appointment_id(self):
        return self._appointment_id

    @appointment_id.setter
    def appointment_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant du rendez-vous ne peut pas être vide.")
        self._appointment_id = value

    # ============================================================
    # patient_id
    # ============================================================
    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant du patient ne peut pas être vide.")
        self._patient_id = value

    # ============================================================
    # doctor_id
    # ============================================================
    @property
    def doctor_id(self):
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant du médecin ne peut pas être vide.")
        self._doctor_id = value

    # ============================================================
    # appointment_date
    # ============================================================
    @property
    def appointment_date(self):
        return self._appointment_date

    @appointment_date.setter
    def appointment_date(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("La date du rendez-vous ne peut pas être vide.")

        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("La date doit être au format YYYY-MM-DD.")

        self._appointment_date = value

    # ============================================================
    # appointment_time
    # ============================================================
    @property
    def appointment_time(self):
        return self._appointment_time

    @appointment_time.setter
    def appointment_time(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("L'heure du rendez-vous ne peut pas être vide.")

        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            raise ValidationError("L'heure doit être au format HH:MM.")

        self._appointment_time = value

    # ============================================================
    # reason
    # ============================================================
    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, value):
        value = str(value).strip()

        if not value:
            raise ValidationError("Le motif du rendez-vous ne peut pas être vide.")

        if len(value) < 3:
            raise ValidationError("Le motif du rendez-vous est trop court.")

        self._reason = value

    # ============================================================
    # status
    # ============================================================
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        value = str(value).strip()

        allowed = ["Programmé", "Terminé", "Annulé"]
        if value not in allowed:
            raise ValidationError("Le statut du rendez-vous est invalide.")

        self._status = value