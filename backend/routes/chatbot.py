from flask import Blueprint, request, jsonify, session
from chatbot_logic import get_chatbot_response

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/api/chatbot/query', methods=['POST'])
def query_chatbot():
    user_id = session.get('user_id')
    
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"success": False, "message": "Message is required"}), 400
        
    user_message = data['message']
    
    # Use logic from chatbot_logic.py
    response_text = get_chatbot_response(user_message, user_id)
    
    return jsonify({
        "success": True,
        "response": response_text
    })
