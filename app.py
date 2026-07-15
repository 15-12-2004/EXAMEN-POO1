import tkinter as tk
from tkinter import ttk, messagebox

from services.clinic_manager import ClinicManager
from exceptions.custom_exceptions import (
    ValidationError,
    NotFoundError,
    AppointmentConflictError,
    DatabaseError,
    BillingError
)


class ClinicApp(tk.Tk):
    """
    Interface principale de l'application de gestion de clinique médicale.
    L'application contient plusieurs onglets (vues) :
    - Patients
    - Médecins
    - Rendez-vous
    - Dossiers médicaux
    - Facturation
    """

    def __init__(self):
        super().__init__()

        self.title("Système de Gestion de Clinique Médicale")
        self.geometry("1200x700")
        self.resizable(True, True)

        # Manager principal qui contient toute la logique métier
        self.manager = ClinicManager()

        # Notebook = système d'onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Création des vues
        self.patient_frame = ttk.Frame(self.notebook)
        self.doctor_frame = ttk.Frame(self.notebook)
        self.appointment_frame = ttk.Frame(self.notebook)
        self.record_frame = ttk.Frame(self.notebook)
        self.invoice_frame = ttk.Frame(self.notebook)

        # Ajout des onglets
        self.notebook.add(self.patient_frame, text="Patients")
        self.notebook.add(self.doctor_frame, text="Médecins")
        self.notebook.add(self.appointment_frame, text="Rendez-vous")
        self.notebook.add(self.record_frame, text="Dossiers Médicaux")
        self.notebook.add(self.invoice_frame, text="Facturation")

        # Construire chaque vue
        self.build_patient_view()
        self.build_doctor_view()
        self.build_appointment_view()
        self.build_record_view()
        self.build_invoice_view()

        # Chargement initial des données dans les tableaux
        self.refresh_patients()
        self.refresh_doctors()
        self.refresh_appointments()
        self.refresh_records()
        self.refresh_invoices()

        # Gestion de fermeture
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ============================================================
    # OUTILS GENERAUX
    # ============================================================

    def clear_tree(self, tree):
        """Supprime toutes les lignes d'un Treeview."""
        for item in tree.get_children():
            tree.delete(item)

    def on_close(self):
        """Ferme proprement l'application et la connexion à la base."""
        try:
            self.manager.close()
        except Exception:
            pass
        self.destroy()

    # ============================================================
    # VUE PATIENTS
    # ============================================================

    def build_patient_view(self):
        """Construit la vue de gestion des patients."""
        form_frame = ttk.LabelFrame(self.patient_frame, text="Ajouter un patient")
        form_frame.pack(fill="x", padx=10, pady=10)

        # Champs du formulaire patient
        ttk.Label(form_frame, text="ID Patient").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.patient_id_entry = ttk.Entry(form_frame)
        self.patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Prénom").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.patient_first_name_entry = ttk.Entry(form_frame)
        self.patient_first_name_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Nom").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.patient_last_name_entry = ttk.Entry(form_frame)
        self.patient_last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Téléphone").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.patient_phone_entry = ttk.Entry(form_frame)
        self.patient_phone_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Âge").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.patient_age_entry = ttk.Entry(form_frame)
        self.patient_age_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Sexe").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.patient_gender_combo = ttk.Combobox(
            form_frame,
            values=["Masculin", "Féminin", "Autre"],
            state="readonly"
        )
        self.patient_gender_combo.grid(row=2, column=3, padx=5, pady=5)
        self.patient_gender_combo.set("Masculin")

        ttk.Label(form_frame, text="Adresse").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.patient_address_entry = ttk.Entry(form_frame, width=40)
        self.patient_address_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky="we")

        ttk.Label(form_frame, text="Groupe sanguin").grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.patient_blood_entry = ttk.Entry(form_frame)
        self.patient_blood_entry.grid(row=3, column=4, padx=5, pady=5)

        ttk.Button(
            form_frame,
            text="Ajouter le patient",
            command=self.add_patient
        ).grid(row=4, column=0, columnspan=5, padx=5, pady=10)

        # Zone de recherche
        search_frame = ttk.LabelFrame(self.patient_frame, text="Recherche patient")
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Nom / Prénom").pack(side="left", padx=5, pady=5)
        self.patient_search_entry = ttk.Entry(search_frame, width=30)
        self.patient_search_entry.pack(side="left", padx=5, pady=5)

        ttk.Button(
            search_frame,
            text="Rechercher",
            command=self.search_patient
        ).pack(side="left", padx=5, pady=5)

        ttk.Button(
            search_frame,
            text="Réinitialiser",
            command=self.refresh_patients
        ).pack(side="left", padx=5, pady=5)

        # Tableau des patients
        table_frame = ttk.LabelFrame(self.patient_frame, text="Liste des patients")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "prenom", "nom", "telephone", "age", "sexe", "adresse", "groupe")
        self.patient_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        headings = [
            ("id", "ID"),
            ("prenom", "Prénom"),
            ("nom", "Nom"),
            ("telephone", "Téléphone"),
            ("age", "Âge"),
            ("sexe", "Sexe"),
            ("adresse", "Adresse"),
            ("groupe", "Groupe sanguin")
        ]

        for col, text in headings:
            self.patient_tree.heading(col, text=text)
            self.patient_tree.column(col, width=120)

        self.patient_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_patient(self):
        """Ajoute un patient via l'interface."""
        try:
            patient = self.manager.register_patient(
                person_id=self.patient_id_entry.get(),
                first_name=self.patient_first_name_entry.get(),
                last_name=self.patient_last_name_entry.get(),
                phone=self.patient_phone_entry.get(),
                age=self.patient_age_entry.get(),
                gender=self.patient_gender_combo.get(),
                address=self.patient_address_entry.get(),
                blood_group=self.patient_blood_entry.get() or "Non renseigné"
            )
        except (ValidationError, DatabaseError) as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")
        else:
            messagebox.showinfo("Succès", f"Patient {patient.full_name()} ajouté avec succès.")
            self.refresh_patients()

            # Vider les champs
            self.patient_id_entry.delete(0, tk.END)
            self.patient_first_name_entry.delete(0, tk.END)
            self.patient_last_name_entry.delete(0, tk.END)
            self.patient_phone_entry.delete(0, tk.END)
            self.patient_age_entry.delete(0, tk.END)
            self.patient_address_entry.delete(0, tk.END)
            self.patient_blood_entry.delete(0, tk.END)
            self.patient_gender_combo.set("Masculin")

    def refresh_patients(self):
        """Recharge la liste complète des patients dans le tableau."""
        try:
            patients = self.manager.get_all_patients()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.patient_tree)

        for patient in patients:
            self.patient_tree.insert("", tk.END, values=patient)

    def search_patient(self):
        """Recherche un patient par nom ou prénom."""
        keyword = self.patient_search_entry.get().strip()
        if not keyword:
            self.refresh_patients()
            return

        try:
            results = self.manager.search_patients_by_name(keyword)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.patient_tree)
        for patient in results:
            self.patient_tree.insert("", tk.END, values=patient)

    # ============================================================
    # VUE MEDECINS
    # ============================================================

    def build_doctor_view(self):
        """Construit la vue de gestion des médecins."""
        form_frame = ttk.LabelFrame(self.doctor_frame, text="Ajouter un médecin")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Person ID").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.doctor_person_id_entry = ttk.Entry(form_frame)
        self.doctor_person_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Prénom").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.doctor_first_name_entry = ttk.Entry(form_frame)
        self.doctor_first_name_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Nom").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.doctor_last_name_entry = ttk.Entry(form_frame)
        self.doctor_last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Téléphone").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.doctor_phone_entry = ttk.Entry(form_frame)
        self.doctor_phone_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Employee ID").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.doctor_employee_id_entry = ttk.Entry(form_frame)
        self.doctor_employee_id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Salaire").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.doctor_salary_entry = ttk.Entry(form_frame)
        self.doctor_salary_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Spécialité").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.doctor_specialty_entry = ttk.Entry(form_frame, width=30)
        self.doctor_specialty_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky="we")

        ttk.Button(
            form_frame,
            text="Ajouter le médecin",
            command=self.add_doctor
        ).grid(row=4, column=0, columnspan=4, padx=5, pady=10)

        # Recherche
        search_frame = ttk.LabelFrame(self.doctor_frame, text="Recherche médecin")
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Spécialité").pack(side="left", padx=5, pady=5)
        self.doctor_search_entry = ttk.Entry(search_frame, width=30)
        self.doctor_search_entry.pack(side="left", padx=5, pady=5)

        ttk.Button(
            search_frame,
            text="Rechercher",
            command=self.search_doctor
        ).pack(side="left", padx=5, pady=5)

        ttk.Button(
            search_frame,
            text="Réinitialiser",
            command=self.refresh_doctors
        ).pack(side="left", padx=5, pady=5)

        # Tableau
        table_frame = ttk.LabelFrame(self.doctor_frame, text="Liste des médecins")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("person_id", "prenom", "nom", "telephone", "employee_id", "salaire", "specialite")
        self.doctor_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        headings = [
            ("person_id", "Person ID"),
            ("prenom", "Prénom"),
            ("nom", "Nom"),
            ("telephone", "Téléphone"),
            ("employee_id", "Employee ID"),
            ("salaire", "Salaire"),
            ("specialite", "Spécialité")
        ]

        for col, text in headings:
            self.doctor_tree.heading(col, text=text)
            self.doctor_tree.column(col, width=140)

        self.doctor_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_doctor(self):
        """Ajoute un médecin via l'interface."""
        try:
            doctor = self.manager.register_doctor(
                person_id=self.doctor_person_id_entry.get(),
                first_name=self.doctor_first_name_entry.get(),
                last_name=self.doctor_last_name_entry.get(),
                phone=self.doctor_phone_entry.get(),
                employee_id=self.doctor_employee_id_entry.get(),
                salary=self.doctor_salary_entry.get(),
                specialty=self.doctor_specialty_entry.get()
            )
        except (ValidationError, DatabaseError) as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")
        else:
            messagebox.showinfo("Succès", f"Médecin {doctor.full_name()} ajouté avec succès.")
            self.refresh_doctors()

            self.doctor_person_id_entry.delete(0, tk.END)
            self.doctor_first_name_entry.delete(0, tk.END)
            self.doctor_last_name_entry.delete(0, tk.END)
            self.doctor_phone_entry.delete(0, tk.END)
            self.doctor_employee_id_entry.delete(0, tk.END)
            self.doctor_salary_entry.delete(0, tk.END)
            self.doctor_specialty_entry.delete(0, tk.END)

    def refresh_doctors(self):
        """Recharge la liste complète des médecins."""
        try:
            doctors = self.manager.get_all_doctors()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.doctor_tree)

        for doctor in doctors:
            self.doctor_tree.insert("", tk.END, values=doctor)

    def search_doctor(self):
        """Recherche un médecin par spécialité."""
        specialty = self.doctor_search_entry.get().strip()
        if not specialty:
            self.refresh_doctors()
            return

        try:
            results = self.manager.search_doctors_by_specialty(specialty)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.doctor_tree)
        for doctor in results:
            self.doctor_tree.insert("", tk.END, values=doctor)

    # ============================================================
    # VUE RENDEZ-VOUS
    # ===========================================================

    def build_appointment_view(self):
        """Construit la vue de gestion des rendez-vous."""
        form_frame = ttk.LabelFrame(self.appointment_frame, text="Programmer un rendez-vous")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="ID RDV").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.appointment_id_entry = ttk.Entry(form_frame)
        self.appointment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Patient").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.appointment_patient_id_entry = ttk.Entry(form_frame)
        self.appointment_patient_id_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Médecin").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.appointment_doctor_id_entry = ttk.Entry(form_frame)
        self.appointment_doctor_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Date (YYYY-MM-DD)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.appointment_date_entry = ttk.Entry(form_frame)
        self.appointment_date_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Heure (HH:MM)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.appointment_time_entry = ttk.Entry(form_frame)
        self.appointment_time_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Motif").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.appointment_reason_entry = ttk.Entry(form_frame, width=30)
        self.appointment_reason_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Button(
            form_frame,
            text="Programmer le rendez-vous",
            command=self.add_appointment
        ).grid(row=3, column=0, columnspan=4, padx=5, pady=10)

        # Tableau
        table_frame = ttk.LabelFrame(self.appointment_frame, text="Liste des rendez-vous")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("appointment_id", "patient_id", "doctor_id", "date", "time", "reason", "status")
        self.appointment_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        headings = [
            ("appointment_id", "ID RDV"),
            ("patient_id", "ID Patient"),
            ("doctor_id", "ID Médecin"),
            ("date", "Date"),
            ("time", "Heure"),
            ("reason", "Motif"),
            ("status", "Statut")
        ]

        for col, text in headings:
            self.appointment_tree.heading(col, text=text)
            self.appointment_tree.column(col, width=150)

        self.appointment_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_appointment(self):
        """Ajoute un rendez-vous via l'interface."""
        try:
            appointment = self.manager.schedule_appointment(
                appointment_id=self.appointment_id_entry.get(),
                patient_id=self.appointment_patient_id_entry.get(),
                doctor_id=self.appointment_doctor_id_entry.get(),
                appointment_date=self.appointment_date_entry.get(),
                appointment_time=self.appointment_time_entry.get(),
                reason=self.appointment_reason_entry.get()
            )
        except (ValidationError, NotFoundError, AppointmentConflictError, DatabaseError) as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")
        else:
            messagebox.showinfo("Succès", f"Rendez-vous {appointment.appointment_id} programmé avec succès.")
            self.refresh_appointments()

            self.appointment_id_entry.delete(0, tk.END)
            self.appointment_patient_id_entry.delete(0, tk.END)
            self.appointment_doctor_id_entry.delete(0, tk.END)
            self.appointment_date_entry.delete(0, tk.END)
            self.appointment_time_entry.delete(0, tk.END)
            self.appointment_reason_entry.delete(0, tk.END)

    def refresh_appointments(self):
        """Recharge la liste des rendez-vous."""
        try:
            appointments = self.manager.get_all_appointments()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.appointment_tree)

        for appointment in appointments:
            self.appointment_tree.insert("", tk.END, values=appointment)

    # ============================================================
    # VUE DOSSIERS MEDICAUX
    # ============================================================

    def build_record_view(self):
        """Construit la vue des dossiers médicaux."""
        form_frame = ttk.LabelFrame(self.record_frame, text="Ajouter un dossier médical")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="ID Dossier").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.record_id_entry = ttk.Entry(form_frame)
        self.record_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Patient").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.record_patient_id_entry = ttk.Entry(form_frame)
        self.record_patient_id_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Diagnostic").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.record_diagnosis_entry = ttk.Entry(form_frame, width=40)
        self.record_diagnosis_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="we")

        ttk.Label(form_frame, text="Traitement").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.record_treatment_entry = ttk.Entry(form_frame, width=40)
        self.record_treatment_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="we")

        ttk.Label(form_frame, text="Notes").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.record_notes_entry = ttk.Entry(form_frame, width=40)
        self.record_notes_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=3, sticky="we")

        ttk.Button(
            form_frame,
            text="Ajouter le dossier",
            command=self.add_record
        ).grid(row=4, column=0, columnspan=4, padx=5, pady=10)

        # Tableau
        table_frame = ttk.LabelFrame(self.record_frame, text="Liste des dossiers médicaux")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("record_id", "patient_id", "diagnosis", "treatment", "notes", "created_at")
        self.record_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        headings = [
            ("record_id", "ID Dossier"),
            ("patient_id", "ID Patient"),
            ("diagnosis", "Diagnostic"),
            ("treatment", "Traitement"),
            ("notes", "Notes"),
            ("created_at", "Date création")
        ]

        for col, text in headings:
            self.record_tree.heading(col, text=text)
            self.record_tree.column(col, width=180)

        self.record_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_record(self):
        """Ajoute un dossier médical via l'interface."""
        try:
            record, notification = self.manager.add_medical_record(
                record_id=self.record_id_entry.get(),
                patient_id=self.record_patient_id_entry.get(),
                diagnosis=self.record_diagnosis_entry.get(),
                treatment=self.record_treatment_entry.get(),
                notes=self.record_notes_entry.get()
            )
        except (ValidationError, NotFoundError, DatabaseError) as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")
        else:
            messagebox.showinfo(
                "Succès",
                f"Dossier {record.record_id} ajouté avec succès.\n\n{notification}"
            )
            self.refresh_records()

            self.record_id_entry.delete(0, tk.END)
            self.record_patient_id_entry.delete(0, tk.END)
            self.record_diagnosis_entry.delete(0, tk.END)
            self.record_treatment_entry.delete(0, tk.END)
            self.record_notes_entry.delete(0, tk.END)

    def refresh_records(self):
        """Recharge la liste des dossiers médicaux."""
        try:
            records = self.manager.get_all_medical_records()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.record_tree)

        for record in records:
            self.record_tree.insert("", tk.END, values=record)

    # ============================================================
    # VUE FACTURATION
    # ============================================================

    def build_invoice_view(self):
        """Construit la vue de facturation."""
        form_frame = ttk.LabelFrame(self.invoice_frame, text="Créer une facture")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="ID Facture").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.invoice_id_entry = ttk.Entry(form_frame)
        self.invoice_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Patient").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.invoice_patient_id_entry = ttk.Entry(form_frame)
        self.invoice_patient_id_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Montant de base").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.invoice_amount_entry = ttk.Entry(form_frame)
        self.invoice_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Type").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.invoice_type_combo = ttk.Combobox(
            form_frame,
            values=["normal", "insurance", "emergency"],
            state="readonly"
        )
        self.invoice_type_combo.grid(row=1, column=3, padx=5, pady=5)
        self.invoice_type_combo.set("normal")

        ttk.Button(
            form_frame,
            text="Créer la facture",
            command=self.add_invoice
        ).grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        # Tableau
        table_frame = ttk.LabelFrame(self.invoice_frame, text="Liste des factures")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("invoice_id", "patient_id", "amount", "status", "created_at")
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        headings = [
            ("invoice_id", "ID Facture"),
            ("patient_id", "ID Patient"),
            ("amount", "Montant"),
            ("status", "Statut"),
            ("created_at", "Date création")
        ]

        for col, text in headings:
            self.invoice_tree.heading(col, text=text)
            self.invoice_tree.column(col, width=180)

        self.invoice_tree.pack(fill="both", expand=True, padx=5, pady=5)

    def add_invoice(self):
        """Crée une facture via l'interface."""
        try:
            invoice, notification = self.manager.create_invoice(
                invoice_id=self.invoice_id_entry.get(),
                patient_id=self.invoice_patient_id_entry.get(),
                base_amount=self.invoice_amount_entry.get(),
                invoice_type=self.invoice_type_combo.get()
            )
        except (NotFoundError, BillingError, DatabaseError) as e:
            messagebox.showerror("Erreur", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue : {e}")
        else:
            messagebox.showinfo(
                "Succès",
                f"Facture {invoice.invoice_id} créée avec succès.\n\n{notification}"
            )
            self.refresh_invoices()

            self.invoice_id_entry.delete(0, tk.END)
            self.invoice_patient_id_entry.delete(0, tk.END)
            self.invoice_amount_entry.delete(0, tk.END)
            self.invoice_type_combo.set("normal")

    def refresh_invoices(self):
        """Recharge la liste des factures."""
        try:
            invoices = self.manager.get_all_invoices()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.clear_tree(self.invoice_tree)

        for invoice in invoices:
            self.invoice_tree.insert("", tk.END, values=invoice) 