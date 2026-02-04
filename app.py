from flask import Flask, request, render_template, redirect, url_for
import joblib
import os
import pandas as pd
import json
import uuid
from datetime import datetime
# Import your scraper
from amazon_scraper import get_amazon_data 

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

HISTORY_FILE = 'history.json'
model = None
vectorizer = None

def load_models():
    global model, vectorizer
    if model is None or vectorizer is None:
        model = joblib.load('sentiment_model_new.pkl')
        vectorizer = joblib.load('tfidf_vectorizer_new.pkl')

def load_history_data():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history_entry(entry):
    history = load_history_data()
    # Insert at the beginning (newest first)
    history.insert(0, entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def process_reviews_in_chunks(review_list, chunk_size=1000):
    from data_preprocessing import preprocess_text
    cleaned_reviews = [preprocess_text(r) for r in review_list]
    for i in range(0, len(cleaned_reviews), chunk_size):
        chunk = cleaned_reviews[i:i + chunk_size]
        yield vectorizer.transform(chunk).toarray()

@app.route('/', methods=['GET', 'POST'])
def home():
    result_data = None
    product_info = None
    error = None
    summary = None 
    
    # Load history for the sidebar
    history = load_history_data()

    if request.method == 'POST':
        product_url = request.form.get('product_url')
        reviews_input = request.form.get('reviews', '').strip()
        file = request.files.get('file')
        
        review_list = []
        entry_type = 'text'
        entry_title = 'Manual Analysis'

        try:
            # 1. HANDLE INPUTS
            if product_url:
                entry_type = 'url'
                scraped_data = get_amazon_data(product_url)
                if not scraped_data['reviews']:
                    error = "No reviews found. Amazon may be blocking requests."
                else:
                    review_list = scraped_data['reviews']
                    product_info = {
                        "title": scraped_data['title'],
                        "image": scraped_data['image'],
                        "description": scraped_data['description'],
                        "url": product_url  # <--- ADDED THIS TO SAVE URL
                    }
                    entry_title = scraped_data['title']
            elif file and file.filename:
                entry_type = 'file'
                entry_title = file.filename
                if file.filename.endswith('.csv'):
                     df = pd.read_csv(file, encoding='ISO-8859-1', nrows=10000)
                     col_name = next((c for c in ['Review', 'review', 'Reviews', 'reviews', 'Text', 'text'] if c in df.columns), None)
                     if col_name:
                        review_list = df[col_name].dropna().astype(str).tolist()
                     else:
                        error = "CSV must contain a 'Review' column."
                elif file.filename.endswith('.txt'):
                     content = file.read().decode('utf-8', errors='ignore')
                     review_list = [line.strip() for line in content.splitlines() if line.strip()]
            elif reviews_input:
                entry_type = 'text'
                entry_title = f"Manual Text ({len(reviews_input.split())} words)"
                review_list = [line.strip() for line in reviews_input.split('\n') if line.strip()]

            # 2. PROCESS REVIEWS
            if review_list and not error:
                load_models()
                from generative import generate_suggestion
                
                sentiments = []
                for chunk_predictions in process_reviews_in_chunks(review_list):
                    sentiments.extend(model.predict(chunk_predictions))
                
                suggestions = [generate_suggestion(sent) for sent in sentiments]
                
                result_data = [{'review': rev, 'sentiment': int(sent), 'suggestion': sugg} 
                           for rev, sent, sugg in zip(review_list, sentiments, suggestions)]
                
                summary = {
                    'positive': sentiments.count(2),
                    'neutral': sentiments.count(1),
                    'negative': sentiments.count(0),
                    'total': len(sentiments)
                }

                # Determine Dominant Sentiment
                dom_sent = "Neutral"
                if summary['positive'] > summary['negative'] and summary['positive'] > summary['neutral']:
                    dom_sent = "Positive"
                elif summary['negative'] > summary['positive'] and summary['negative'] > summary['neutral']:
                    dom_sent = "Negative"

                # Save to History
                history_entry = {
                    'id': str(uuid.uuid4()),
                    'timestamp': datetime.now().strftime("%b %d, %Y %I:%M %p"),
                    'type': entry_type,
                    'title': entry_title,
                    'dominant_sentiment': dom_sent,
                    'summary': summary,
                    'product': product_info,
                    'result': result_data
                }
                save_history_entry(history_entry)
                
                # Reload history to include the new item immediately
                history = load_history_data()

        except Exception as e:
            error = f"System Error: {str(e)}"

    return render_template('index.html', error=error, result=result_data, product=product_info, summary=summary, history=history)

@app.route('/history/<item_id>')
def view_history(item_id):
    history = load_history_data()
    # Find the specific entry
    entry = next((item for item in history if item['id'] == item_id), None)
    
    if entry:
        # Render the homepage but with the historical data loaded
        return render_template('index.html', 
                             result=entry['result'], 
                             product=entry.get('product'), 
                             summary=entry['summary'], 
                             history=history,
                             error=None)
    return redirect(url_for('home'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)