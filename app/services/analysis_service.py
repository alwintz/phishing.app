from ml.predictor import predict_email
from database.database import save_analysis
from database.database import count_phishing_attempts
from database.database import count_all_analyses


def analyze_email(email_text: str):

    result = predict_email(email_text)

    save_analysis(email_text, result)

    result["total_phishing_attempts"] = count_phishing_attempts()
    result["total_emails_analyzed"] = count_all_analyses()

    return result