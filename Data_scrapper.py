import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

# Directories for output
pdf_folder = '/workspaces/scraper/pdfdata'
scraped_data_folder = '/workspaces/scraper/scraped_data'
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(scraped_data_folder, exist_ok=True)

# Path to the JSON file
json_file_path = "/workspaces/scraper/university_page_urls.json"

# Load JSON data
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return {}

# Function to download PDFs
def download_pdf(url, folder_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder_path, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded PDF: {filename}")
        else:
            print(f"Failed to download PDF from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading PDF from {url}: {e}")

# Function to scrape webpage content and save to JSON
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
            print(f"Scraped data saved to: {filename}")
        else:
            print(f"Failed to scrape {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Main function to process the data
def process_data(json_file):
    data = load_json(json_file)
    for main_url, urls in data.items():
        print(f"Processing main URL: {main_url}")
        for url in urls:
            if url.lower().endswith('.pdf') or 'pdf' in url.lower():
                download_pdf(url, pdf_folder)
            else:
                scrape_and_save_json(url, scraped_data_folder)

# Execute the script
if __name__ == "__main__":
    process_data(json_file_path)
