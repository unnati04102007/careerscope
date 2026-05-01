import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
import difflib
import json

# Try to import NLTK but make it optional since we can work without stemming
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    _stemmer = PorterStemmer()
    _stop_words = set(stopwords.words('english'))
    NLTK_AVAILABLE = True
except:
    NLTK_AVAILABLE = False
    _stemmer = None
    _stop_words = set()

# Load NLP Models (non-critical for basic operation)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHATBOT_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'chatbot'))

tfidf_vectorizer = None
tfidf_matrix = None
college_data = None
NLP_READY = False

try:
    tfidf_pkl_path = os.path.join(CHATBOT_DIR, 'tfidf_model.pkl')
    matrix_pkl_path = os.path.join(CHATBOT_DIR, 'tfidf_matrix.pkl')
    college_csv_path = os.path.join(CHATBOT_DIR, 'college_data_cleaned.csv')
    
    if os.path.exists(tfidf_pkl_path) and os.path.exists(matrix_pkl_path):
        with open(tfidf_pkl_path, 'rb') as f:
            tfidf_vectorizer = pickle.load(f)
        with open(matrix_pkl_path, 'rb') as f:
            tfidf_matrix = pickle.load(f)
        
        if os.path.exists(college_csv_path):
            college_data = pd.read_csv(college_csv_path)
            NLP_READY = True
        else:
            print(f"College data CSV not found at {college_csv_path}")
    else:
        print(f"TF-IDF model files not found at {CHATBOT_DIR}")
except Exception as e:
    print(f"Warning: NLP models not loaded - {e}. Chatbot will use rule-based responses only.")

