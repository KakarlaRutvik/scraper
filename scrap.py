import requests
import csv
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse

# Read the URLs from the CSV file
def read_urls_from_csv(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader if row]  # Only take the first column and skip empty rows
    return urls

# Function to get domain as a filename-friendly string
def get_domain(url):
    domain = urlparse(url).netloc
    return domain.replace("www.", "").replace(".", "_")

# Directory for JSON files
json_output_dir = "scraped_data"
os.makedirs(json_output_dir, exist_ok=True)

# CSV file containing the URLs
csv_file = 'university_page_urls.csv'

# Read the URLs from CSV
urls = read_urls_from_csv(csv_file)

# Loop through each main URL
for main_url in urls:
    try:
        # Send a GET request to the main URL
        main_response = requests.get(main_url)
        main_response.raise_for_status()  # Ensure request was successful

        # Parse the HTML content of the main page
        main_soup = BeautifulSoup(main_response.content, 'html.parser')

        # Extract all sub-URLs (links) from the page
        sub_urls = [a['href'] for a in main_soup.find_all('a', href=True)]
        
        # Ensure all URLs are absolute URLs
        sub_urls = [requests.compat.urljoin(main_url, href) for href in sub_urls]

        # Dictionary to store page content for each sub-URL
        main_data = {}

        # Loop through each sub-URL under the main URL
        for sub_url in sub_urls:
            try:
                # Send GET request to sub-URL
                sub_response = requests.get(sub_url)
                sub_response.raise_for_status()  # Ensure request was successful

                # Parse the HTML content of the sub-page
                sub_soup = BeautifulSoup(sub_response.content, 'html.parser')

                # Extract and clean text from the sub-page
                sub_text = sub_soup.get_text(separator=' ', strip=True)

                # Add the content to the main_data dictionary
                main_data[sub_url] = sub_text
                print(f"Scraped content from: {sub_url}")

            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve {sub_url}: {e}")
                main_data[sub_url] = "Failed to retrieve data"

        # Write the data to a JSON file named after the main URL's domain
        domain_name = get_domain(main_url)
        json_file_path = os.path.join(json_output_dir, f"{domain_name}.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(main_data, json_file, ensure_ascii=False, indent=4)

        print(f"Data for main URL {main_url} saved to {json_file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to process main URL {main_url}: {e}")
