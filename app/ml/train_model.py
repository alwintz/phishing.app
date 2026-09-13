import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


CSV_PATH = "data/email_phishing_text.csv"
MODEL_PATH = "ml/phishing_model.pkl"
VECTORIZER_PATH = "ml/vectorizer.pkl"


def train_model():

    print("Loading dataset...")

    # Load raw email text and known labels
    df = pd.read_csv(CSV_PATH)

    print(df.head())

    # Raw email text
    X = df["email_text"]

    # 0 = legitimate
    # 1 = phishing
    y = df["label"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.5,
        random_state=42,
        stratify=y
    )

    # Convert email text into numerical TF-IDF features
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)

    # Important:
    # transform() is used on test data.
    # We do NOT fit the vectorizer again.
    X_test_tfidf = vectorizer.transform(X_test)

    # Create Random Forest classifier
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    print("Training model...")

    # Train Random Forest on TF-IDF numerical features
    model.fit(X_train_tfidf, y_train)

    # Predict unseen test data
    y_pred = model.predict(X_test_tfidf)

    # Basic model evaluation
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model Accuracy: {accuracy:.2%}")

    # Save model and fitted TF-IDF vectorizer
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Model saved successfully")
    print("TF-IDF vectorizer saved successfully")


if __name__ == "__main__":
    train_model()