from pdf_downloader import *
import pytesseract
from pdf2image import convert_from_path
import os
import shutil  # Import shutil for file operations

# For Windows users, you may need to specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# For Mac users, you may need to specify the path to the Tesseract executable
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def pdf_to_images(pdf_path):
    # Converts a PDF file to images (one image per page).
    print(f"Converting {pdf_path} to images...")
    images = convert_from_path(pdf_path)
    return images

def ocr_image(image):
    # Performs OCR on a single image.
    text = pytesseract.image_to_string(image)
    return text

def pdf_ocr(pdf_path, output_dir='./ocr_output', processed_dir='./processed_pdfs'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ensure the processed directory exists
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    print(f"Extracting text from {pdf_path}")
    # Convert PDF to images
    images = pdf_to_images(pdf_path)

    # Perform OCR on each image and save the text
    extracted_text = ''
    for i, image in enumerate(images):
        print(f"Performing OCR on page {i+1}")
        page_text = ocr_image(image)
        extracted_text += page_text

    # Save the extracted text to a .txt file
    output_file = os.path.join(output_dir, os.path.basename(pdf_path).replace('.pdf', '.txt'))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    # Move the processed PDF to the processed directory
    shutil.move(pdf_path, os.path.join(processed_dir, os.path.basename(pdf_path)))

    print(f"OCR completed. Extracted text saved to {output_file}. PDF moved to {processed_dir}")

if __name__ == '__main__':
    # Iterate over all files in the folder
    input_path = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\highcourtjudgements\\pdfs"
    for file_name in os.listdir(input_path):
        # Check if the file is a PDF
        if file_name.endswith('.pdf'):
            pdf_file_path = os.path.join(input_path, file_name)
            print(f"Processing: {pdf_file_path}")
            
            # Perform OCR on each PDF
            pdf_ocr(pdf_file_path)
