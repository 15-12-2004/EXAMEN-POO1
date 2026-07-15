import sqlite3
from datetime import datetime

from exceptions.custom_exceptions import DatabaseError, NotFoundError


class DataManager:
    """
    Gère la persistance des données avec SQLite.
    Cette classe centralise :
    - la connexion à la base
    - la création des tables
    - les insertions
    - les lectures
    - certaines suppressions/modifications si besoin
    """

    def __init__(self, db_name="clinique_medicale_poo.db"):
        self.db_name = db_name
        self.connection = None
        self.connect()
        self.create_tables()

    # ============================================================
    # CONNEXION ET INITIALISATION
    # ============================================================

    def connect(self):
        """
        Ouvre la connexion SQLite.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            raise DatabaseError(f"Impossible de se connecter à la base de données : {e}")

    def create_tables(self):
        """
        Crée toutes les tables nécessaires si elles n'existent pas déjà.
        """
        cursor = self.connection.cursor()

        try:
            # Table des patients
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    address TEXT NOT NULL,
                    blood_group TEXT
                )
            """)

            # Table des médecins
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    person_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    employee_id TEXT NOT NULL UNIQUE,
                    salary REAL NOT NULL,
                    specialty TEXT NOT NULL
                )
            """)

            # Table des rendez-vous
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    doctor_id TEXT NOT NULL,
                    appointment_date TEXT NOT NULL,
                    appointment_time TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(person_id)
                )
            """)

            # Table des dossiers médicaux
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    diagnosis TEXT NOT NULL,
                    treatment TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            """)

            # Table des factures
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            """)

        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Erreur lors de la création des tables : {e}")
        else:
            self.connection.commit()
        finally:
            cursor.close()

    # ============================================================
    # PATIENTS
    # ============================================================

    def add_patient(self, patient):
        """
        Ajoute un patient dans la base.
        patient doit être un objet Patient.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO patients (id, first_name, last_name, phone, age, gender, address, blood_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient.person_id,
                patient.first_name,
                patient.last_name,
                patient.phone,
                patient.age,
                patient.gender,
                patient.address,
                patient.blood_group
            ))
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Erreur lors de l'ajout du patient : {e}")
        else:
            self.connection.commit()
        finally:
            cursor.close()

    def get_all_patients(self):
        """
        Retourne la liste de tous les patients sous forme de tuples.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT id, first_name, last_name, phone, age, gender, address, blood_group
                FROM patients
                ORDER BY first_name, last_name
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la récupération des patients : {e}")
        finally:
            cursor.close()

    def get_patient_by_id(self, patient_id):
        """
        Recherche un patient par son identifiant.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT id, first_name, last_name, phone, age, gender, address, blood_group
                FROM patients
                WHERE id = ?
            """, (patient_id,))
            row = cursor.fetchone()

            if row is None:
                raise NotFoundError(f"Aucun patient trouvé avec l'identifiant {patient_id}.")

            return row
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la recherche du patient : {e}")
        finally:
            cursor.close()

    # ============================================================
    # MEDECINS
    # ============================================================

    def add_doctor(self, doctor):
        """
        Ajoute un médecin dans la base.
        doctor doit être un objet Doctor.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO doctors (
                    person_id, first_name, last_name, phone, employee_id, salary, specialty
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                doctor.person_id,
                doctor.first_name,
                doctor.last_name,
                doctor.phone,
                doctor.employee_id,
                doctor.salary,
                doctor.specialty
            ))
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Erreur lors de l'ajout du médecin : {e}")
        else:
            self.connection.commit()
        finally:
            cursor.close()

    def get_all_doctors(self):
        """
        Retourne la liste de tous les médecins.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT person_id, first_name, last_name, phone, employee_id, salary, specialty
                FROM doctors
                ORDER BY first_name, last_name
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la récupération des médecins : {e}")
        finally:
            cursor.close()

    def get_doctor_by_id(self, doctor_id):
        """
        Recherche un médecin par son person_id.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT person_id, first_name, last_name, phone, employee_id, salary, specialty
                FROM doctors
                WHERE person_id = ?
            """, (doctor_id,))
            row = cursor.fetchone()

            if row is None:
                raise NotFoundError(f"Aucun médecin trouvé avec l'identifiant {doctor_id}.")

            return row
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la recherche du médecin : {e}")
        finally:
            cursor.close()

    # ============================================================
    # RENDEZ-VOUS
    # ============================================================

    def add_appointment(self, appointment):
        """
        Ajoute un rendez-vous dans la base.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO appointments (
                    appointment_id, patient_id, doctor_id, appointment_date,
                    appointment_time, reason, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                appointment.appointment_id,
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.appointment_time,
                appointment.reason,
                appointment.status
            ))
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Erreur lors de l'ajout du rendez-vous : {e}")
        else:
            self.connection.commit()
        finally:
            cursor.close()

    def get_all_appointments(self):
        """
        Retourne tous les rendez-vous.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT appointment_id, patient_id, doctor_id, appointment_date,
                       appointment_time, reason, status
                FROM appointments
                ORDER BY appointment_date, appointment_time
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la récupération des rendez-vous : {e}")
        finally:
            cursor.close()

    # ============================================================
    # DOSSIERS MEDICAUX
    # ============================================================

    def add_medical_record(self, medical_record):
        """
        Ajoute un dossier médical dans la base.
        Si la date n'est pas fournie, on met la date/heure actuelle.
        """
        cursor = self.connection.cursor()

        created_at = medical_record.created_at
        if not created_at:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor.execute("""
                INSERT INTO medical_records (
                    record_id, patient_id, diagnosis, treatment, notes, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                medical_record.record_id,
                medical_record.patient_id,
                medical_record.diagnosis,
                medical_record.treatment,
                medical_record.notes,
                created_at
            ))
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Erreur lors de l'ajout du dossier médical : {e}")
        else:
            self.connection.commit()
        finally:
            cursor.close()

    def get_all_medical_records(self):
        """
        Retourne tous les dossiers médicaux.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT record_id, patient_id, diagnosis, treatment, notes, created_at
                FROM medical_records
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la récupération des dossiers médicaux : {e}")
        finally:
            cursor.close()

    # ============================================================
    # FACTURES
    # ============================================================

    def add_invoice(self, invoice):
        """
        Ajoute une facture dans la base.
        Si la date n'est pas fournie, on met la date/heure actuelle.
        """
        cursor = self.connection.cursor()

        created_at = invoice.created_at
        if not created_at:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor.execute("""
                INSERT INTO invoices (
                    invoice_id, patient_id, amount, status, created_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                invoice.invoice_id,
                invoice.patient_id,
                invoice.amount,
                invoice.status,
                created_at
            ))
        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Erreur lors de l'ajout de la facture : {e}")
        else:
            self.connection.commit()
        finally:
            cursor.close()

    def get_all_invoices(self):
        """
        Retourne toutes les factures.
        """
        cursor = self.connection.cursor()

        try:
            cursor.execute("""
                SELECT invoice_id, patient_id, amount, status, created_at
                FROM invoices
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            raise DatabaseError(f"Erreur lors de la récupération des factures : {e}")
        finally:
            cursor.close()

    # ============================================================
    # OUTILS DIVERS
    # ============================================================

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.connection:
            self.connection.close()




def delete_patient(self, patient_id):
    """
    Supprime un patient à partir de son identifiant.
    """
    try:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        self.connection.commit()

        if cursor.rowcount == 0:
            print("Aucun patient trouvé avec cet identifiant.")
        else:
            print("Patient supprimé avec succès.")

    except Exception as e:
        self.connection.rollback()
        print(f"Erreur lors de la suppression du patient : {e}")


def delete_doctor(self, doctor_id):
    """
    Supprime un médecin à partir de son identifiant.
    """
    try:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM doctors WHERE doctor_id = ?", (doctor_id,))
        self.connection.commit()

        if cursor.rowcount == 0:
            print("Aucun médecin trouvé avec cet identifiant.")
        else:
            print("Médecin supprimé avec succès.")

    except Exception as e:
        self.connection.rollback()
        print(f"Erreur lors de la suppression du médecin : {e}")


def delete_appointment(self, appointment_id):
    """
    Supprime un rendez-vous à partir de son identifiant.
    """
    try:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM appointments WHERE appointment_id = ?", (appointment_id,))
        self.connection.commit()

        if cursor.rowcount == 0:
            print("Aucun rendez-vous trouvé avec cet identifiant.")
        else:
            print("Rendez-vous supprimé avec succès.")

    except Exception as e:
        self.connection.rollback()
        print(f"Erreur lors de la suppression du rendez-vous : {e}")


def delete_medical_record(self, record_id):
    """
    Supprime un dossier médical à partir de son identifiant.
    """
    try:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM medical_records WHERE record_id = ?", (record_id,))
        self.connection.commit()

        if cursor.rowcount == 0:
            print("Aucun dossier médical trouvé avec cet identifiant.")
        else:
            print("Dossier médical supprimé avec succès.")

    except Exception as e:
        self.connection.rollback()
        print(f"Erreur lors de la suppression du dossier médical : {e}")


def delete_invoice(self, invoice_id):
    """
    Supprime une facture à partir de son identifiant.
    """
    try:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM invoices WHERE invoice_id = ?", (invoice_id,))
        self.connection.commit()

        if cursor.rowcount == 0:
            print("Aucune facture trouvée avec cet identifiant.")
        else:
            print("Facture supprimée avec succès.")

    except Exception as e:
        self.connection.rollback()
        print(f"Erreur lors de la suppression de la facture : {e}")