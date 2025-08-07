#!/bin/bash

# Script de build pour Vercel
# Auteur: MABIALA EULOGE

echo "🚀 Démarrage du build par MABIALA EULOGE..."

# Installation des dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements-vercel.txt

# Installation des dépendances Node.js
echo "📦 Installation des dépendances Node.js..."
npm install

# Build du frontend
echo "🏗️ Construction du frontend React..."
npm run build

# Création du dossier de build final
echo "📁 Préparation du dossier de build..."
mkdir -p .vercel/output/static
cp -r dist/* .vercel/output/static/

# Copie des fichiers de l'API
echo "🔧 Configuration de l'API..."
mkdir -p .vercel/output/functions
cp -r api/* .vercel/output/functions/

echo "✅ Build terminé avec succès!"
echo "👨‍💻 Projet construit par MABIALA EULOGE"
