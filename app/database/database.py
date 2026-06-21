import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "phishing.db")



def create_table():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            label INTEGER NOT NULL,
            confidence REAL NOT NULL,
            num_words INTEGER,
            num_unique_words INTEGER,
            num_stopwords INTEGER,
            num_links INTEGER,
            num_unique_domains INTEGER,
            num_email_addresses INTEGER,
            num_spelling_errors INTEGER,
            num_urgent_keywords INTEGER
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(email_text: str, result: dict):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    features = result["features"]

    cursor.execute("""
        INSERT INTO analysis_results (
            email_text,
            prediction,
            label,
            confidence,
            num_words,
            num_unique_words,
            num_stopwords,
            num_links,
            num_unique_domains,
            num_email_addresses,
            num_spelling_errors,
            num_urgent_keywords
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email_text,
        result["prediction"],
        result["label"],
        result["confidence"],
        features["num_words"],
        features["num_unique_words"],
        features["num_stopwords"],
        features["num_links"],
        features["num_unique_domains"],
        features["num_email_addresses"],
        features["num_spelling_errors"],
        features["num_urgent_keywords"]
    ))

    connection.commit()
    connection.close()


  


def count_phishing_attempts():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM analysis_results
        WHERE prediction = 'phishing'
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


def count_all_analyses():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM analysis_results
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count