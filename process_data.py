import json
import pandas as pd
from collections import defaultdict, Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

# Sample data (replace with your actual data)
data = [
    {
        "title": "Two Sum",
        "tags": ["array", "hash-table"],
        "description": "Given an array of integers, return indices of the two numbers such that they add up to a specific target."
    },
    {
        "title": "Add Two Numbers",
        "tags": ["linked-list", "math"],
        "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit."
    },
    # Add more problem data here
]


with open(os.path.join("data", "output-3200")) as f:
    data = json.load(f)
    data = data.values()

def process(data):
    # Function to clean and tokenize text
    def clean_and_tokenize(text):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]
        return words

    # Dictionary to hold word counts for each tag
    tag_word_counts = defaultdict(Counter)

    # Process each problem
    for problem in data:
        description = problem["description"]
        tags = problem["tags"]
        words = clean_and_tokenize(description)
        
        for tag in tags:
            tag_word_counts[tag].update(words)

    # Convert to DataFrame for easier analysis
    tag_word_counts_df = pd.DataFrame(tag_word_counts).fillna(0).astype(int)

    # Function to get top n words for each tag
    def get_top_n_words(tag_word_counts, n):
        top_words = {}
        for tag, counts in tag_word_counts.items():
            top_words[tag] = counts.most_common(n)
        return top_words

    # Get top n words for each tag
    top_n_words_per_tag = get_top_n_words(tag_word_counts, 10)  # Change 10 to your desired number

    # Display the top words for each tag
    r = {}
    for tag, words in top_n_words_per_tag.items():
        print(f"Tag: {tag}")
        for word, count in words:
            print(f"  {word}: {count}")
        print()
        r[tag] = [(x,y) for x,y in words]
    
  
    return r

if __name__ == "__main__":
    print(process(data))