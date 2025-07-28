# model/predict.py

import pickle
from PreProcessing import preprocess
from langdetect import detect

# Load vectorizer and model once
with open("E:/project rough/project/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("E:/project rough/project/logistic_model.pkl", "rb") as f:
    model = pickle.load(f)

# --- Utility functions ---

def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

def clean_and_filter(comments):
    english_comments = [c for c in comments if is_english(c)]
    cleaned = [preprocess(c) for c in english_comments]
    return cleaned, english_comments

# --- Main function to use ---

def predict_sentiments(comments):
    """
    Takes a list of raw comments.
    Returns a list of tuples: (original_comment, sentiment_label)
    """
    cleaned, original = clean_and_filter(comments)
    if not cleaned:
        return []

    X = vectorizer.transform(cleaned)
    preds = model.predict(X)

    # Map numerical predictions to human-readable labels
    label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}

    results = []
    for comment, pred in zip(original, preds):
        sentiment_label = label_map[pred]
        results.append((comment, sentiment_label))

    return results
