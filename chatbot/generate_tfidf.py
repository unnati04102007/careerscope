import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os

print("Downloading stopwords...")
nltk.download('stopwords', quiet=True)

_stemmer = PorterStemmer()
_stop_words = set(stopwords.words('english'))

def advanced_clean(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    tokens = [_stemmer.stem(t) for t in tokens if t not in _stop_words and len(t) > 1]
    return " ".join(tokens)

print("Loading dataset...")
data_path = '../backend/data/tfidf_college_reviews.xlsx'
if not os.path.exists(data_path):
    print(f"File not found: {data_path}")
    exit(1)

df = pd.read_excel(data_path)
df = df.dropna(subset=['review']).copy()

print("Cleaning reviews...")
df['processed_text'] = df['review'].apply(advanced_clean)

# Group by college
df_grouped = (
    df.groupby('college')['processed_text']
    .apply(' '.join)
    .reset_index()
)

df_grouped = df_grouped[df_grouped['processed_text'].str.strip() != ''].copy()
df_grouped.reset_index(drop=True, inplace=True)

# Generate pseudo data for Fees, State, Rating since tfidf_college_reviews.xlsx might not have them
# We'll extract ratings if available, else mock them
print("Preparing college_data_cleaned.csv...")
college_data = pd.DataFrame()
college_data['College_Name'] = df_grouped['college']
college_data['State'] = 'Unknown' # Can be updated from main DB later
college_data['Fees'] = 'Unknown' # Can be updated from main DB later

# Calculate avg rating
ratings = []
for col in df_grouped['college']:
    col_rows = df[df['college'] == col]
    avg = pd.to_numeric(col_rows['rating'], errors='coerce').mean()
    ratings.append(round(float(avg), 1) if pd.notna(avg) else 'N/A')
college_data['Rating'] = ratings

college_data.to_csv('college_data_cleaned.csv', index=False)

print("Training TF-IDF...")
tfidf_vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
tfidf_matrix = tfidf_vectorizer.fit_transform(df_grouped['processed_text'])

print("Saving models...")
with open('tfidf_model.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)

with open('tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)

print("Done! Model and data generated successfully.")
