import os
from flask import Flask, render_template, session
from flask_cors import CORS
from database.models.models import db

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'career-scope-dev-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careerscope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 604800  # 7 days
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

# Enable CORS for frontend, allowing credentials for sessions
CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize database
db.init_app(app)

# Register Blueprints
from routes.auth import auth_bp
from routes.quiz import quiz_bp
from routes.careers import careers_bp
from routes.colleges import colleges_bp
from routes.chatbot import chatbot_bp

app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(careers_bp)
app.register_blueprint(colleges_bp)
app.register_blueprint(chatbot_bp)

# Create database tables
with app.app_context():
    db.create_all()

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """
    Serve index.html for all routes to allow React to handle routing
    Only for non-API routes
    """
    if path.startswith('api/'):
        return {'error': 'API route not found'}, 404
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
