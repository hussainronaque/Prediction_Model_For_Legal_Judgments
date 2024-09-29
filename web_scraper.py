import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pdf2image import convert_from_path
import pytesseract
import pdfplumber

# Set the path for the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'D:/Habib University/Deep Learning/tesseract/tesseract.exe'  # Adjust this path accordingly

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# WebDriverManager automatically installs the correct version of ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the website
driver.get('https://www.supremecourt.gov.pk/latest-judgements/')

# Give some time for the page to load
time.sleep(3)

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all PDF links
pdf_links = []
for a in soup.find_all('a', href=True):
    if a['href'].endswith('.pdf'):  # Only select PDF links
        pdf_links.append(a['href'])

# Select the top 20 most recent PDFs
pdf_links = pdf_links[:20]

# Folder to store downloaded PDFs
pdf_folder = 'pdfs'
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# Function to download PDF
def download_pdf(pdf_url, folder):
    pdf_name = pdf_url.split('/')[-1]
    pdf_path = os.path.join(folder, pdf_name)
    
    # Download the PDF
    response = requests.get(pdf_url)
    with open(pdf_path, 'wb') as f:
        f.write(response.content)
    return pdf_path

# Download the top 20 PDFs
pdf_files = [download_pdf(link, pdf_folder) for link in pdf_links]

# Function to extract text from PDF using pdfplumber (for regular PDFs)
def extract_pdf_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Check if text extraction is successful
                text += page_text + "\n"  # Append text from the page
            else:
                text += "No extractable text found on this page.\n"  # Log if no text is found
    return text

# Function to extract text from PDF using OCR (for scanned PDFs)
def extract_pdf_text_with_ocr(pdf_file):
    images = convert_from_path(pdf_file)
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)  # Extract text using OCR
    return text

# Extract information from the PDFs
case_info = []

for pdf_file in pdf_files:
    # Try to extract text normally first
    pdf_text = extract_pdf_text(pdf_file)

    # Print the PDF text for debugging
    print(f"Extracted Text from {pdf_file}:\n{pdf_text}\n{'-'*80}")

    # If no text is found, use OCR
    if "No extractable text found on this page." in pdf_text:
        print(f"Using OCR for {pdf_file}...")
        pdf_text = extract_pdf_text_with_ocr(pdf_file)
    
    # Print the OCR text for debugging
    print(f"OCR Text from {pdf_file}:\n{pdf_text}\n{'-'*80}")

    case = {"crime": "", "judgment": ""}
    
    # Extract crime and judgment
    order_index = pdf_text.find('Order')
    judgment_index = pdf_text.find('Judgment')
    
    if order_index != -1:
        case["crime"] = pdf_text[order_index:].split('\n')[0].strip()  # Get the text after 'Order'
    
    if judgment_index != -1:
        case["judgment"] = pdf_text[judgment_index:].split('\n')[0].strip()  # Get the text after 'Judgment'
    
    case_info.append(case)

# Write the extracted information to a text file
with open('case_summary_new.txt', 'w') as f:
    for i, case in enumerate(case_info, 1):
        f.write(f"Case {i}:\n")
        f.write(f"Crime: {case['crime']}\n")
        f.write(f"Judgment: {case['judgment']}\n")
        f.write("\n" + "="*50 + "\n\n")

# Close the Selenium driver
driver.quit()
