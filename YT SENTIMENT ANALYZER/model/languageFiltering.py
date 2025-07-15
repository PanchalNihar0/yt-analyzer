import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Load your dataset
df = pd.read_csv("D:/projects/YT SENTIMENT ANALYZER/data/YoutubeCommentsDataSet.csv")  # Adjust path if needed

# Function to detect language safely
def detect_language(text):
    try:
        if isinstance(text, str):
            return detect(text)
        else:
            return "unknown"
    except:
        return "unknown"
df = df.dropna(subset=["Comment"])
# Apply language detection to each comment
df["language"] = df["Comment"].apply(detect_language)

# Filter only English comments
df_english = df[df["language"] == "en"]

# Optional: Drop the 'language' column after filtering
df_english = df_english.drop(columns=["language"])

# Save cleaned English-only dataset
df_english.to_csv("model/english_only_dataset.csv", index=False)

print(f"Filtered dataset: {len(df_english)} rows remaining.")
