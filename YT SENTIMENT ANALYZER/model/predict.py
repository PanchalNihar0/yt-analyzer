# model/predict.py

import pickle
from model.PreProcessing import preprocess
from langdetect import detect

# Load vectorizer and model once
with open("D:/projects/YT SENTIMENT ANALYZER/model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("D:/projects/YT SENTIMENT ANALYZER/model/logistic_model.pkl", "rb") as f:
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
    Takes list of raw comments.
    Returns prediction list of labels (0=neg, 1=neutral, 2=pos).
    """
    cleaned, original = clean_and_filter(comments)
    if not cleaned:
        return [], []

    X = vectorizer.transform(cleaned)
    preds = model.predict(X)
    return preds, original
