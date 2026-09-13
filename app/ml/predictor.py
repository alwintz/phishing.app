import joblib

from ml.feature_extractor import extract_features


MODEL_PATH = "ml/phishing_model.pkl"
VECTORIZER_PATH = "ml/vectorizer.pkl"

# Load trained model and fitted TF-IDF vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_email(email_text: str):
    """
    Analyses a new email using the saved TF-IDF vectorizer
    and trained Random Forest model.
    """

    # Convert the new email into the same TF-IDF format
    # that was used during model training
    email_tfidf = vectorizer.transform([email_text])

    # Calculate class probabilities
    probabilities = model.predict_proba(email_tfidf)[0]

    phishing_probability = float(probabilities[1])

    # Extract additional security indicators
    # These are used for display and database storage
    features = extract_features(email_text)

    # Convert phishing probability into risk level
    if phishing_probability >= 0.70:
        prediction = "phishing"
        label = 1
        risk_level = "high"

    elif phishing_probability >= 0.40:
        prediction = "suspicious"
        label = 0
        risk_level = "medium"

    else:
        prediction = "legitimate"
        label = 0
        risk_level = "low"

    return {
        "prediction": prediction,
        "label": label,
        "confidence": round(phishing_probability, 2),
        "risk_level": risk_level,
        "features": {
            "num_words": features[0],
            "num_unique_words": features[1],
            "num_stopwords": features[2],
            "num_links": features[3],
            "num_unique_domains": features[4],
            "num_email_addresses": features[5],
            "num_urgent_keywords": features[6],
        }
    }