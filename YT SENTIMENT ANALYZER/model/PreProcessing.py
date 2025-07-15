import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load your English-only dataset
df = pd.read_csv("data/english_only_dataset.csv")

# Initialize tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    
    # Replace numbers, 10/10, 5stars, 20gb etc. with <num>
    text = re.sub(r'\b\d+[a-zA-Z/]*\b', '<num>', text)

    # Remove everything except lowercase letters, space, and <num> markers
    text = re.sub(r'[^a-z\s<>]', '', text)

    # Tokenize and clean
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    
    return " ".join(words)

# Apply cleaning to each comment
df["Cleaned_Comment"] = df["Comment"].apply(clean_text)

# Save to new CSV
df.to_csv("data/english_cleaned_dataset.csv", index=False)

print("✅ Preprocessing complete. Cleaned dataset saved.")
