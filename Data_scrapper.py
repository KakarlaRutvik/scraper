import os
import csv
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

# Create the necessary directories if they do not exist
os.makedirs('/workspaces/scraper/pdfdata', exist_ok=True)
os.makedirs('/workspaces/scraper/scraped_data', exist_ok=True)

# please fill this blank where it reads data from json file named "college_urls.json"
[ code part]

# Function to download a PDF and save it to the specified folder
def download_pdf(url, folder_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Ensure the request was successful
        if response.status_code == 200:
            # Get the filename from the URL
            filename = os.path.join(folder_path, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded PDF: {filename}")
        else:
            print(f"Failed to download PDF from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading PDF from {url}: {e}")

# Function to scrape a webpage and save the content to a JSON file
def scrape_and_save_json(url, folder_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the textual content (you can modify this based on your needs)
            text_content = soup.get_text(strip=True)
            
            # Prepare data to be saved in JSON
            data = {
                'url': url,
                'content': text_content
            }

            # Create a filename based on the URL
            filename = os.path.join(folder_path, f"{urlparse(url).netloc.replace('.', '_')}.json")
            
            # Save the data as a JSON file
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print(f"Scraped data saved to: {filename}")
        else:
            print(f"Failed to scrape {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Open and read the CSV file
with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # Read CSV as dictionary
    for row in reader:
        # Check if 'pageurls' column exists and if the value is a valid URL
        if 'pageurls' in row and row['pageurls']:
            url = row['pageurls']
            
            # Check if the URL is a PDF
            if url.lower().endswith('.pdf') or 'pdf' in url.lower():
                # If it's a PDF, download it
                download_pdf(url, '/workspaces/scraper/pdfdata')
            else:
                # If it's not a PDF, scrape the webpage and save it as JSON
                scrape_and_save_json(url, '/workspaces/scraper/scraped_data')
