import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download once
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    """Clean a single comment string"""
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'\b\d+[a-zA-Z/]*\b', '<num>', text)
    text = re.sub(r'[^a-z\s<>]', '', text)

    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]

    return " ".join(words)

# Optional: only run this block if running the script directly
if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("data/english_only_dataset.csv")
    df["Cleaned_Comment"] = df["Comment"].apply(preprocess)
    df.to_csv("data/english_cleaned_dataset.csv", index=False)
    print("✅ Preprocessing complete. Cleaned dataset saved.")
