from datetime import datetime
from exceptions.custom_exceptions import ValidationError


class Invoice:
    """
    Représente une facture associée à un patient.
    """

    def __init__(self, invoice_id, patient_id, amount, status="Non payée"):
        self.invoice_id = invoice_id
        self.patient_id = patient_id
        self.amount = amount
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def invoice_id(self):
        return self._invoice_id

    @invoice_id.setter
    def invoice_id(self, value):
        value = str(value).strip()
        if not value:
            raise ValidationError("L'identifiant de la facture ne peut pas être vide.")
        self._invoice_id = value

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
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        try:
            amount_float = float(value)
        except ValueError:
            raise ValidationError("Le montant de la facture doit être un nombre valide.")

        if amount_float <= 0:
            raise ValidationError("Le montant de la facture doit être supérieur à 0.")

        self._amount = round(amount_float, 2)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        value = str(value).strip()

        allowed = ["Payée", "Non payée", "Partiellement payée"]
        if value not in allowed:
            raise ValidationError("Le statut de la facture est invalide.")

        self._status = value