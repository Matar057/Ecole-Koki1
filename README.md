# EduManage - Système de Gestion Scolaire

Un système de gestion scolaire complet, full-stack, construit avec Django, conçu pour les environnements d'enseignement secondaire.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Fonctionnalités

### Rôles Utilisateurs & Authentification
- **Admin** : Accès complet au système, gestion des utilisateurs, configuration
- **Enseignants** : Gestion des classes, saisie des notes, prise de présence
- **Étudiants** : Consultation des notes, présence, emploi du temps
- **Parents** : Suivi de la progression des enfants, statut des frais

### Modules Principaux

| Module | Fonctionnalités |
|--------|-----------------|
| **Gestion des Étudiants** | Opérations CRUD, photos de profil, documents, lien avec les parents |
| **Gestion des Enseignants** | Gestion de profil, assignation de matières/classes |
| **Classes & Matières** | Années académiques, classes, sections, gestion des matières |
| **Présence** | Suivi quotidien, saisie en masse, rapports, export Excel |
| **Examens & Résultats** | Création d'examens, saisie des notes, notation automatique, bulletins PDF |
| **Gestion des Frais** | Structure des frais, suivi des paiements, reçus PDF, résumés |
| **Emploi du Temps** | Horaires des classes, horaires des enseignants, vue hebdomadaire |
| **Notifications** | Annonces, alertes par email, notifications sur le tableau de bord |

### Analytique du Tableau de Bord
- Nombre d'étudiants/enseignants
- Graphiques de taux de présence (Chart.js)
- Visualisation des étudiants par classe
- Résumé de la collecte des frais
- Examens à venir & annonces

## Stack Technique

- **Backend** : Django 5.0+
- **Base de données** : SQLite (dev) / PostgreSQL (production)
- **Frontend** : Bootstrap 5, Chart.js, Bootstrap Icons
- **Génération PDF** : ReportLab
- **Export Excel** : XlsxWriter
- **Formulaires** : Crispy Forms + Bootstrap 5

## Structure du Projet

```
gestion_scolaire_django/
├── config/                 # Paramètres du projet
│   ├── settings.py
│   ├── urls.py
│   └── context_processors.py
├── users/                  # Authentification & gestion des utilisateurs
├── students/               # Profils & documents des étudiants
├── teachers/               # Gestion des enseignants
├── academics/              # Classes, sections, matières
├── attendance/             # Suivi de la présence
├── exams/                  # Examens, notes, bulletins
├── fees/                   # Structure des frais & paiements
├── timetable/              # Horaires des classes & enseignants
├── notifications/          # Annonces & alertes
├── dashboard/              # Tableau de bord analytique
├── templates/              # Templates HTML
├── static/                 # CSS, JS, images
├── media/                  # Fichiers téléchargés
└── manage.py
```

## Démarrage Rapide

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner ou naviguer vers le répertoire du projet**
   ```bash
   cd gestion_scolaire_django
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement**
   ```bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```

5. **Exécuter les migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Charger les données exemples**
   ```bash
   python manage.py seed_data
   ```

7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

8. **Accéder à l'application**
   - Ouvrir : http://localhost:8000
   - Panneau d'administration : http://localhost:8000/admin

### Identifiants de Connexion par Défaut

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Admin | admin@school.com | admin123 |
| Enseignant | john.smith@school.com | teacher123 |
| Étudiant | alice.smith0@student.school.com | student123 |
| Parent | robert.anderson@email.com | parent123 |

## Déploiement en Production

### Configuration PostgreSQL

1. Installer PostgreSQL et créer une base de données :
   ```sql
   CREATE DATABASE school_management;
   CREATE USER schooldbuser WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE school_management TO schooldbuser;
   ```

2. Mettre à jour `.env` :
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=school_management
   DB_USER=schooldbuser
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. Installer l'adaptateur PostgreSQL :
   ```bash
   pip install psycopg2-binary
   ```

### Gunicorn + Nginx

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Points d'Accès API (Disponibles via l'Admin Django)

Le système utilise l'interface d'administration intégrée de Django pour un accès de type API. Pour un support API REST, intégrer Django REST Framework.

## Fonctionnalités de Sécurité

- Protection CSRF sur tous les formulaires
- Chiffrement des mots de passe (intégré à Django)
- Contrôle d'accès basé sur les rôles
- Validation des entrées via les formulaires Django
- Gestion sécurisée des téléchargements de fichiers
- Protection XSS via les templates Django

## Personnalisation

### Ajouter de Nouveaux Rôles
Modifier `users/models.py` et ajouter à `ROLE_CHOICES` :
```python
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('teacher', 'Enseignant'),
    ('student', 'Étudiant'),
    ('parent', 'Parent'),
    ('librarian', 'Bibliothécaire'),  # Nouveau rôle
)
```

### Configuration Email
Pour les notifications email en production, mettre à jour `.env` :
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## Contribution

1. Forker le repository
2. Créer une branche de fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. Valider vos modifications (`git commit -m 'Ajouter une fonctionnalité incroyable'`)
4. Pousser vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT.

## Support

Pour les problèmes et les demandes de fonctionnalités, veuillez ouvrir une issue sur le repository.

---

Construit avec Django | Bootstrap 5 | Chart.js
