from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class UserProfile(db.Model):
    """User profile model for quiz responses"""
    __tablename__ = 'user_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    class_level = db.Column(db.String(20), nullable=False)
    stream = db.Column(db.String(50), nullable=False)
    math_score = db.Column(db.Integer, default=0)
    science_score = db.Column(db.Integer, default=0)
    english_score = db.Column(db.Integer, default=0)
    social_score = db.Column(db.Integer, default=0)
    interests = db.Column(db.Text, default='[]')  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_interests(self):
        """Parse interests JSON"""
        try:
            return json.loads(self.interests) if self.interests else []
        except:
            return []
    
    def set_interests(self, interests_list):
        """Set interests as JSON"""
        self.interests = json.dumps(interests_list)
    
    def __repr__(self):
        return f'<UserProfile user_id={self.user_id}>'

class College(db.Model):
    """College model"""
    __tablename__ = 'college'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    city = db.Column(db.String(100), index=True)
    state = db.Column(db.String(50), index=True)
    type = db.Column(db.String(50), index=True)  # Engineering, Medical, Arts, Commerce, Management, Law, Design
    rating = db.Column(db.Float, default=0.0)
    placement_pct = db.Column(db.String(20))  # "95%"
    fees = db.Column(db.String(50))  # "₹2.2L" or "₹1.3K"
    established = db.Column(db.Integer)
    address = db.Column(db.String(255))
    description = db.Column(db.Text)
    courses = db.Column(db.Text)  # JSON string or comma-separated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_courses(self):
        """Parse courses"""
        if not self.courses:
            return []
        try:
            return json.loads(self.courses)
        except:
            return self.courses.split(',')
    
    def set_courses(self, courses_list):
        """Set courses as JSON"""
        self.courses = json.dumps(courses_list)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'type': self.type,
            'rating': self.rating,
            'placement_pct': self.placement_pct,
            'fees': self.fees,
            'established': self.established,
            'address': self.address,
            'description': self.description,
            'courses': self.get_courses()
        }
    
    def __repr__(self):
        return f'<College {self.name}>'
