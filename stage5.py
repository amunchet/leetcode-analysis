import os
import json
import pandas as pd
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer

# Download required NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

# Function to clean and tokenize text
def clean_and_tokenize(text):
    # Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()
    # Tokenize and remove stop words
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return words

# Load data from file
with open(os.path.join("data", "output-3200")) as f:
    data = json.load(f)
    data = data.values()

# Dictionary to hold word counts for each tag
tag_word_counts = defaultdict(Counter)
overall_word_counts = Counter()

# Process each problem
for problem in data:
    description = problem["description"]
    tags = json.loads(problem["tags"].replace("'", '"'))  # Convert string to list of dictionaries
    words = clean_and_tokenize(description)
    overall_word_counts.update(words)
    
    for tag in tags:
        tag_slug = tag['slug']
        tag_word_counts[tag_slug].update(words)

# Filter out words with count <= 10
filtered_vocab = {word for word, count in overall_word_counts.items() if count > 10}

# Create a DataFrame for word counts
df_tag_words = pd.DataFrame(tag_word_counts).fillna(0).astype(int).T

# Filter columns based on the filtered vocabulary
df_tag_words = df_tag_words.loc[:, df_tag_words.columns.intersection(filtered_vocab)]

# Calculate TF-IDF scores
tfidf_transformer = TfidfTransformer()
tfidf_matrix = tfidf_transformer.fit_transform(df_tag_words.T)

# Create DataFrame for TF-IDF scores
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), index=df_tag_words.columns, columns=df_tag_words.index)

# Get words for each tag based on TF-IDF scores and filter by frequency > 10
top_n_words_per_tag = {}

for tag in df_tfidf.columns:
    tag_scores = df_tfidf[tag]
    filtered_tag_scores = tag_scores[tag_scores.index.intersection(filtered_vocab)]
    sorted_tag_scores = filtered_tag_scores.sort_values(ascending=False)
    top_n_words_per_tag[tag] = [(word, sorted_tag_scores[word], df_tag_words.at[tag, word]) for word in sorted_tag_scores.index]

# Prepare data for CSV
max_words = max(len(words) for words in top_n_words_per_tag.values())
output_data = []

for i in range(max_words):
    row = []
    for tag in top_n_words_per_tag:
        if i < len(top_n_words_per_tag[tag]):
            word, tfidf_score, count = top_n_words_per_tag[tag][i]
            row.append(f"{word} (TF-IDF: {tfidf_score:.2f}, Count: {count})")  # Append the word with TF-IDF score and count
        else:
            row.append('')  # Append an empty string if no more words are available
    output_data.append(row)

# Create column headers from tags
headers = list(top_n_words_per_tag.keys())

# Convert to DataFrame
output_df = pd.DataFrame(output_data, columns=headers)

# Save to CSV
output_df.to_csv('tag_word_tfidf.csv', index=False)

print("CSV file 'tag_word_tfidf.csv' has been created.")
