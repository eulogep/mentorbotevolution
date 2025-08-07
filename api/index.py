"""
Point d'entrée API pour Vercel
Auteur: MABIALA EULOGE
"""

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import sys

# Ajout du chemin racine au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.routes.user import user_bp
from src.routes.learning import learning_bp
from src.routes.mastery import mastery_bp

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Enregistrement des blueprints
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(learning_bp, url_prefix='/api/learning')
app.register_blueprint(mastery_bp, url_prefix='/api/mastery')

@app.route('/')
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'name': 'Euloge Learning Platform API',
        'version': '2.0.0',
        'author': 'MABIALA EULOGE',
        'description': 'API pour la plateforme d\'apprentissage basée sur l\'IA et les neurosciences'
    })

@app.route('/health')
def health_check():
    """Vérification de l'état de l'API"""
    return jsonify({
        'status': 'healthy',
        'author': 'MABIALA EULOGE',
        'version': '2.0.0'
    })
