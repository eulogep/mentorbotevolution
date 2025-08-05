"""
Euloge Learning Platform - Backend API
=====================================

@author: EULOGE MABIALA
@description: Serveur Flask pour la plateforme d'apprentissage IA
@version: 2.0.0
@license: MIT

Ce serveur fournit les API nécessaires pour la plateforme d'apprentissage
basée sur l'IA et les neurosciences pour optimiser la préparation au TOEIC.
"""

import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.learning import learning_bp
from src.routes.mastery import mastery_bp
from src.routes.analysis import analysis_bp
from src.routes.spaced_repetition import spaced_repetition_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configuration CORS pour permettre les requêtes cross-origin
CORS(app)

# Enregistrement des blueprints existants
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(learning_bp, url_prefix='/api/learning')
app.register_blueprint(mastery_bp, url_prefix='/api/mastery')

# Enregistrement des nouveaux blueprints v2.0
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(spaced_repetition_bp, url_prefix='/api/spaced-repetition')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

