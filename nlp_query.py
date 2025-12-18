from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

commands = [
    "show total sales",
    "show total expenses",
    "show profit",
    "sales chart",
    "expense chart",
    "profit chart",
]

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(commands)

def interpret(query: str) -> str:
    q_vec = vectorizer.transform([query])
    similarity = cosine_similarity(q_vec, matrix).flatten()
    idx = similarity.argmax()
    return commands[idx]
