from flask import Blueprint, request, jsonify
import os
from datetime import datetime, timedelta
import json
import random

learning_bp = Blueprint('learning', __name__)

# Simulation d'un client OpenAI pour éviter les problèmes de déploiement
class MockOpenAI:
    def __init__(self, api_key=None, base_url=None):
        pass
    
    class chat:
        class completions:
            @staticmethod
            def create(model, messages, max_tokens, temperature):
                # Simulation de réponse IA
                class MockResponse:
                    def __init__(self):
                        self.choices = [MockChoice()]
                
                class MockChoice:
                    def __init__(self):
                        self.message = MockMessage()
                
                class MockMessage:
                    def __init__(self):
                        self.content = "Réponse simulée de l'IA pour la démonstration"
                
                return MockResponse()

# Configuration OpenAI simulée
client = MockOpenAI(
    api_key=os.getenv('OPENAI_API_KEY', 'demo'),
    base_url=os.getenv('OPENAI_API_BASE', 'demo')
)

# Données simulées pour la démonstration
user_progress = {
    "current_score": 650,
    "target_score": 800,
    "listening": 340,
    "reading": 310,
    "speaking": 140,
    "writing": 130,
    "streak_days": 12,
    "sessions_today": 3,
    "total_sessions": 5,
    "energy_level": "high",
    "chronotype": "morning",
    "next_review": "2h"
}

flashcards_data = [
    {"id": 1, "question": "What does 'accommodate' mean?", "answer": "To provide lodging or sufficient space for", "difficulty": "medium", "next_review": datetime.now() + timedelta(hours=2)},
    {"id": 2, "question": "Difference between 'will' and 'going to'?", "answer": "'Will' for spontaneous decisions, 'going to' for planned actions", "difficulty": "hard", "next_review": datetime.now() + timedelta(hours=4)},
    {"id": 3, "question": "What is a conditional sentence?", "answer": "A sentence expressing a condition and its result (if...then)", "difficulty": "easy", "next_review": datetime.now() + timedelta(hours=1)}
]

@learning_bp.route('/progress', methods=['GET'])
def get_progress():
    """Récupère les données de progression de l'utilisateur"""
    return jsonify(user_progress)

@learning_bp.route('/progress', methods=['POST'])
def update_progress():
    """Met à jour la progression de l'utilisateur"""
    data = request.get_json()
    user_progress.update(data)
    return jsonify({"status": "success", "message": "Progress updated"})

@learning_bp.route('/spaced-repetition/cards', methods=['GET'])
def get_spaced_repetition_cards():
    """Récupère les cartes pour la répétition espacée"""
    now = datetime.now()
    due_cards = [card for card in flashcards_data if card['next_review'] <= now]
    return jsonify({
        "due_cards": len(due_cards),
        "new_cards": 8,
        "cards": due_cards[:5]  # Limite à 5 cartes par session
    })

@learning_bp.route('/spaced-repetition/review', methods=['POST'])
def review_card():
    """Traite la révision d'une carte et calcule le prochain intervalle"""
    data = request.get_json()
    card_id = data.get('card_id')
    difficulty = data.get('difficulty')  # 'easy', 'medium', 'hard', 'again'
    
    # Algorithme de répétition espacée simplifié
    intervals = {
        'again': timedelta(minutes=10),
        'hard': timedelta(hours=1),
        'medium': timedelta(hours=4),
        'easy': timedelta(days=1)
    }
    
    # Trouve et met à jour la carte
    for card in flashcards_data:
        if card['id'] == card_id:
            card['next_review'] = datetime.now() + intervals.get(difficulty, timedelta(hours=4))
            break
    
    return jsonify({"status": "success", "next_review": card['next_review'].isoformat()})

