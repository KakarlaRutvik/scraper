import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# List of main URLs to scrape
urls = [
    "https://www.kluniversity.in/"
]

# Loop through each main URL
for main_url in urls:
    try:
        # Send a GET request to the main URL
        response = requests.get(main_url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags with 'href' attribute
        links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            # Create the full URL
            full_url = urljoin(main_url, link)
            links.append(full_url)

        # Print the main URL and each page URL
        print(f"Main URL: {main_url}")
        for page_url in links:
            print(f"  - {page_url}")

        print(f"Successfully processed {main_url}\n")

    except requests.exceptions.RequestException as e:
        print(f"Failed to process {main_url}: {e}")

print("All URLs have been processed.")
