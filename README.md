# Test Technique Backend

Ce projet est une API backend réalisée avec Django et Django REST Framework, permettant de :
- Enregistrer une adresse en base de données
- Consulter les risques associés via l'API Géorisques

L'application est entièrement dockerisée pour un déploiement facile.

---

## 🚀 Stack Technique

- Python 3.12
- Django 4.2
- Django REST Framework
- SQLite3
- Docker & Docker Compose
- Gunicorn (serveur WSGI de production)

---

## 📦 Guide de Démarrage Rapide

### Option 1 : Démarrage Local sans Docker (développement)

1. Cloner le projet :

    ```bash
    git clone https://github.com/qiuziyuan/Klaire-Tech-Test.git
    cd Klaire-Tech-Test
    ```

2. Créer un environnement virtuel et installer les dépendances :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows : venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Créer le dossier `data/` s'il n'existe pas :

    ```bash
    mkdir data
    ```

4. Créer un fichier `.env` avec ce contenu :

    ```env
    DATABASE_URL=sqlite:///data/db.sqlite3
    ```

5. Effectuer les migrations et lancer le serveur :

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

Accédez à l'API sur : `http://127.0.0.1:8000/`

---

### Option 2 : Démarrage via Docker (recommandé)

1. Cloner le projet :

    ```bash
    git clone https://github.com/qiuziyuan/Klaire-Tech-Test.git
    cd Klaire-Tech-Test
    ```

2. Créer le dossier `data/` s'il n'existe pas :

    ```bash
    mkdir data
    ```

3. Vérifier que le fichier `.env` existe, sinon le créer :

    ```env
    DATABASE_URL=sqlite:////data/db.sqlite3
    ```

4. Lancer les commandes Docker :

    ```bash
    docker compose build
    docker compose up
    ```

Accédez à l'API sur : `http://localhost:8000/`

---

### 🚀 Démarrage Automatique en Un Clic (Scripts)

Ce projet fournit deux scripts pour un démarrage rapide :

- **Linux / Mac** :

    ```bash
    ./start.sh
    ```

- **Windows PowerShell** :

    ```powershell
    .\start.ps1
    ```

**Fonctionnalités du script :**
- Crée automatiquement le dossier `data/` si nécessaire
- Vérifie l'existence du fichier `.env`
- Construit l'image Docker
- Démarre les conteneurs avec `docker compose up`

---

## ⚙️ Variables d'Environnement

| Variable | Valeur par défaut | Description |
|:---|:---|:---|
| `DATABASE_URL` | sqlite:////data/db.sqlite3 | Chemin de la base de données SQLite |

---

## 📚 Documentation de l'API

### 1. Enregistrer une Adresse

**POST** `/api/addresses/`

- **Payload JSON** :

    ```json
    {
      "q": "8 bd du Port"
    }
    ```

- **Réponse Succès (200 OK)** :

    ```json
    {
    "id": 1,
    "label": "8 Boulevard du Port 95000 Cergy",
    "housenumber": "8",
    "street": "Boulevard du Port",
    "postcode": "95000",
    "citycode": "95127",
    "latitude": 49.031624,
    "longitude": 2.062821
    }
    ```

- **Erreurs possibles** :
  - 400 Bad Request
  - 404 Adresse introuvable
  - 500 Erreur serveur (API externe inaccessible)

---

### 2. Consulter les Risques d'une Adresse

**GET** `/api/addresses/{id}/risks/`

- **Réponse Succès (200 OK)** :
  
  Retourne le JSON complet de l'API Géorisques.

- **Erreurs possibles** :
  - 404 Adresse introuvable
  - 500 Erreur serveur (API Géorisques inaccessible)

---

## 🧪 Tests Unitaires

### Scénarios supplémentaires couverts

- ✅ **Validation d'entrée** :
  - Champ `q` manquant ➔ 400 Bad Request
  - Champ `q` vide ➔ 400 Bad Request
- ✅ **Création d'adresse** :
  - Succès ➔ 200 OK
  - Adresse non trouvée via API externe ➔ 404 Not Found
  - Échec de l'API externe ➔ 500 Internal Server Error
- ✅ **Consultation des risques** :
  - Succès ➔ 200 OK
  - Adresse inexistante en base ➔ 404 Not Found
  - Échec d'appel à l'API Géorisques ➔ 500 Internal Server Error

### Technologies utilisées pour les tests

- **Django TestCase** pour les tests unitaires
- **Unittest.mock.patch** pour simuler les appels aux API externes

### Avant de lancer les tests

Pour exécuter correctement les tests en local (hors Docker), merci de suivre ces étapes préalables :

1. Créer et activer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate
```
2. Installer les dépendances du projet :
```bash
pip install -r requirements.txt
```

### Lancer tous les tests

Depuis la racine du projet, exécuter :

```bash
python manage.py test
```
---

## 🛠 FAQ

- **Problème : Docker ne trouve pas de fichier de configuration**  
  ➔ Vérifiez que vous êtes bien dans le dossier contenant `docker-compose.yml`.

- **Problème : Fichier .env manquant**  
  ➔ Créez un fichier `.env` avec la variable `DATABASE_URL`.

- **Problème : Erreur d'accès API**  
  ➔ Vérifiez votre connexion internet et les URLs externes (api-adresse.data.gouv.fr, georisques.gouv.fr).

---

## 👨‍💻 Auteur

- **Pierre (qiuziyuan)**
