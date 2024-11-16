import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Set up NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Directory paths for storing scraped data and downloaded PDFs
data_dir = '/workspaces/scraper/scraped_data'
pdf_dir = '/workspaces/scraper/pdfdata'
os.makedirs(data_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

# List of main college URLs
main_urls = [
    "https://www.kluniversity.in/"  # Add other URLs as needed
]

# Function to download a PDF and save it to the specified folder
def download_pdf(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder_path, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download PDF from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading PDF from {url}: {e}")

# Function to scrape a webpage and save the content to a JSON file
def scrape_and_save_json(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text(strip=True)
            data = {'url': url, 'content': text_content}
            filename = os.path.join(folder_path, f"{urlparse(url).netloc.replace('.', '_')}.json")
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
        else:
            print(f"Failed to scrape {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Function to clean text content using NLTK
def clean_text_with_nltk(text):
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    cleaned_text = ' '.join(filtered_words)
    return cleaned_text

# Function to clean JSON data by removing PDFs and cleaning text
def remove_pdf_content_from_json(data):
    cleaned_data = {}
    for url, content in data.items():
        if url.lower().endswith('.pdf') or 'pdf' in url.lower():
            cleaned_data[url] = ""
        else:
            cleaned_data[url] = clean_text_with_nltk(content) if isinstance(content, str) else content
    return cleaned_data

# Step 1: Extract sub-URLs from main URLs
print("Please wait...")  # Display message during URL extraction
all_urls = {}
for main_url in main_urls:
    try:
        response = requests.get(main_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            full_url = urljoin(main_url, link)
            links.add(full_url)
        all_urls[main_url] = list(links)
    except requests.exceptions.RequestException as e:
        print(f"Failed to process {main_url}: {e}")

# Step 2: Process each extracted URL (download PDFs or scrape web pages)
print("Please wait...")  # Display message during scraping and downloading
for main_url, urls in all_urls.items():
    for url in urls:
        if url.lower().endswith('.pdf') or 'pdf' in url.lower():
            download_pdf(url, pdf_dir)
        else:
            scrape_and_save_json(url, data_dir)

# Step 3: Clean the scraped data in the `scraped_data` directory
print("Please wait...")  # Display message during cleaning
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        cleaned_data = remove_pdf_content_from_json(data)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)

print("Process completed: All data has been scraped, cleaned, and saved.")
