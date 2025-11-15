# Softdesk – API

Gestion collaborative de projets, tickets et commentaires

---

## Sommaire

- Présentation
- Fonctionnalités principales
- Prérequis
- Installation et configuration
- Gestion des dépendances (Pipenv)
- Variables d’environnement à paramétrer
- Lancement et utilisation
- Sécurité et bonnes pratiques
- Pagination
- Endpoints API principaux
- Mises à jour automatiques (Dependabot)
- Conseils pour les tests

---

## Présentation

Softdesk est une API RESTful permettant la gestion sécurisée et collaborative de projets.
Chaque utilisateur authentifié peut créer un projet, y inviter des contributeurs, créer des tickets (« issues ») et échanger via des commentaires.

---

## Fonctionnalités principales

- Authentification sécurisée par tokens JWT
- Gestion des utilisateurs, projets, tickets et commentaires
- Permissions fines (gestion auteur/contributeur, accès restreints)
- Conformité RGPD : consentements utilisateurs, droit à l’oubli
- Pagination intégrée et performances optimisées
- Mises à jour de sécurité automatisées

---

## Prérequis

- Python 3.10 ou supérieur
- Pipenv
- Git
- Base de données SQLite (par défaut)
- Outil de test API (Postman recommandé)

---

## Installation et configuration

1. **Cloner le dépôt :**
    ```
    git clone https://github.com/Americanufo/PROJET_10.git
    cd PROJET_10
    ```

2. **Installer pipenv :**
    ```
    pip install pipenv
    ```

3. **Installer les dépendances dans l’environnement virtuel :**
    ```
    pipenv install
    ```

---

## Lancement et utilisation

1. **Activer l’environnement Pipenv :**
    ```
    pipenv shell
    ```

2. **Appliquer les migrations :**
    ```
    python manage.py migrate
    ```

3. **Créer un superutilisateur :**
    ```
    python manage.py createsuperuser
    ```

4. **Démarrer le serveur :**
    ```
    python manage.py runserver
    ```
    Le serveur sera accessible par défaut sur [http://localhost:8000/](http://localhost:8000/)

---

## Variables d’environnement à paramétrer

- `SECRET_KEY` : clé secrète Django
- `DEBUG` : "True" ou "False" selon l’environnement

---

## Étapes pour sécuriser la clé secrète

La clé secrète Django (`SECRET_KEY`) est une donnée sensible qui ne doit jamais être exposée publiquement.

### 1. Créer un fichier `.env`

Créez un fichier `.env` à la racine de votre projet (là où se trouve le fichier `manage.py`).

- **Sur macOS ou Linux :**

  Ouvrez le terminal, naviguez dans votre projet puis créez le fichier avec un éditeur de texte (exemple : nano) :
  cd /chemin/vers/ton/projet
  nano .env

- **Sur Windows :**

Ouvrez le Bloc-notes (Notepad) ou un autre éditeur de texte, puis créez un fichier nommé `.env` (avec un point au début, pas d'extension) à la racine du projet.

---

### 2. Ajouter la clé secrète dans `.env`

Dans ce fichier `.env`, ajoutez la ligne suivante (remplacez la clé par votre propre clé secrète) :

SECRET_KEY=votre_clef_secrete_django_ici

Sauvegardez et quittez l’éditeur (`Ctrl+O` puis `Entrée` et `Ctrl+X` dans nano).

---

### 3. Ajouter `.env` au `.gitignore`

Pour éviter que le fichier `.env` soit poussé dans votre dépôt git et exposé publiquement, ajoutez `.env` à votre `.gitignore` :


---

### 4. Installer la librairie `python-decouple`

Cette librairie permet de charger automatiquement les variables depuis `.env`.

Installez-la avec :
pip install python-decouple


---

### 5. Modifier `settings.py`

Dans votre fichier `settings.py`, importez `config` depuis `decouple` en ajoutant en haut :
from decouple import config

Puis remplacez la ligne contenant la clé statique par :

SECRET_KEY = config('SECRET_KEY')

---

## Gestion des dépendances (Pipenv)

- Les dépendances sont entièrement gérées par Pipenv (`Pipfile`, `Pipfile.lock`).
- Pour ajouter une librairie :
    ```
    pipenv install nompaquet
    ```
- Les mises à jour sont automatisées avec Dependabot (voir le fichier `.github/dependabot.yml`).

---

## Sécurité et bonnes pratiques

- **Authentification :** JWT obligatoire via DRF Simple JWT pour tous les endpoints.
- **Permissions :** Toutes les ressources sont protégées (`IsAuthenticated`) et soumises à des vérifications d’auteur/contributeur pour modification ou suppression.
- **RGPD :** Collecte du consentement, droit à l’oubli, contrôle strict de l’âge (minimum 15 ans pour l’inscription).
- **Validation :** Entrées utilisateur systématiquement vérifiées (serializers) et sécurisées.
- **Pagination :** Toutes les listes sont paginées pour économiser la bande passante et améliorer l’expérience.

---

## Pagination

- La pagination est configurée à 10 résultats/page.
- Pour naviguer entre les pages, utilisez les paramètres `limit` et `offset` :
    ```
    /api/projects/?limit=10&offset=10
    ```

---

## Endpoints API principaux

- `/api/users/` – Gestion des utilisateurs
- `/api/projects/` – Gestion des projets
- `/api/contributors/` – Gestion des contributeurs de projet
- `/api/issues/` – Création et gestion des tickets
- `/api/comments/` – Ajout et gestion des commentaires

_Note : tous les endpoints nécessitent une authentification JWT._

---

## Mises à jour automatiques avec Dependabot

- Les dépendances du projet sont suivies automatiquement grâce à Dependabot.
- Dès qu’une mise à jour de sécurité est disponible, une Pull Request dédiée est générée.
- Veillez à fusionner ces PRs régulièrement pour maintenir le projet sécurisé.

---

## Conseils pour les tests

- Utilisez Postman ou tout autre client REST pour tester l’ensemble des endpoints.
- Vérifiez les réponses pour différents rôles (auteur, contributeur, utilisateur non connecté) afin de garantir la robustesse des contrôles d’accès.
- N’hésitez pas à consulter le code source pour manipuler l’API.
