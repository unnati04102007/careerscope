from flask import Blueprint, request, jsonify, session
import json
from database.models.models import db, UserProfile
from routes.careers import get_suggestions

quiz_bp = Blueprint('quiz_bp', __name__)

@quiz_bp.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
        
    data = request.json
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    # Check if profile already exists
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.session.add(profile)
        
    profile.class_level = data.get('class_level', '')
    profile.stream = data.get('stream', '')
    
    # Parse scores
    profile.math_score = data.get('math_score', 0)
    profile.science_score = data.get('science_score', 0)
    profile.english_score = data.get('english_score', 0)
    profile.social_score = data.get('social_score', 0)
    
    interests = data.get('interests', [])
    profile.interests = json.dumps(interests)
    
    db.session.commit()
    
    # Generate career suggestions immediately
    careers = get_suggestions(profile)
    
    return jsonify({
        "success": True, 
        "message": "Profile saved",
        "careers": careers
    })

@quiz_bp.route('/api/quiz/profile', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Not authenticated"}), 401
        
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"success": True, "has_profile": False})
        
    try:
        interests = json.loads(profile.interests) if profile.interests else []
    except:
        interests = []
        
    return jsonify({
        "success": True, 
        "has_profile": True,
        "completed": True,
        "profile": {
            "class_level": profile.class_level,
            "stream": profile.stream,
            "math_score": profile.math_score,
            "science_score": profile.science_score,
            "english_score": profile.english_score,
            "social_score": profile.social_score,
            "interests": interests
        }
    })
