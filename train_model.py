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
from sklearn.utils import resample
import re
import os
from data_preprocessing import preprocess_text

# Set NLTK data path
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if not os.path.exists(nltk_data_path):
    raise FileNotFoundError(f"NLTK data not found at {nltk_data_path}. Please ensure nltk_data folder is in the project root.")
nltk.data.path = [nltk_data_path] + nltk.data.path

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


# Load and preprocess data
data = pd.read_csv('reviews.csv', encoding='ISO-8859-1', low_memory=False)
data['cleaned_review'] = data['Review'].apply(preprocess_text)
sentiment_map = {'negative': 0, 'neutral': 1, 'positive': 2}
data['Sentiment'] = data['Sentiment'].str.lower().map(sentiment_map).fillna(-1)
data = data[data['Sentiment'] != -1]
print("Initial sentiment distribution:", data['Sentiment'].value_counts())

# Balance dataset
min_count = min(data['Sentiment'].value_counts())
data_positive = data[data['Sentiment'] == 2].sample(n=min_count, random_state=42)
data_negative = data[data['Sentiment'] == 0].sample(n=min_count, random_state=42)
data_neutral = data[data['Sentiment'] == 1].sample(n=min_count, random_state=42)
data_balanced = pd.concat([data_positive, data_negative, data_neutral])
print("Balanced sentiment distribution:", data_balanced['Sentiment'].value_counts())

# Vectorize and train
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data_balanced['cleaned_review']).toarray()
y = data_balanced['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, 'sentiment_model_new.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer_new.pkl')
print("Model and vectorizer saved successfully.")