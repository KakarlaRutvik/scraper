import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Define the stop words in English
stop_words = set(stopwords.words('english'))

# Function to clean text content using NLTK (e.g., remove stop words)
def clean_text_with_nltk(text):
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words and non-alphabetic tokens
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    # Join filtered words back into a single string
    cleaned_text = ' '.join(filtered_words)
    return cleaned_text

# Function to check if a URL or path points to a PDF and clean content with NLTK
def remove_pdf_content_from_json(data):
    cleaned_data = {}
    for url, content in data.items():
        # Check if the URL or file name suggests it's a PDF file
        if url.lower().endswith('.pdf') or 'pdf' in url.lower():
            print(f"Removing content for PDF file: {url}")
            cleaned_data[url] = ""  # Remove content by setting it to an empty string
        else:
            # Clean non-PDF content with NLTK
            cleaned_data[url] = clean_text_with_nltk(content) if isinstance(content, str) else content
    return cleaned_data

# Define the directory containing JSON files
data_dir = '/workspaces/scraper/scraped_data'

# Process each JSON file in the directory
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(data_dir, filename)

        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Remove PDF contents and clean text content
        cleaned_data = remove_pdf_content_from_json(data)

        # Overwrite the original file with the cleaned data
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)

        print(f"Cleaned and overwritten JSON file: {file_path}")
