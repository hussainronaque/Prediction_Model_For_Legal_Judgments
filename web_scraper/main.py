import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpagecontent import PDFPageContent


def get_pdf_links(url):

    response = requests.get(url)
    response.raise_for_status()  # error if does not gets the response from url

    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all links that end with .pdf
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

    return pdf_links


def extract_text_from_pdf(pdf_path):

    with open(pdf_path, 'rb') as pdf_file:
        parser = PDFParser(pdf_file)
        document = PDFDocument(parser)

        text = ''
        for page in document.get_pages():
            content = PDFPageContent.create_content(page)
            text += content.get_text()

    return text


def scrape_judgements(base_url, output_dir='judgements'):
    """
    Scrapes legal judgements from a high court website and saves them to a directory.

    Args:
        base_url (str): The base URL of the website.
        output_dir (str, optional): The directory to save the judgements. Defaults to 'judgements'.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_links = get_pdf_links(base_url)

    for link in pdf_links:
        pdf_url = urljoin(base_url, link)  # Create absolute URL
        file_name = re.sub(r'[^a-zA-Z0-9]', '_', link)  # Sanitize filename

        # Download and save the PDF file
        response = requests.get(pdf_url)
        response.raise_for_status()

        with open(os.path.join(output_dir, file_name), 'wb') as f:
            f.write(response.content)

        # Extract text from the PDF and save to a separate file
        text = extract_text_from_pdf(os.path.join(output_dir, file_name))
        with open(os.path.join(output_dir, file_name.replace('.pdf', '.txt')), 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"Downloaded and processed: {file_name}")


if __name__ == '__main__':
    # Replace with the actual URL of the high court website
    high_court_url = 'https://www.supremecourt.gov.pk/judgement-search/'
    scrape_judgements(high_court_url)