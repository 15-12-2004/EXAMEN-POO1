class NotificationService:
    """
    Service de notifications.
    Pour ce projet, on simule les notifications par des messages texte.
    On peut imaginer plus tard l'envoi de SMS, email, WhatsApp, etc.
    """

    def send_appointment_confirmation(self, patient_name, doctor_name, appointment_date, appointment_time):
        """
        Génère un message de confirmation de rendez-vous.
        """
        return (
            f"Rendez-vous confirmé pour {patient_name} avec Dr {doctor_name} "
            f"le {appointment_date} à {appointment_time}."
        )

    def send_invoice_notification(self, patient_name, amount):
        """
        Génère un message lié à une facture.
        """
        return (
            f"Bonjour {patient_name}, une facture de {amount} USD a été générée à votre nom."
        )

    def send_medical_record_notification(self, patient_name):
        """
        Génère un message informant qu'un dossier médical a été ajouté.
        """
        return (
            f"Le dossier médical du patient {patient_name} a été enregistré avec succès."
        )