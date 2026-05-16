# 🤖 SentimentAI: Amazon Product Intelligence Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SentimentAI** is a robust, full-stack Product Intelligence Dashboard designed to transform raw Amazon customer feedback into actionable business insights. Using advanced Natural Language Processing (NLP) and custom web scraping automation, it provides a comprehensive view of market sentiment.

---

## 🌟 Key Features

*   **🔍 Advanced Scraping Engine:** Employs Selenium with a "Smart Scroll" algorithm to bypass anti-bot measures and capture lazy-loaded reviews.
*   **📊 Dynamic Sentiment Analytics:** Interactive Donut Charts (via Chart.js) visualizing Positive, Neutral, and Negative distributions.
*   **💡 AI-Driven Insights:** Automatically generates strategic business advice based on analyzed sentiment trends.
*   **📂 Multi-Input Support:** Analyze data from direct Amazon URLs, uploaded CSV/TXT files, or manual text entry.
*   **🌓 Premium UX/UI:** Glassmorphic dashboard design with a persistent Dark/Light mode toggle.
*   **📜 Analysis History:** Local persistent storage for easy retrieval of previous product analyses.

---

## 🚀 Technical Methodology

### Machine Learning Pipeline
- **Preprocessing:** NLTK-powered cleaning (Tokenization, Stop-word removal, Lemmatization).
- **Vectorization:** TF-IDF (Term Frequency-Inverse Document Frequency) for feature extraction.
- **Classification:** Random Forest Classifier for high-accuracy sentiment prediction.

### Scraping Strategy
To handle Amazon's dynamic content, we built a custom automation wrapper using **Selenium** and **ChromeDriver**. The script mimics human browsing behavior to trigger JavaScript events required for loading reviews that standard scrapers miss.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Chrome (latest version)
- Git (optional)

### Step-by-Step Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/muhammadumarafzaal/sentiment-analysis.git
    cd sentiment-analysis
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLTK Data**
    Run the following in a Python shell:
    ```python
    import nltk
    nltk.download(['stopwords', 'wordnet', 'omw-1.4'])
    ```

---

## 🖥️ Usage Guide

1.  **Start the Application**
    ```bash
    python app.py
    ```
2.  **Access the Dashboard**
    Open your browser and navigate to `http://127.0.0.1:5000`.
3.  **Run Analysis**
    - **URL Tab:** Paste an Amazon product link and wait for the automated scraper.
    - **Manual/File Tab:** Upload datasets or type text directly for instant classification.
4.  **View History**
    Access the **History** tab in the sidebar to review all past analysis results.

---

## 📂 Project Architecture

```text
sentiment-analysis/
├── app.py                  # Main Flask application & API routes
├── amazon_scraper.py       # Selenium-based scraping logic
├── data_preprocessing.py   # Text cleaning & NLP pipeline
├── generative.py           # Business insight generation
├── train_model.py          # ML training & serialization
├── requirements.txt        # Project dependencies
├── static/                 # CSS (Glassmorphism) & JS
└── templates/              # Jinja2 HTML templates
```

---

## 👥 Contributors

- **Umar Afzal** (23F-3106) 


---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Developed by [muhammadumarafzaal](https://github.com/muhammadumarafzaal)**
