import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')

# Download NLTK stop words if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

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

# Path to the specific JSON file
input_file_path = '/workspaces/scraper/scraped_data/angrau_ac_in.json'
output_file_path = '/workspaces/scraper/scraped_data/cl.json'

# Read the JSON file
with open(input_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Remove PDF contents from the JSON data and clean text content
cleaned_data = remove_pdf_content_from_json(data)

# Save the cleaned data to a new JSON file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)

print(f"Cleaned JSON saved to: {output_file_path}")
