import os
import json
import pandas as pd
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

# Process each problem
for problem in data:
    description = problem["description"]
    tags = json.loads(problem["tags"].replace("'", '"'))  # Convert string to list of dictionaries
    words = clean_and_tokenize(description)
    
    for tag in tags:
        tag_slug = tag['slug']
        tag_word_counts[tag_slug].update(words)

# Find the maximum number of words for any tag to ensure equal rows
max_words = max(len(counts) for counts in tag_word_counts.values())

# Prepare data for DataFrame
output_data = []

for i in range(max_words):
    row = []
    for tag in tag_word_counts:
        most_common_words = tag_word_counts[tag].most_common()
        if i < len(most_common_words):
            word, count = most_common_words[i]
            row.append(f"{word} ({count})")  # Append the word with count
        else:
            row.append('')  # Append an empty string if no more words are available
    output_data.append(row)

# Create column headers from tags
headers = list(tag_word_counts.keys())

# Convert to DataFrame
output_df = pd.DataFrame(output_data, columns=headers)

# Save to CSV
output_df.to_csv('tag_word_counts.csv', index=False)

print("CSV file 'tag_word_counts.csv' has been created.")
