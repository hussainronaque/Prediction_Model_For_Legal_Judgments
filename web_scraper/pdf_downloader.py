import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re

def get_pdf_links(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we get a successful response

    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all links that contain .pdf
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if '.pdf' in a['href']]

    return pdf_links

def download_pdfs(base_url, output_dir='judgements'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all PDF links from the base URL
    pdf_links = get_pdf_links(base_url)

    if not pdf_links:
        print("No PDF links found.")
        return

    for link in pdf_links:
        pdf_url = urljoin(base_url, link)  # Create an absolute URL
        file_name = re.sub(r'[^a-zA-Z0-9]', '.', link.split('/')[-1])  # Sanitize the filename

        # Download and save the PDF file
        response = requests.get(pdf_url)
        response.raise_for_status()

        with open(os.path.join(output_dir, file_name), 'wb') as f:
            f.write(response.content)

        print(f"Downloaded: {file_name}")

if __name__ == '__main__':
    # List of URLs to download PDFs from
    url = [
        'https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting',
        'https://www.supremecourt.gov.pk/judgement-search/#1573035933449-63bb4a39-ac81',
        'https://www.peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search',
        'https://caselaw.shc.gov.pk/caselaw/search-all/search'
    ]
    
    # Loop through each URL and download PDFs
    for i in url:
        download_pdfs(i)
