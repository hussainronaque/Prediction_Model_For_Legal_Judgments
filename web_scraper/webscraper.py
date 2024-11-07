import requests
from bs4 import BeautifulSoup
import os

# Function to fetch and save webpage content
def save_webpage_content(url, output_filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for failed requests

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the text content from the HTML
        text_content = soup.get_text()

        # Save the text content to a .txt file
        output_path = "highcourtjudgements/webpages-pdf"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path = os.path.join(output_path, output_filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text_content)

        print(f"Content saved successfully to {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")


# https://caselaw.shc.gov.pk/caselaw/search-all/search
# List of URLs to fetch content from
urls = [
    #add your links here !
]


# Loop through each URL and save content
for index, url in enumerate(urls):
    output_filename = f"webpage_content_{index + 1}.txt"  # Generate a unique filename for each URL
    save_webpage_content(url, output_filename)