@learning_bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    """Assistant IA conversationnel pour l'apprentissage"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant IA spécialisé dans l'apprentissage de l'anglais et la préparation au TOEIC. Réponds de manière pédagogique et encourageante."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})
        
    except Exception as e:
        return jsonify({"error": "Service IA temporairement indisponible", "details": str(e)}), 500

@learning_bp.route('/ai/quiz/generate', methods=['POST'])
def generate_quiz():
    """Génère un quiz adaptatif basé sur le niveau de l'utilisateur"""
    data = request.get_json()
    topic = data.get('topic', 'general')
    difficulty = data.get('difficulty', 'intermediate')
    
    try:
        prompt = f"""Génère un quiz TOEIC de 5 questions sur le thème '{topic}' avec un niveau '{difficulty}'. 
        Format JSON avec: question, options (A,B,C,D), correct_answer, explanation.
        Exemple de format:
        {{
            "questions": [
                {{
                    "question": "What is the main purpose of the meeting?",
                    "options": {{"A": "To discuss budget", "B": "To plan vacation", "C": "To review performance", "D": "To hire staff"}},
                    "correct_answer": "A",
                    "explanation": "The meeting agenda clearly states budget discussion as the main topic."
                }}
            ]
        }}"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.5
        )
        
        quiz_content = response.choices[0].message.content
        # Tente de parser le JSON, sinon retourne un quiz par défaut
        try:
            quiz_data = json.loads(quiz_content)
        except:
            quiz_data = {
                "questions": [
                    {
                        "question": "Which word best completes the sentence: 'The company will _____ its employees about the new policy.'",
                        "options": {"A": "inform", "B": "perform", "C": "confirm", "D": "reform"},
                        "correct_answer": "A",
                        "explanation": "'Inform' means to give information to someone, which fits the context."
                    }
                ]
            }
        
        return jsonify(quiz_data)
        
    except Exception as e:
        # Quiz de fallback en cas d'erreur
        fallback_quiz = {
            "questions": [
                {
                    "question": "What does 'deadline' mean?",
                    "options": {"A": "A line that is dead", "B": "The latest time by which something must be completed", "C": "A type of fishing line", "D": "A dangerous situation"},
                    "correct_answer": "B",
                    "explanation": "A deadline is the latest time or date by which something should be completed."
                }
            ]
        }
        return jsonify(fallback_quiz)

@learning_bp.route('/productivity/deep-work', methods=['POST'])
def start_deep_work():
    """Démarre une session de Deep Work"""
    data = request.get_json()
    duration = data.get('duration', 45)  # minutes
    
    session_data = {
        "session_id": f"dw_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "duration": duration,
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=duration)).isoformat(),
        "status": "active"
    }
    
    return jsonify(session_data)

@learning_bp.route('/productivity/energy', methods=['POST'])
def log_energy():
    """Enregistre le niveau d'énergie de l'utilisateur"""
    data = request.get_json()
    energy_level = data.get('energy_level')  # 'low', 'medium', 'high'
    
    # Recommandations basées sur le niveau d'énergie
    recommendations = {
        'high': ['Tâches complexes', 'Nouveau vocabulaire', 'Grammaire avancée'],
        'medium': ['Révisions', 'Exercices de listening', 'Lecture'],
        'low': ['Flashcards simples', 'Révision passive', 'Pause recommandée']
    }
    
    return jsonify({
        "energy_level": energy_level,
        "recommendations": recommendations.get(energy_level, []),
        "timestamp": datetime.now().isoformat()
    })

@learning_bp.route('/collaborative/groups', methods=['GET'])
def get_study_groups():
    """Récupère les groupes d'étude disponibles"""
    groups = [
        {
            "id": 1,
            "name": "TOEIC 800+ Challenge",
            "members": 12,
            "next_session": "Aujourd'hui 19h",
            "topic": "Business English",
            "level": "Advanced"
        },
        {
            "id": 2,
            "name": "Grammar Masters",
            "members": 8,
            "next_session": "Demain 14h",
            "topic": "Advanced Grammar",
            "level": "Intermediate+"
        }
    ]
    
    return jsonify({"groups": groups})

@learning_bp.route('/collaborative/mentor', methods=['GET'])
def get_mentor_info():
    """Récupère les informations du mentor assigné"""
    mentor = {
        "name": "Sarah K.",
        "score": 850,
        "status": "available",
        "specialties": ["Business English", "TOEIC Strategy"],
        "sessions_completed": 47,
        "rating": 4.9
    }
    
    return jsonify(mentor)

@learning_bp.route('/analytics/performance', methods=['GET'])
def get_performance_analytics():
    """Récupère les analytics de performance avec recommandations IA"""
    analytics = {
        "weekly_progress": {
            "sessions": 21,
            "hours_studied": 15.5,
            "cards_reviewed": 234,
            "quiz_accuracy": 0.87
        },
        "strengths": ["Listening comprehension", "Vocabulary retention"],
        "weaknesses": ["Reading speed", "Complex grammar"],
        "ai_recommendations": [
            {
                "type": "focus_area",
                "message": "Concentrez-vous sur le Reading",
                "reason": "Votre score le plus faible. +30 points possibles",
                "priority": "high"
            },
            {
                "type": "timing",
                "message": "Session Deep Work recommandée",
                "reason": "Votre pic d'énergie: 14h-16h",
                "priority": "medium"
            }
        ],
        "next_milestone": {
            "target": 700,
            "estimated_date": "2024-09-15",
            "confidence": 0.85
        }
    }
    
    return jsonify(analytics)

@learning_bp.route('/neuroscience/feynman', methods=['POST'])
def feynman_explanation():
    """Génère une explication selon la technique Feynman"""
    data = request.get_json()
    concept = data.get('concept', '')
    
    try:
        prompt = f"""Explique le concept '{concept}' en utilisant la technique Feynman:
        1. Utilise un langage simple et accessible
        2. Utilise des analogies et des exemples concrets
        3. Identifie les points qui pourraient être confus
        4. Propose une visualisation ou un schéma mental
        
        Format ta réponse en JSON avec les clés: simple_explanation, analogy, potential_confusion, visualization"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.6
        )
        
        explanation = response.choices[0].message.content
        try:
            explanation_data = json.loads(explanation)
        except:
            explanation_data = {
                "simple_explanation": f"Explication simplifiée de {concept}",
                "analogy": "Analogie pour mieux comprendre",
                "potential_confusion": "Points à clarifier",
                "visualization": "Image mentale suggérée"
            }
        
        return jsonify(explanation_data)
        
    except Exception as e:
        return jsonify({"error": "Service d'explication temporairement indisponible"}), 500

