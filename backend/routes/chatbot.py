from flask import Blueprint, jsonify, request
from backend.utils.data_loader import load_colleges_data
import random

chatbot_bp = Blueprint('chatbot', __name__)

COLLEGES_DATA = load_colleges_data()

def find_college_info(query):
    """
    Simple keyword search for college info in the dataset.
    """
    query = query.lower()
    matches = []
    
    # Check for direct college name match
    for college in COLLEGES_DATA:
        if college['College_Name'].lower() in query:
            matches.append(college)
            
    if not matches:
        # Try generic search
        words = query.split()
        for college in COLLEGES_DATA:
            # Match if any significant word of college name is in query
            # (Very naive, but works for exact names)
            if any(word in college['College_Name'].lower() for word in words if len(word) > 4):
                 matches.append(college)
                 if len(matches) > 0: break # Just find one for now

    return matches[0] if matches else None

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chatbot interactions.
    """
    data = request.json
    user_msg = data.get('message', '').strip()
    
    if not user_msg:
        return jsonify({"reply": "Please say something!"})

    response = ""
    lower_msg = user_msg.lower()

    # Intent Detection
    
    # 1. Greeting
    if any(x in lower_msg for x in ['hi', 'hello', 'hey', 'namaste']):
        response = "Hello! I am your CareerScope assistant. Ask me about careers or colleges (e.g., 'Suggest colleges in Mumbai', 'Fees of IIT Bombay')."

    # 2. Specific College Info
    elif any(x in lower_msg for x in ['fees', 'placement', 'rating', 'info', 'about']):
        college = find_college_info(lower_msg)
        if college:
            name = college['College_Name']
            fees = college['UG_fee']
            rating = college['Rating']
            placement = college['Placement']
            # formatting response
            if 'fees' in lower_msg:
                response = f"The UG fees for **{name}** is approx ₹{fees}."
            elif 'placement' in lower_msg:
                response = f"**{name}** has a placement score of {placement}/10."
            elif 'rating' in lower_msg:
                response = f"**{name}** has an overall rating of {rating}/10."
            else:
                response = f"**{name}** is located in {college['State']}. Rating: {rating}/10, Fees: ₹{fees}."
        else:
            response = "I couldn't find that specific college. Please check the spelling or ask about another one."

    # 3. Suggestion / List
    elif 'suggest' in lower_msg or 'best colleges' in lower_msg or 'top colleges' in lower_msg:
        # Extract state if mentioned
        states = list(set(str(c.get('State', '')).lower() for c in COLLEGES_DATA))
        found_state = None
        for state in states:
            if state in lower_msg:
                found_state = state
                break
        
        filtered = COLLEGES_DATA
        if found_state:
            filtered = [c for c in filtered if str(c.get('State', '')).lower() == found_state]
        
        # Sort by rating
        filtered.sort(key=lambda x: float(x.get('Rating', 0)), reverse=True)
        top_5 = filtered[:5]
        
        if top_5:
            list_str = "\n".join([f"- **{c['College_Name']}** (Rating: {c['Rating']})" for c in top_5])
            response = f"Here are the top colleges{' in ' + found_state.title() if found_state else ''}:\n{list_str}"
        else:
            response = "I couldn't find any colleges matching your criteria."

    # 4. Career Advice (Generic)
    elif 'career' in lower_msg or 'job' in lower_msg:
        response = "For career advice, focus on your interests. If you like coding, explore CS/IT. If you like design, look into UI/UX or Architecture. Check out our 'Questionnaire' page for a personalized path!"
        
    # Default
    else:
        response = "I am still learning! You can ask me about college fees, ratings, or ask for suggestions like 'Best colleges in Pune'."

    return jsonify({"reply": response})
