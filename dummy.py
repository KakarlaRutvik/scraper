import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import itertools
import time
import sys

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

# Animation helper function
def display_animation(message, duration=5):
    animation = itertools.cycle([message + ".", message + "..", message + "..."])
    start_time = time.time()
    while time.time() - start_time < duration:
        sys.stdout.write("\r" + next(animation))  # Overwrites the current line
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r")  # Clears the line when done

# Function to download a PDF and save it to the specified folder
def download_pdf(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder_path, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"\nFailed to download PDF from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"\nError downloading PDF from {url}: {e}")

# Function to scrape a webpage and save the content to a text file
def scrape_and_save_text(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text(strip=True)
            cleaned_text = clean_text_with_nltk(text_content)
            filename = os.path.join(folder_path, f"{urlparse(url).netloc.replace('.', '_')}.txt")
            with open(filename, 'w', encoding='utf-8') as txt_file:
                txt_file.write(cleaned_text)
        else:
            print(f"\nFailed to scrape {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"\nError scraping {url}: {e}")

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
print("\nExtracting URLs...")
display_animation("Please wait", duration=5)
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
        print(f"\nFailed to process {main_url}: {e}")

# Step 2: Process each extracted URL (download PDFs or scrape web pages)
print("\nProcessing URLs...")
display_animation("Please wait", duration=5)
for main_url, urls in all_urls.items():
    for url in urls:
        if url.lower().endswith('.pdf') or 'pdf' in url.lower():
            download_pdf(url, pdf_dir)
        else:
            scrape_and_save_text(url, data_dir)

# Step 3: Clean the scraped data in the `scraped_data` directory
print("\nCleaning data...")
display_animation("Please wait", duration=5)
for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            text_content = txt_file.read()
        cleaned_text = clean_text_with_nltk(text_content)
        with open(file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(cleaned_text)

print("\nProcess completed: All data has been scraped, cleaned, and saved as text files.")
