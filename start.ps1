Write-Host "🚀 Démarrage du projet Klaire Backend..."

# Vérifier si le dossier data existe
if (-not (Test-Path -Path "./data")) {
    Write-Host "📁 Création du dossier data..."
    New-Item -ItemType Directory -Path "./data"
}

# Vérifier si le fichier .env existe
if (-not (Test-Path -Path ".env")) {
    Write-Host "⚠️  Fichier .env introuvable ! Merci de le créer avec ce contenu :"
    Write-Host "DATABASE_URL=sqlite:////data/db.sqlite3"
    exit 1
}

# Construction de l'image Docker
Write-Host "🔨 Construction de l'image Docker..."
docker compose build

# Lancement des services Docker
Write-Host "🚢 Lancement des services Docker..."
docker compose up