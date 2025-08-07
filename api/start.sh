#!/bin/bash

# Script de démarrage pour Vercel
# Auteur: MABIALA EULOGE

echo "🚀 Démarrage de l'application Euloge Learning Platform..."
echo "👨‍💻 Développé par MABIALA EULOGE"

# Activation de l'environnement Python
echo "🐍 Configuration de l'environnement Python..."
python -m venv .venv
source .venv/bin/activate

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements-vercel.txt

# Démarrage de l'application
echo "🌐 Démarrage du serveur..."
gunicorn -c gunicorn_config.py api.index:app
