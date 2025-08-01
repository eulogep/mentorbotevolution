from flask import Blueprint, request, jsonify

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/progress', methods=['GET'])
def get_progress():
    # Données de progression simulées
    progress_data = {
        'currentScore': 650,
        'targetScore': 800,
        'listening': 340,
        'reading': 310,
        'speaking': 140,
        'writing': 130,
        'streakDays': 12,
        'sessionsToday': 3,
        'totalSessions': 5,
        'nextReview': "2h",
        'weeklyProgress': 29,
        'totalHours': 77,
        'averageStreak': 10
    }
    return jsonify(progress_data)

@learning_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    recommendations = [
        {
            "type": "focus",
            "title": "Concentrez-vous sur le Reading",
            "description": "Votre score le plus faible. +30 points possibles",
            "priority": "high",
            "color": "from-red-500 to-pink-500"
        },
        {
            "type": "timing",
            "title": "Session Deep Work recommandée",
            "description": "Votre pic d'énergie: 14h-16h",
            "priority": "medium",
            "color": "from-blue-500 to-cyan-500"
        },
        {
            "type": "review",
            "title": "Révision espacée optimale",
            "description": "Moment idéal pour réviser le vocabulaire",
            "priority": "medium",
            "color": "from-purple-500 to-indigo-500"
        }
    ]
    return jsonify(recommendations) 