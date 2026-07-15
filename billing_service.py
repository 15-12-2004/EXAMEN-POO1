from patterns.strategy import (
    NormalBillingStrategy,
    InsuranceBillingStrategy,
    EmergencyBillingStrategy
)
from models.invoice import Invoice
from exceptions.custom_exceptions import BillingError


class BillingService:
    """
    Service de facturation.
    Il applique une stratégie de calcul selon le type de facture.
    """

    def __init__(self):
        self._strategies = {
            "normal": NormalBillingStrategy(),
            "insurance": InsuranceBillingStrategy(),
            "emergency": EmergencyBillingStrategy()
        }

    def create_invoice(self, invoice_id, patient_id, base_amount, invoice_type="normal"):
        """
        Crée une facture en appliquant une stratégie de calcul.
        """
        try:
            invoice_type = str(invoice_type).strip().lower()

            if invoice_type not in self._strategies:
                raise BillingError("Type de facturation inconnu.")

            strategy = self._strategies[invoice_type]
            final_amount = strategy.calculate_amount(base_amount)

            invoice = Invoice(
                invoice_id=invoice_id,
                patient_id=patient_id,
                amount=final_amount,
                status="Non payée"
            )

        except BillingError:
            raise
        except Exception as e:
            raise BillingError(f"Erreur lors de la création de la facture : {e}")
        else:
            return invoice