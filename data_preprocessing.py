import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from generative import generate_suggestion
from sklearn.utils import resample
import re
import os


nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if not os.path.exists(nltk_data_path):
    raise FileNotFoundError(f"NLTK data not found at {nltk_data_path}. Please ensure nltk_data folder is in the project root.")
nltk.data.path = [nltk_data_path] + nltk.data.path
# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    # Handle non-string values
    if not isinstance(text, str) or pd.isna(text):
        return ""
    # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)
