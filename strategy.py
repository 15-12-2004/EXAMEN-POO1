from abc import ABC, abstractmethod


class BillingStrategy(ABC):
    """
    Classe abstraite pour les stratégies de facturation.
    Chaque stratégie doit définir sa propre manière
    de calculer le montant final d'une facture.
    """

    @abstractmethod
    def calculate_amount(self, base_amount):
        """
        Calcule et retourne le montant final à payer.
        """
        pass


class NormalBillingStrategy(BillingStrategy):
    """
    Facturation normale :
    le patient paie simplement le montant de base.
    """

    def calculate_amount(self, base_amount):
        return float(base_amount)


class InsuranceBillingStrategy(BillingStrategy):
    """
    Facturation avec assurance :
    l'assurance couvre une partie du montant.
    Ici, on suppose que le patient paie 30% du montant total.
    """

    def calculate_amount(self, base_amount):
        return float(base_amount) * 0.30


class EmergencyBillingStrategy(BillingStrategy):
    """
    Facturation d'urgence :
    on applique une majoration de 20%.
    """

    def calculate_amount(self, base_amount):
        return float(base_amount) * 1.20