from flask import Blueprint, request, jsonify, session
import json
from database.models.models import UserProfile

careers_bp = Blueprint('careers_bp', __name__)

def get_suggestions(profile):
    careers = []
    math = profile.math_score or 0
    science = profile.science_score or 0
    english = profile.english_score or 0
    
    try:
        interests = json.loads(profile.interests) if profile.interests else []
    except:
        interests = []
        
    stream = profile.stream or ""

    CAREER_DATA = {
        "Software Engineer": {
            "desc": "Build software systems and applications",
            "salary": "₹6L - ₹40L/yr",
            "type": "Engineering",
            "icon": "💻"
        },
        "Data Scientist": {
            "desc": "Analyze data to drive business decisions",
            "salary": "₹8L - ₹35L/yr",
            "type": "Engineering",
            "icon": "📊"
        },
        "Robotics Engineer": {
            "desc": "Design and build robotic systems",
            "salary": "₹5L - ₹25L/yr",
            "type": "Engineering",
            "icon": "🤖"
        },
        "MBBS Doctor": {
            "desc": "Diagnose and treat patients in clinical settings",
            "salary": "₹8L - ₹50L/yr",
            "type": "Medical",
            "icon": "🏥"
        },
        "Pharmacist": {
            "desc": "Dispense medicines and advise on drug use",
            "salary": "₹3L - ₹15L/yr",
            "type": "Medical",
            "icon": "💊"
        },
        "Biomedical Engineer": {
            "desc": "Apply engineering to solve medical problems",
            "salary": "₹4L - ₹20L/yr",
            "type": "Engineering",
            "icon": "🔬"
        },
        "CA (Chartered Accountant)": {
            "desc": "Manage finances, audits and tax compliance",
            "salary": "₹7L - ₹40L/yr",
            "type": "Commerce",
            "icon": "📈"
        },
        "Investment Banker": {
            "desc": "Raise capital and advise on mergers",
            "salary": "₹12L - ₹80L/yr",
            "type": "Management",
            "icon": "🏦"
        },
        "Financial Analyst": {
            "desc": "Evaluate investments and financial performance",
            "salary": "₹5L - ₹25L/yr",
            "type": "Commerce",
            "icon": "💹"
        },
        "UI/UX Designer": {
            "desc": "Design intuitive digital experiences",
            "salary": "₹4L - ₹22L/yr",
            "type": "Design",
            "icon": "🎨"
        },
        "Graphic Designer": {
            "desc": "Create visual content for brands and media",
            "salary": "₹3L - ₹15L/yr",
            "type": "Design",
            "icon": "✏️"
        },
        "Architect": {
            "desc": "Design buildings and urban spaces",
            "salary": "₹4L - ₹20L/yr",
            "type": "Engineering",
            "icon": "🏛️"
        },
        "Lawyer": {
            "desc": "Represent clients in legal proceedings",
            "salary": "₹5L - ₹50L/yr",
            "type": "Law",
            "icon": "⚖️"
        },
        "Legal Consultant": {
            "desc": "Provide expert legal advice to organizations",
            "salary": "₹6L - ₹30L/yr",
            "type": "Law",
            "icon": "📜"
        },
        "Professor": {
            "desc": "Teach and conduct research at universities",
            "salary": "₹5L - ₹20L/yr",
            "type": "Arts",
            "icon": "📚"
        },
        "Educational Consultant": {
            "desc": "Guide students and institutions on learning",
            "salary": "₹4L - ₹15L/yr",
            "type": "Arts",
            "icon": "🎓"
        },
        "Journalist": {
            "desc": "Report news and investigate stories",
            "salary": "₹3L - ₹18L/yr",
            "type": "Arts",
            "icon": "📰"
        },
        "Author": {
            "desc": "Write books, scripts and creative content",
            "salary": "₹2L - ₹30L/yr",
            "type": "Arts",
            "icon": "✍️"
        },
        "Sports Coach": {
            "desc": "Train athletes and manage sports teams",
            "salary": "₹3L - ₹20L/yr",
            "type": "Arts",
            "icon": "🏅"
        },
        "Music Producer": {
            "desc": "Create and produce music for artists",
            "salary": "₹3L - ₹25L/yr",
            "type": "Arts",
            "icon": "🎵"
        },
        "Psychologist": {
            "desc": "Study human behavior and treat mental health",
            "salary": "₹4L - ₹20L/yr",
            "type": "Arts",
            "icon": "🧠"
        },
        "Social Worker": {
            "desc": "Support individuals and communities in need",
            "salary": "₹3L - ₹12L/yr",
            "type": "Arts",
            "icon": "🤝"
        },
        "Business Analyst": {
            "desc": "Bridge business needs with technology solutions",
            "salary": "₹5L - ₹25L/yr",
            "type": "Management",
            "icon": "📋"
        },
        "Digital Marketer": {
            "desc": "Grow brands through online channels",
            "salary": "₹3L - ₹18L/yr",
            "type": "Management",
            "icon": "📱"
        },
        "Environmental Scientist": {
            "desc": "Study and protect natural ecosystems",
            "salary": "₹4L - ₹18L/yr",
            "type": "Engineering",
            "icon": "🌿"
        },
        "Agricultural Scientist": {
            "desc": "Improve farming techniques and crop yields",
            "salary": "₹3L - ₹15L/yr",
            "type": "Engineering",
            "icon": "🌾"
        }
    }

    # Rule-based matching
    if math >= 85 and any(i in interests for i in ["Technology", "Engineering"]):
        careers.extend(["Software Engineer", "Data Scientist", "Robotics Engineer"])
    
    if science >= 85 and "Medicine" in interests:
        careers.extend(["MBBS Doctor", "Pharmacist", "Biomedical Engineer"])
    
    if math >= 75 and any(i in interests for i in ["Finance", "Business"]):
        careers.extend(["CA (Chartered Accountant)", "Investment Banker", "Financial Analyst"])
    
    if "Design/Art" in interests:
        careers.extend(["UI/UX Designer", "Graphic Designer", "Architect"])
    
    if "Law" in interests:
        careers.extend(["Lawyer", "Legal Consultant"])
    
    if "Teaching" in interests:
        careers.extend(["Professor", "Educational Consultant"])
    
    if "Writing" in interests:
        careers.extend(["Journalist", "Author"])
    
    if "Sports" in interests:
        careers.append("Sports Coach")
    
    if "Music" in interests:
        careers.append("Music Producer")
    
    if "Psychology" in interests:
        careers.append("Psychologist")
    
    if "Environment" in interests:
        careers.append("Environmental Scientist")
    
    if "Agriculture" in interests:
        careers.append("Agricultural Scientist")
    
    if stream == "Commerce":
        careers.extend(["CA (Chartered Accountant)", "Financial Analyst", "Business Analyst"])
    
    if stream == "Arts":
        careers.extend(["Psychologist", "Social Worker", "Journalist"])

    # Remove duplicates, keep order
    seen = set()
    unique = []
    for c in careers:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    
    # Fallback if nothing matched
    if not unique:
        unique = ["Business Analyst", "Digital Marketer", "Software Engineer"]
    
    # Build response with college type for filtering
    result = []
    for i, name in enumerate(unique[:8]):
        data = CAREER_DATA.get(name, {
            "desc": "Explore this growing career path",
            "salary": "₹4L - ₹20L/yr",
            "type": "Engineering",
            "icon": "🎯"
        })
        result.append({
            "name": name,
            "description": data["desc"],
            "salary": data["salary"],
            "college_type": data["type"],
            "icon": data["icon"],
            "recommended": i == 0  # first one is top recommended
        })
    
    return result

@careers_bp.route('/api/careers/suggest', methods=['GET'])
def suggest_careers():
    user_id = request.args.get('user_id') or session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "User ID required"}), 400
        
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"success": False, "message": "Profile not found"}), 404
        
    result = get_suggestions(profile)
    return jsonify({
        "success": True,
        "careers": result
    })
