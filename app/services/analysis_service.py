from ml.predictor import predict_email
from database.database import save_analysis
from database.database import count_phishing_attempts
from database.database import count_all_analyses


def analyze_email(email_text: str):

    result = predict_email(email_text)

    save_analysis(email_text, result)

    result["total_phishing_attempts"] = count_phishing_attempts()
    result["total_emails_analyzed"] = count_all_analyses()

    # Show analysis in console
    print("\n=== PHISHING EMAIL ANALYSIS ===")
    print("Email:", email_text)
    print("Prediction:", result["prediction"])
    print("Confidence:", result["confidence"])
    print("Risk Level:", result["risk_level"])
    print("Features:", result["features"])
    print("Total Phishing Attempts:", result["total_phishing_attempts"])
    print("Total Emails Analyzed:", result["total_emails_analyzed"])
    print("===============================\n")

    return result