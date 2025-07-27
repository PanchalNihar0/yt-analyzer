import sys
import os

# ✅ Ensure parent directory is in sys.path to import model.predict
PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from youtube_comment_downloader import YoutubeCommentDownloader
from model.predict import predict_sentiments  # ✅ Use your existing predict.py as-is

# 🔹 Function to fetch YouTube comments
def fetch_comments(youtube_url, max_count=100):
    downloader = YoutubeCommentDownloader()
    comments = []
    for comment in downloader.get_comments_from_url(youtube_url):
        comments.append(comment['text'])
        if len(comments) >= max_count:
            break
    return comments

# 🧪 Main Execution
if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    print("🔄 Fetching comments...")
    raw_comments = fetch_comments(url)
    print(f"💬 Fetched {len(raw_comments)} comments.")

    if not raw_comments:
        print("❌ No comments fetched. Exiting.")
        exit()

    print("🔍 Predicting sentiments...")
    results = predict_sentiments(raw_comments)  # ✅ Using your predict.py function directly

    if not results:
        print("❌ No results to display after prediction.")
    else:
        print("\n📋 Labeled Sentiments:")
        for comment, sentiment in results:
            print(f"{comment} → {sentiment}")
