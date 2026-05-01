"""
nlp_recommender.py
------------------
NLP-based college recommendation engine using TF-IDF + Cosine Similarity
trained on real student college reviews.

Dataset: backend/data/tfidf_college_reviews.xlsx
Model  : TfidfVectorizer(max_features=500, ngram_range=(1,2))
"""

import os
import re

import nltk
nltk.download('stopwords', quiet=True)

import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
_stemmer = PorterStemmer()
_stop_words = set(stopwords.words('english'))

# Module-level handles — populated in _load_model()
tfidf_vectorizer: TfidfVectorizer = None
tfidf_matrix_grouped = None
df_grouped: pd.DataFrame = None
df: pd.DataFrame = None
_model_ready: bool = False


# ---------------------------------------------------------------------------
# Text cleaning (must match the preprocessing used during training)
# ---------------------------------------------------------------------------
def advanced_clean(text: str) -> str:
    """
    Lowercase → strip special chars → tokenise → remove stopwords → stem.
    Identical to the function used when building the training dataset.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    tokens = [_stemmer.stem(t) for t in tokens if t not in _stop_words and len(t) > 1]
    return " ".join(tokens)


# ---------------------------------------------------------------------------
# Load dataset and train TF-IDF model at import time
# ---------------------------------------------------------------------------
def _load_model():
    global tfidf_vectorizer, tfidf_matrix_grouped, df_grouped, df, _model_ready

    try:
        # Resolve path relative to this file: chatbot/ → project root → backend/data/
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, '..', 'backend', 'data', 'tfidf_college_reviews.xlsx')
        data_path = os.path.normpath(data_path)

        if not os.path.exists(data_path):
            print(f"⚠️  NLP model: dataset not found at {data_path}")
            return

        # Load
        df = pd.read_excel(data_path)

        # Drop rows with missing reviews
        df = df.dropna(subset=['review']).copy()

        # Apply cleaning to produce / overwrite processed_text
        df['processed_text'] = df['review'].apply(advanced_clean)

        # Group by college — concatenate all processed reviews into one document
        df_grouped = (
            df.groupby('college')['processed_text']
            .apply(' '.join)
            .reset_index()
        )

        # Ensure no empty documents
        df_grouped = df_grouped[df_grouped['processed_text'].str.strip() != ''].copy()
        df_grouped.reset_index(drop=True, inplace=True)

        # Train TF-IDF (same hyper-params as training)
        tfidf_vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        tfidf_matrix_grouped = tfidf_vectorizer.fit_transform(df_grouped['processed_text'])

        _model_ready = True
        print(
            f"[NLP] Model ready: {len(df_grouped)} colleges, "
            f"{len(df)} reviews loaded"
        )

    except Exception as exc:
        print(f"[NLP] WARNING: model failed to load: {exc}")
        _model_ready = False


# Run at import
_load_model()


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def is_review_query(user_message: str) -> bool:
    """
    Returns True when the user's message suggests they want experience /
    culture / review-based college recommendations.
    """
    KEYWORDS = [
        'placement', 'culture', 'hostel', 'campus', 'faculty', 'atmosphere',
        'coding', 'environment', 'life', 'experience', 'fest', 'food',
        'infrastructure', 'review', 'kaisa hai', 'kaisi hai', 'how is',
        'what is it like', 'recommend', 'suggest', 'best for', 'good for',
        'known for',
    ]
    lower = user_message.lower()
    return any(kw in lower for kw in KEYWORDS)


def get_nlp_recommendations(user_query: str, top_n: int = 3) -> list:
    """
    Match *user_query* against grouped college reviews using TF-IDF cosine
    similarity and return the top colleges.

    Returns
    -------
    list of dict:
        {
            'college'      : str,
            'match_score'  : float,   # cosine similarity (0–1)
            'avg_rating'   : float,
            'highlight'    : str,     # first 150 chars of best review
            'total_reviews': int,
        }
    Empty list if the model is not ready or no results exceed the threshold.
    """
    if not _model_ready or df_grouped is None:
        return []

    try:
        # Clean query the same way as documents
        cleaned_query = advanced_clean(user_query)
        if not cleaned_query.strip():
            return []

        # Vectorise query
        query_vec = tfidf_vectorizer.transform([cleaned_query])

        # Cosine similarity against all college groups
        scores = cosine_similarity(query_vec, tfidf_matrix_grouped).flatten()

        # Sort descending
        ranked_indices = np.argsort(scores)[::-1]

        results = []
        for idx in ranked_indices[:top_n * 2]:          # fetch extra to allow filtering
            score = float(scores[idx])
            if score <= 0.05:                            # skip irrelevant
                continue

            college_name = df_grouped.iloc[idx]['college']

            # Rows in original df for this college
            college_rows = df[df['college'] == college_name]

            # Average rating (coerce to numeric safely)
            avg_rating = pd.to_numeric(college_rows['rating'], errors='coerce').mean()
            avg_rating = round(float(avg_rating), 1) if not np.isnan(avg_rating) else 0.0

            # Best review = row with highest numeric rating
            college_rows_sorted = college_rows.copy()
            college_rows_sorted['_num_rating'] = pd.to_numeric(
                college_rows_sorted['rating'], errors='coerce'
            )
            best_row = college_rows_sorted.sort_values('_num_rating', ascending=False).iloc[0]
            highlight = str(best_row['review'])[:150].strip()

            results.append({
                'college'      : college_name,
                'match_score'  : score,
                'avg_rating'   : avg_rating,
                'highlight'    : highlight,
                'total_reviews': len(college_rows),
            })

            if len(results) >= top_n:
                break

        return results

    except Exception as exc:
        print(f"[NLP] WARNING: get_nlp_recommendations error: {exc}")
        return []
