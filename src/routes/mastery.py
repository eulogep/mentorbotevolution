from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import random

mastery_bp = Blueprint('mastery', __name__)

@mastery_bp.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = [
        {
            "id": 1,
            "name": "TOEIC Listening",
            "description": "Compréhension orale du TOEIC",
            "progress": 75,
            "status": "in_progress",
            "color": "from-blue-500 to-blue-600"
        },
        {
            "id": 2,
            "name": "TOEIC Reading",
            "description": "Compréhension écrite du TOEIC",
            "progress": 45,
            "status": "needs_attention",
            "color": "from-green-500 to-green-600"
        },
        {
            "id": 3,
            "name": "Grammaire Avancée",
            "description": "Règles grammaticales complexes",
            "progress": 90,
            "status": "mastered",
            "color": "from-purple-500 to-purple-600"
        }
    ]
    return jsonify(subjects)

@mastery_bp.route('/get-subjects', methods=['GET'])
def get_subjects_enhanced():
    """Endpoint attendu par le frontend: retourne {status, subjects: [...]} avec un schéma riche"""
    # Génération de données simulées enrichies compatibles avec MasteryDashboard
    base_subjects = [
        {
            "id": 1,
            "name": "TOEIC Listening",
            "description": "Compréhension orale du TOEIC",
            "progress": 72,
        },
        {
            "id": 2,
            "name": "TOEIC Reading",
            "description": "Compréhension écrite du TOEIC",
            "progress": 48,
        },
        {
            "id": 3,
            "name": "Grammaire Avancée",
            "description": "Règles grammaticales complexes",
            "progress": 91,
        },
    ]

    def fake_concepts():
        concepts = []
        statuses = ['completed', 'in-progress', 'not-started']
        names = [
            'Phrasal Verbs', 'Tenses Review', 'Business Vocabulary',
            'Conditional Sentences', 'Reading Strategies', 'Listening Accents'
        ]
        for i, nm in enumerate(random.sample(names, k=4)):
            status = random.choice(statuses)
            mastery = 100 if status == 'completed' else (random.randint(40, 85) if status == 'in-progress' else 0)
            concepts.append({
                'id': i + 1,
                'name': nm,
                'status': status,
                'mastery': mastery,
            })
        return concepts

    subjects = []
    now = datetime.now()
    for s in base_subjects:
        subjects.append({
            **s,
            "target_score": 800,
            "current_score": random.randint(600, 720),
            "next_session": (now + timedelta(hours=random.randint(2, 48))).strftime('%d %b, %H:%M'),
            "total_time": random.randint(12, 60),  # heures
            "streak": random.randint(3, 20),
            "concepts": fake_concepts(),
        })

    return jsonify({
        'status': 'success',
        'subjects': subjects,
    })

@mastery_bp.route('/plan', methods=['POST'])
def create_plan():
    data = request.get_json()
    
    # Logique pour créer un plan d'apprentissage
    plan = {
        "id": 1,
        "subject": data.get('subject', 'TOEIC'),
        "duration": data.get('duration', '30'),
        "focus_areas": data.get('focus_areas', ['listening', 'reading']),
        "created_at": datetime.utcnow().isoformat() + 'Z'
    }
    
    return jsonify(plan), 201 