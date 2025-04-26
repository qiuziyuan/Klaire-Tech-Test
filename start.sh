#!/bin/bash

echo "🚀 Démarrage du projet Klaire Backend..."

# Vérifier si le dossier data existe
if [ ! -d "./data" ]; then
  echo "📁 Création du dossier data..."
  mkdir ./data
fi

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
  echo "⚠️  Fichier .env introuvable ! Merci de le créer avec le contenu suivant :"
  echo "DATABASE_URL=sqlite:////data/db.sqlite3"
  exit 1
fi

# Construction de l'image Docker
echo "🔨 Construction de l'image Docker..."
docker compose build

# Lancer les conteneurs
echo "🚢 Lancement des services Docker..."
docker compose up