# 🏥 Système de Gestion d'une Clinique Médicale

## Description

Le **Système de Gestion d'une Clinique Médicale** est une application de bureau développée en **Python** dans le cadre du cours de **Génie Logiciel**.

L'application permet d'automatiser la gestion des activités d'une clinique médicale grâce à une interface graphique conviviale développée avec **Tkinter** et une base de données **SQLite**.

---

# Fonctionnalités

L'application permet de :

- Gérer les patients
  - Ajouter un patient
  - Modifier un patientS
  - Supprimer un patient
  - Rechercher un patient
  - Afficher tous les patients

- Gérer les médecins
  - Ajouter un médecin
  - Modifier un médecin
  - Supprimer un médecin
  - Rechercher un médecin

- Gérer les rendez-vous
  - Programmer un rendez-vous
  - Modifier un rendez-vous
  - Supprimer un rendez-vous

- Gérer les dossiers médicaux
  - Ajouter un dossier médical
  - Consulter un dossier médical
  - Supprimer un dossier médical

- Gérer la facturation
  - Créer une facture
  - Calcul automatique du montant
  - Différents types de facturation

- Afficher les statistiques
  - Nombre de patients
  - Nombre de médecins
  - Nombre de rendez-vous
  - Nombre de factures
  - Chiffre d'affaires



# Technologies utilisées

- Python 3
- Tkinter
- SQLite3


# Concepts de Génie Logiciel utilisés

Ce projet met en œuvre plusieurs concepts de programmation orientée objet :

- Encapsulation
- Héritage 
- Polymorphisme
- Classe abstraite
- Gestion des exceptions

Patrons de conception utilisés :

- Factory Pattern
- Strategy Pattern

---

# Structure du projet

```
Gestion_Clinique_Medicale/

│── main.py
│── README.md
│── requirements.txt

├── exceptions
│   ├── custom_exceptions.py
│   └── __init__.py

├── models
│   ├── person.py
│   ├── patient.py
│   ├── doctor.py
│   ├── staff.py
│   ├── appointment.py
│   ├── medical_record.py
│   ├── invoice.py
│   └── __init__.py

├── patterns
│   ├── factory.py
│   ├── strategy.py
│   └── __init__.py

├── persistence
│   ├── data_manager.py
│   └── __init__.py

├── services
│   ├── clinic_manager.py
│   ├── billing_service.py
│   ├── notification_service.py
│   ├── search_service.py
│   └── __init__.py

└── ui
    ├── app.py
    └── __init__.py
```

---

# Installation

## 1. Cloner le projet

```bash
git clone https://github.com/Blessing/EXAMEN POO1
```

---

## 2. Se placer dans le dossier

```bash
cd Gestion-Clinique-Medicale
```

---

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 4. Lancer l'application

```bash
python main.py
```

---

# Base de données

L'application utilise une base de données **SQLite**.

Le fichier est créé automatiquement :

```
clinique_medicale_poo.db
```

---

# Gestion des erreurs

Le système effectue plusieurs validations :

- Vérification des champs obligatoires
- Validation des numéros de téléphone
- Validation de l'âge
- Validation des montants
- Vérification des identifiants
- Gestion des conflits de rendez-vous
- Gestion des exceptions SQLite

Les exceptions personnalisées utilisées sont :

- ValidationError
- DatabaseError
- NotFoundError
- BillingError
- AppointmentConflictError
