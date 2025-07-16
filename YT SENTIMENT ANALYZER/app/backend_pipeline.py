import sys
import os

# ✅ Add parent directory to sys.path to import model
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import pickle
from youtube_comment_downloader import YoutubeCommentDownloader
from langdetect import detect
from model.PreProcessing import preprocess

# 🔹 Step 1: Fetch comments
def fetch_comments(youtube_url, max_count=100):
    downloader = YoutubeCommentDownloader()
    comments = []
    for comment in downloader.get_comments_from_url(youtube_url):
        comments.append(comment['text'])
        if len(comments) >= max_count:
            break
    return comments

# 🔹 Step 2: Filter English comments
def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

def filter_english(comments):
    return [c for c in comments if is_english(c)]

# 🔹 Step 3: Clean each comment
def clean_comments(comments):
    return [preprocess(c) for c in comments]

# 🔹 Step 4: Load model and vectorizer
with open("D:/projects/YT SENTIMENT ANALYZER/model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("D:/projects/YT SENTIMENT ANALYZER/model/logistic_model.pkl", "rb") as f:
    model = pickle.load(f)

# 🔹 Step 5: Predict
def predict_sentiment(cleaned_comments):
    X = vectorizer.transform(cleaned_comments)
    return model.predict(X)

# 🔹 Step 6: Summarize results
def get_sentiment_ratio(preds):
    from collections import Counter

    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    labels = [label_map[p] for p in preds]

    counts = Counter(labels)
    total = len(labels)

    pos = counts.get("positive", 0)
    neu = counts.get("neutral", 0)
    neg = counts.get("negative", 0)

    return {
        "total": total,
        "positive": pos,
        "neutral": neu,
        "negative": neg,
        "positive_ratio": round((pos / total) * 100, 2) if total else 0,
        "neutral_ratio": round((neu / total) * 100, 2) if total else 0,
        "negative_ratio": round((neg / total) * 100, 2) if total else 0,
    }

# 🧪 Run and test
if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    print("🔄 Fetching comments...")
    raw_comments = fetch_comments(url)
    print(f"💬 Fetched {len(raw_comments)} comments.")

    english_comments = filter_english(raw_comments)
    print(f"🌐 Filtered to {len(english_comments)} English comments.")

    cleaned = clean_comments(english_comments)
    preds = predict_sentiment(cleaned)
    result = get_sentiment_ratio(preds)

    print("\n📊 Sentiment Analysis Result:")
    print(f"Total Comments: {result['total']}")
    print(f"Positive: {result['positive']} ({result['positive_ratio']}%)")
    print(f"Neutral:  {result['neutral']} ({result['neutral_ratio']}%)")
    print(f"Negative: {result['negative']} ({result['negative_ratio']}%)")
