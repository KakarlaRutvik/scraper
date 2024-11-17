import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# List of main URLs to scrape (with college names manually added)
urls = [
    "https://www.kluniversity.in/"
]

# Creating a dictionary with college names as keys and URLs as values
college_urls = {url.split("/")[2]: url for url in urls}

# Save the data to a JSON file
with open('university_colleges_urls.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(college_urls, jsonfile, ensure_ascii=False, indent=4)

print("The college URLs have been saved to 'university_colleges_urls.json'.")

# Dictionary to hold main URL and their sub URLs
all_urls = {}

# Loop through each main URL
for main_url in urls:
    try:
        # Send a GET request to the main URL
        response = requests.get(main_url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags with 'href' attribute
        links = set()  # Use set to avoid duplicates
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            # Create the full URL
            full_url = urljoin(main_url, link)
            links.add(full_url)  # Add to set of links

        # Save the main URL and its sub URLs in the dictionary
        all_urls[main_url] = list(links)

        print(f"Successfully processed {main_url}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to process {main_url}: {e}")

# Save the collected URLs to a JSON file
with open('university_page_urls.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(all_urls, jsonfile, ensure_ascii=False, indent=4)

print("All URLs have been processed and saved to university_page_urls.json.")
