import joblib

from ml.feature_extractor import extract_features


# Load the trained model saved by train_model.py
MODEL_PATH = "ml/phishing_model.pkl"
model = joblib.load(MODEL_PATH)


def predict_email(email_text: str):
    """
    Receives raw email text, converts it into numeric features,
    then uses the trained ML model to predict phishing or legitimate.
    """

    # Convert email text into the same 8 features used during training
    features = extract_features(email_text)

    # Predict class: 0 = legitimate, 1 = phishing
    prediction = model.predict([features])[0]

    # Get confidence score from model probabilities
    probabilities = model.predict_proba([features])[0]
    confidence = max(probabilities)

    # Business rule:
    # If the email contains at least one link and many urgent words,
    # classify it as phishing even if the ML model says legitimate.
    if prediction == 0 and features[3] >= 1 and features[7] >= 2:
        prediction = 1
        confidence = max(confidence, 0.75)

    return {
        "prediction": "phishing" if prediction == 1 else "legitimate",
        "label": int(prediction),
        "confidence": round(float(confidence), 2),
        "features": {
            "num_words": features[0],
            "num_unique_words": features[1],
            "num_stopwords": features[2],
            "num_links": features[3],
            "num_unique_domains": features[4],
            "num_email_addresses": features[5],
            "num_spelling_errors": features[6],
            "num_urgent_keywords": features[7],
        }
    }