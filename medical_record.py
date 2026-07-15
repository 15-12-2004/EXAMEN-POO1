from datetime import datetime
from exceptions.custom_exceptions import ValidationError


class MedicalRecord:
    """
    Représente un dossier médical associé à un patient.
    """

    def __init__(self, record_id, patient_id, diagnosis, treatment, notes=""):
        self.record_id = record_id
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.notes = notes
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def record_id(self):
        return self._record_id

    @record_id.setter
    def record_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant du dossier médical ne peut pas être vide.")
        self._record_id = value

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant du patient ne peut pas être vide.")
        self._patient_id = value

    @property
    def diagnosis(self):
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("Le diagnostic ne peut pas être vide.")
        if len(value) < 3:
            raise ValidationError("Le diagnostic est trop court.")
        self._diagnosis = value

    @property
    def treatment(self):
        return self._treatment

    @treatment.setter
    def treatment(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("Le traitement ne peut pas être vide.")
        if len(value) < 3:
            raise ValidationError("Le traitement est trop court.")
        self._treatment = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        value = str(value).strip()
        self._notes = value