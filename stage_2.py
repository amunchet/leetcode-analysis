import json
import re
import os
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

# Sample data (replace with your actual JSON data)
data = [
    {
        'tags': "[{'name': 'Array', 'id': 'VG9waWNUYWdOb2RlOjU=', 'slug': 'array'}, {'name': 'Hash Table', 'id': 'VG9waWNUYWdOb2RlOjY=', 'slug': 'hash-table'}]",
        'description': '<p>given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>\n\n<p>you may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>\n\n<p>you can return the answer in any order.</p>\n\n<p>&nbsp;</p>\n<p><strong class="'
    },
    # Add more entries here
]

with open(os.path.join("data", "output-3200")) as f:
    data = json.load(f)
    data = data.values()

# Function to clean and tokenize text
def clean_and_tokenize(text):
    # Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()
    # Tokenize and remove stop words
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return words

# Dictionary to hold word counts for each tag
tag_word_counts = defaultdict(Counter)

# Process each problem
for problem in data:
    # print("Problem:", problem)
    description = problem["description"]
    tags = json.loads(problem["tags"].replace("'", '"'))  # Convert string to list of dictionaries
    words = clean_and_tokenize(description)
    
    for tag in tags:
        tag_slug = tag['slug']
        tag_word_counts[tag_slug].update(words)

# Convert to a list of tags with word counts
tag_word_counts_list = {tag: counts.most_common() for tag, counts in tag_word_counts.items()}

# Print the result
for tag, words in tag_word_counts_list.items():
    print(f"Tag: {tag}")
    for word, count in words:
        print(f"  {word}: {count}")
    print()