def advanced_clean(text: str) -> str:
    """Clean and preprocess text"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    
    if NLTK_AVAILABLE and _stemmer:
        tokens = [_stemmer.stem(t) for t in tokens if t not in _stop_words and len(t) > 1]
    else:
        tokens = [t for t in tokens if len(t) > 1]
    
    return " ".join(tokens)

def get_career_suggestions_from_profile(user_profile=None):
    """Generate career suggestions based on user profile"""
    if not user_profile:
        return None
    
    interests = user_profile.get('interests', [])
    math = user_profile.get('math_score', 0)
    science = user_profile.get('science_score', 0)
    stream = user_profile.get('stream', '')
    
    suggestions = []
    
    if math >= 85 and ('Technology' in interests or 'Engineering' in interests):
        suggestions.extend(['Software Engineer', 'Data Scientist', 'Robotics Engineer'])
    
    if science >= 85 and 'Medicine' in interests:
        suggestions.extend(['MBBS Doctor', 'Pharmacist', 'Biomedical Engineer'])
    
    if 'Design/Art' in interests:
        suggestions.extend(['UI/UX Designer', 'Graphic Designer', 'Architect'])
    
    if 'Law' in interests:
        suggestions.extend(['Lawyer', 'Legal Consultant'])
    
    if 'Teaching' in interests:
        suggestions.extend(['Professor', 'Teacher'])
    
    if stream == 'Commerce':
        suggestions.extend(['Chartered Accountant (CA)', 'Business Analyst'])
    
    return list(set(suggestions))[:3] if suggestions else None

def get_chatbot_response(message: str, user_id=None, user_profile=None) -> str:
    """
    Main chatbot response function.
    
    Args:
        message: User message
        user_id: User ID (optional)
        user_profile: User profile dict with interests, marks, stream (optional)
    
    Returns:
        Response string
    """
    msg = message.lower().strip()
    
    if not msg:
        return "Please ask me something! 😊"
    
    # 1. Greeting intents
    if any(x in msg for x in ['hi', 'hello', 'hey', 'namaste', 'howdy', 'sup']):
        return (
            "Hello! 👋 I'm your CareerScope assistant. I'm here to help you explore careers and colleges. "
            "You can ask me about:\n"
            "• Specific colleges and universities\n"
            "• Career paths and salaries\n"
            "• Entrance exams and cutoffs\n"
            "• What career suits your interests\n\n"
            "What would you like to know?"
        )
    
    # 2. Help/Info
    if any(x in msg for x in ['help', 'what can you do', 'how does this work', 'guide']):
        return (
            "I can help you with:\n\n"
            "💼 **Careers** - Ask about different professions, required skills, and salaries\n"
            "🎓 **Colleges** - Find and learn about universities in India\n"
            "📚 **Exams** - Information about JEE, NEET, CAT, and other entrance exams\n"
            "💡 **Recommendations** - Get personalized career suggestions based on your profile\n\n"
            "Try asking: 'Tell me about software engineering' or 'Which colleges are best for medical?'"
        )
    
    # 3. Career/Job inquiry
    if any(x in msg for x in ['career', 'job', 'profession', 'what should i do', 'suggest a career']):
        if user_profile:
            suggestions = get_career_suggestions_from_profile(user_profile)
            if suggestions:
                career_text = '\n• '.join(suggestions)
                return f"Based on your profile, here are some great career options for you:\n\n• {career_text}\n\nWould you like to know more about any of these?"
        
        return (
            "There are many exciting career paths! Here are some popular options:\n\n"
            "🖥️ **Tech Careers**: Software Engineer, Data Scientist, AI Engineer, Web Developer\n"
            "🏥 **Medical**: Doctor (MBBS), Pharmacist, Dentist, Nurse\n"
            "⚖️ **Law**: Lawyer, Judge, Legal Consultant\n"
            "💼 **Business**: CA, Business Analyst, Investment Banker\n"
            "🎨 **Creative**: Designer, Architect, Content Creator\n\n"
            "Complete your profile for personalized recommendations!"
        )
    
    # 4. Salary inquiry
    if any(x in msg for x in ['salary', 'money', 'earn', 'package', 'lpa', 'income']):
        return (
            "💰 **Average Salaries in India (Entry Level):**\n\n"
            "Tech & Engineering:\n"
            "• Software Engineer: ₹8L - ₹20L\n"
            "• Data Scientist: ₹10L - ₹25L\n"
            "• DevOps Engineer: ₹9L - ₹18L\n\n"
            "Medical:\n"
            "• Doctor (MBBS): ₹12L - ₹30L+\n"
            "• Pharmacist: ₹4L - ₹10L\n\n"
            "Finance & Business:\n"
            "• CA: ₹8L - ₹20L\n"
            "• Investment Banker: ₹15L - ₹40L+\n"
            "• Business Analyst: ₹7L - ₹16L\n\n"
            "Creative:\n"
            "• UI/UX Designer: ₹6L - ₹18L\n"
            "• Architect: ₹5L - ₹15L\n\n"
            "Note: Salaries vary by company, location, and experience."
        )
    
    # 5. Exam inquiry
    if any(x in msg for x in ['exam', 'cutoff', 'jee', 'neet', 'cat', 'boards', 'score']):
        return (
            "📝 **Entrance Exams in India:**\n\n"
            "**JEE (Joint Entrance Exam)**\n"
            "• For: Engineering (IITs, NITs)\n"
            "• JEE Main: 120-180 marks (generally)\n"
            "• JEE Advanced: Top 2.5L from Main\n"
            "• Focus on: Physics, Chemistry, Math\n\n"
            "**NEET**\n"
            "• For: Medical programs (MBBS, BDS)\n"
            "• Score: 720 marks total\n"
            "• Cutoff: ~50th percentile for general category\n"
            "• Focus on: Biology, Chemistry, Physics\n\n"
            "**CAT/GMAT**\n"
            "• For: MBA programs\n"
            "• Requires: Graduation\n"
            "• Typical cutoff: 95-99 percentile for top IIMs\n\n"
            "Want more details about any exam?"
        )
    
    # 6. College search using NLP if available
    if any(x in msg for x in ['college', 'university', 'institute', 'recommend', 'suggest', 'best', 'top']):
        if NLP_READY and tfidf_vectorizer is not None:
            try:
                cleaned_query = advanced_clean(message)
                if cleaned_query:
                    query_vec = tfidf_vectorizer.transform([cleaned_query])
                    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
                    
                    top_indices = np.argsort(scores)[::-1][:3]
                    results = []
                    
                    for idx in top_indices:
                        if idx < len(college_data):
                            score = float(scores[idx])
                            if score > 0.01:
                                row = college_data.iloc[idx]
                                college_name = row.get('College_Name', row.get('name', 'Unknown'))
                                rating = row.get('Rating', row.get('rating', 'N/A'))
                                state = row.get('State', row.get('state', 'N/A'))
                                results.append(f"🎓 **{college_name}** - {state} | Rating: {rating}⭐")
                    
                    if results:
                        response = "Here are some colleges matching your query:\n\n"
                        response += "\n".join(results)
                        response += "\n\nVisit the Colleges page for more details!"
                        return response
            except Exception as e:
                print(f"NLP error: {e}")
        
        return (
            "Popular colleges in India:\n\n"
            "**Engineering**: IIT Bombay, IIT Delhi, NIT Trichy, BITS Pilani\n"
            "**Medical**: AIIMS Delhi, JIPMER, Medical colleges across India\n"
            "**Management**: IIM Ahmedabad, XLRI Jamshedpur, ISB\n"
            "**Arts & Sciences**: St. Xavier's, Hindu College, Miranda House\n"
            "**Law**: NLSIU Bangalore, Symbiosis Law School\n"
            "**Design**: NID Ahmedabad, NIFT Delhi\n\n"
            "Visit the Colleges page to explore with filters!"
        )
    
    # 7. Stream specific advice
    if 'science' in msg or 'engineering' in msg or 'tech' in msg:
        return (
            "🔬 **Science & Engineering Path:**\n\n"
            "Popular Careers: Software Engineer, Doctor, Data Scientist, Robotics Engineer, Architect\n\n"
            "What You Need:\n"
            "• Strong Math & Physics foundation\n"
            "• Problem-solving skills\n"
            "• Logical thinking\n\n"
            "Top Exams: JEE (Engineering), NEET (Medical)\n\n"
            "Top Colleges: IITs, NITs, AIIMS, Medical colleges\n\n"
            "Top Universities: IIT Bombay, IIT Delhi, AIIMS Delhi"
        )
    
    if 'commerce' in msg or 'business' in msg or 'finance' in msg:
        return (
            "💼 **Commerce & Business Path:**\n\n"
            "Popular Careers: CA, Business Analyst, Investment Banker, Financial Analyst, Entrepreneur\n\n"
            "What You Need:\n"
            "• Strong Math & Economics\n"
            "• Analytical skills\n"
            "• Business acumen\n\n"
            "Competitive Exams: CA Final, CAT (for MBA), CFA\n\n"
            "Top Colleges: SRCC Delhi, St. Xavier's, Christ University\n\n"
            "Career Path: Bachelor's → CA/CMA/MBA → Specialization"
        )
    
    if 'arts' in msg or 'humanities' in msg:
        return (
            "🎭 **Arts & Humanities Path:**\n\n"
            "Popular Careers: Psychologist, Social Worker, Journalist, Teacher, Lawyer, Content Creator\n\n"
            "What You Need:\n"
            "• Strong communication skills\n"
            "• Analytical thinking\n"
            "• Creativity\n"
            "• Empathy & human understanding\n\n"
            "Exams: UPSC, Law entrance, Media entrance\n\n"
            "Top Colleges: Presidency University, Miranda House, Hindu College"
        )
    
    # 8. Default response
    return (
        "I'm here to help! 🤖 You can ask me about:\n\n"
        "• Careers (e.g., 'Tell me about software engineering')\n"
        "• Colleges (e.g., 'What are the best engineering colleges?')\n"
        "• Exams (e.g., 'What's the JEE cutoff?')\n"
        "• Salaries (e.g., 'How much do data scientists earn?')\n"
        "• Your stream (e.g., 'I'm in commerce stream, what careers?')\n\n"
        "What would you like to explore?"
    )

