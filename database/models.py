from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to responses
    responses = db.relationship('UserResponse', backref='user', lazy=True)

class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.String(200)) # e.g. "Math, Coding"
    recommended_stream = db.Column(db.String(50)) # e.g. "Science"
    avg_salary = db.Column(db.String(50))

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    fees = db.Column(db.String(50))
    courses = db.Column(db.String(200)) # Comma separated list for simplicity
    
class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    academic_level = db.Column(db.String(50))
    stream = db.Column(db.String(50))
    interests = db.Column(db.String(500)) # JSON string or comma separated
    skills = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
