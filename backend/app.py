from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from config import Config
import sys
import os

# Fix import path for models if running from root
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from database.models import db, User, Career, College, UserResponse
from chatbot.chatbot_logic import get_chat_response

# Initialize Flask with custom template and static folders
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config.from_object(Config)
CORS(app) # Enable CORS for frontend

db.init_app(app)

# --- View Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/register.html')
def register_page():
     # In our design, register is part of login.html or handled effectively there.
     # If separate, render it, but for now we map it to login or just render login with a parameter in frontend JS
     return render_template('login.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/questionnaire.html')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/colleges.html')
def colleges():
    return render_template('colleges.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# --- API Routes ---

# --- API Routes ---

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "msg": "CareerScope Backend Running"})

# Register Blueprints
from backend.routes.colleges import colleges_bp
from backend.routes.chatbot import chatbot_bp

app.register_blueprint(colleges_bp)
app.register_blueprint(chatbot_bp)

# Auth Routes (Mock for now, real implementation would use JWT/Session)
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    # In real app: hash password, save to DB
    # For prototype: Just mock success
    return jsonify({"success": True, "message": "User registered!", "user": {"name": data.get('name')}})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    # For prototype: Accept any login
    return jsonify({"success": True, "token": "mock-token-123", "user": {"name": "Test User"}})

# Recommendation Route (Mock Logic)
@app.route('/api/recommend', methods=['POST'])
def recommend():
    # In a real engine, we would parse user answers.
    # For now, we return all careers or filter slightly if we had logic enabled.
    # To keep it simple and showing DB integration, we return all careers.
    
    careers = Career.query.all()
    recommendations = []
    
    # Mock matching logic (just to show variability)
    # in reality, you'd match `item.required_skills` with `user_skills`
    for item in careers:
        recommendations.append({
            "title": item.title,
            "match": "85%", # Placeholder match score
            "reason": f"Matches your interest in {item.recommended_stream}",
            "salary": item.avg_salary
        })
        
    return jsonify({"recommendations": recommendations})


# Initialize DB
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
