import streamlit as st
import requests

st.title("Sentiment Analysis Frontend")

# Input reviews text from user
reviews = st.text_area("Enter reviews (separate by commas):")

if st.button("Analyze Reviews"):
    if not reviews.strip():
        st.warning("Please enter some reviews.")
    else:
        # Change the URL to your deployed Flask backend or local one
        FLASK_API_URL = "http://localhost:5000/analyze"
        
        try:
            response = requests.post(FLASK_API_URL, json={"reviews": reviews})
            if response.status_code == 200:
                results = response.json()
                for res in results:
                    st.write(f"Review: {res['review']}")
                    st.write(f"Sentiment: {res['sentiment']}")
                    st.write(f"Suggestion: {res['suggestion']}")
                    st.markdown("---")
            else:
                st.error(f"API error: {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
