from flask import Blueprint, request, jsonify

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

@mastery_bp.route('/plan', methods=['POST'])
def create_plan():
    data = request.get_json()
    
    # Logique pour créer un plan d'apprentissage
    plan = {
        "id": 1,
        "subject": data.get('subject', 'TOEIC'),
        "duration": data.get('duration', '30'),
        "focus_areas": data.get('focus_areas', ['listening', 'reading']),
        "created_at": "2024-01-08T10:00:00Z"
    }
    
    return jsonify(plan), 201 