import re
from urllib.parse import urlparse


URGENT_WORDS = [
    "urgent",
    "verify",
    "verification",
    "account",
    "password",
    "login",
    "bank",
    "security",
    "click",
    "immediately",
    "suspended",
    "limited",
    "confirm",
    "update",
    "payment",
    "expired",
    "risk",
    "warning",
    "blocked",
    "unauthorized",
    "access",
    "restore"
]


STOPWORDS = [
    "the", "is", "are", "a", "an", "to", "for", "of", "and", "or",
    "in", "on", "at", "with", "your", "you", "we", "our", "this",
    "that", "it", "be", "by", "from"
]


def extract_features(email_text: str):
    text = email_text.lower()

    words = re.findall(r"\b\w+\b", text)

    links = re.findall(r"https?://\S+|www\.\S+", text)

    domains = []
    for link in links:
        if not link.startswith("http"):
            link = "http://" + link
        domains.append(urlparse(link).netloc)

    email_addresses = re.findall(
        r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        email_text
    )

    num_urgent_keywords = sum(
        1 for word in words if word in URGENT_WORDS
    )

    num_stopwords = sum(
        1 for word in words if word in STOPWORDS
    )

    return [
        len(words),                 # num_words
        len(set(words)),             # num_unique_words
        num_stopwords,               # num_stopwords
        len(links),                  # num_links
        len(set(domains)),           # num_unique_domains
        len(email_addresses),        # num_email_addresses
        0,                           # num_spelling_errors
        num_urgent_keywords          # num_urgent_keywords
    ]