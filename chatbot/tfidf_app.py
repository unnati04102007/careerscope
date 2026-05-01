from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

app = Flask(__name__)
CORS(app)

_stemmer = PorterStemmer()
_stop_words = set(stopwords.words('english'))

def advanced_clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    tokens = [_stemmer.stem(t) for t in tokens if t not in _stop_words and len(t) > 1]
    return " ".join(tokens)

print("Loading TF-IDF models and college data...")
try:
    with open('tfidf_model.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
        
    with open('tfidf_matrix.pkl', 'rb') as f:
        tfidf_matrix = pickle.load(f)
        
    college_data = pd.read_csv('college_data_cleaned.csv')
    print("Successfully loaded resources!")
except Exception as e:
    print(f"Error loading files: {e}")
    tfidf_vectorizer, tfidf_matrix, college_data = None, None, None

@app.route('/api/chat', methods=['POST'])
def chat():
    if tfidf_vectorizer is None or tfidf_matrix is None or college_data is None:
        return jsonify({"error": "NLP Models not loaded properly."}), 500
        
    data = request.json
    user_query = data.get('query', '').strip()
    
    if not user_query:
        return jsonify({"error": "Please provide a query."}), 400
        
    cleaned_query = advanced_clean(user_query)
    query_vec = tfidf_vectorizer.transform([cleaned_query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    top_indices = np.argsort(scores)[::-1][:3]
    
    results = []
    for idx in top_indices:
        score = float(scores[idx])
        if score > 0.01:
            row = college_data.iloc[idx]
            results.append({
                "college_name": str(row.get('College_Name', 'Unknown')),
                "match_score": round(score * 100, 1),
                "state": str(row.get('State', 'N/A')),
                "fees": str(row.get('Fees', 'N/A')),
                "rating": str(row.get('Rating', 'N/A'))
            })
            
    return jsonify({
        "query": user_query,
        "top_matches": results
    })

if __name__ == '__main__':
    # Using 5002 to avoid conflicting with anything else running
    app.run(debug=True, port=5002)
