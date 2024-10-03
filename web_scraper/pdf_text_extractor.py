import pytesseract
from pdf2image import convert_from_path
import os

# For Windows users, you may need to specify the path to the Tesseract executable
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

#For Mac users, you may need to specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def pdf_to_images(pdf_path):
    # Converts a PDF file to images (one image per page).
    images = convert_from_path(pdf_path)
    return images

def ocr_image(image):
    # Performs OCR on a single image.
    text = pytesseract.image_to_string(image)
    return text

def pdf_ocr(pdf_path, output_dir='ocr_output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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

    print(f"OCR completed. Extracted text saved to {output_file}")

if __name__ == '__main__':
    # Path to your PDF file
    pdf_file_path = 'judgements/2024LHC4027.pdf'
    
    # Perform OCR on the PDF
    pdf_ocr(pdf_file_path) 