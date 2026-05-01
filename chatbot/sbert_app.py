import os
import re
import pickle
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app)

print("Loading SBERT model...")
# Loads the lightweight, fast miniLM model as requested
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Loading embeddings.pkl...")
college_data = []
corpus_embeddings = None

try:
    # Assuming embeddings.pkl contains a list of dictionaries:
    # [{'college_name': 'IIT Bombay', 'snippet': 'Great coding culture...', 'embedding': [...]}, ...]
    with open('embeddings.pkl', 'rb') as f:
        college_data = pickle.load(f)
    
    # Extract embeddings into a single tensor for efficient comparison
    embeddings_list = [item['embedding'] for item in college_data]
    if embeddings_list:
        corpus_embeddings = torch.tensor(embeddings_list)
        print(f"Successfully loaded {len(college_data)} embeddings.")
    else:
        print("Embeddings list is empty.")
except FileNotFoundError:
    print("Warning: embeddings.pkl not found. Please ensure it is in the same directory.")
except Exception as e:
    print(f"Error loading embeddings: {e}")

def clean_text(text):
    """Clean user query for better matching."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return " ".join(text.split())

@app.route('/api/chat', methods=['POST'])
def chat():
    if not college_data or corpus_embeddings is None:
        return jsonify({
            "error": "Embeddings not loaded. Please generate embeddings.pkl first."
        }), 500
        
    data = request.json
    user_query = data.get('user_query', '').strip()
    
    if not user_query:
        return jsonify({"error": "No user_query provided"}), 400
        
    # Clean and encode the query
    cleaned_query = clean_text(user_query)
    query_embedding = model.encode(cleaned_query, convert_to_tensor=True)
    
    # Compute cosine similarities between query and all college embeddings
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    
    # Get the top 3 matches
    top_k = min(3, len(college_data))
    top_results = torch.topk(cos_scores, k=top_k)
    
    results = []
    for score, idx in zip(top_results[0], top_results[1]):
        idx = int(idx)
        item = college_data[idx]
        results.append({
            "college_name": item.get('college_name', 'Unknown College'),
            "match_score": round(float(score) * 100, 2), # Convert to percentage
            "snippet": item.get('snippet', 'No review available.')
        })
        
    return jsonify({
        "query": user_query,
        "top_matches": results
    })

if __name__ == '__main__':
    # Running on 5001 to avoid clashing with the main app on 5000
    app.run(debug=True, port=5001)
