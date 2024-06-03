import requests
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import ServicesNames
from services.registry_client import get_service


def vectorize_text(vectorizer: TfidfVectorizer, text: str):
    vector = vectorizer.transform([text])
    return vector.toarray().tolist()


def process_text(text: str) -> str:
    url = get_service(ServicesNames.text_processing)
    data = {
        'text': text
    }
    result = requests.post(url=url, json=data)
    return result.json()['result']
