import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


CSV_PATH = "data/email_phishing_data.csv"
MODEL_PATH = "ml/phishing_model.pkl"


def train_model():

    print("Loading dataset...")

    # Load historical phishing and legitimate email data
    df = pd.read_csv(CSV_PATH)

    print(df.head())

    # Select only the columns that will be used as inputs to the model
    X = df[
        [
            "num_words",
            "num_unique_words",
            "num_stopwords",
            "num_links",
            "num_unique_domains",
            "num_email_addresses",
            "num_spelling_errors",
            "num_urgent_keywords"
        ]
    ]

    # Target value:
    # 0 = legitimate email
    # 1 = phishing email
    y = df["label"]

    # Keep 20% of records separate so the model can be tested
    # on data it has never seen before
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Random Forest combines multiple decision trees
    # to improve prediction accuracy and reduce overfitting
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    print("Training model...")

    # Learn phishing patterns from the training dataset
    model.fit(X_train, y_train)

    # Predict classifications for unseen test records
    y_pred = model.predict(X_test)

    # Measure how many emails were classified correctly
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model Accuracy: {accuracy:.2%}")

    # Save trained model so the API can use it later
    # without retraining every time the application starts
    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully")


# Start training when this file is executed directly
if __name__ == "__main__":
    train_model()