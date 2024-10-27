## *** NOT IN USE ANYMORE ***

import os
import re
import pandas as pd

# Define input and output keywords
input_keywords = {
    'Crime': ['crime', 'offence', 'incident', 'accused', 'committed', 'murder', 'assault', 'shooting', 'firearm', 'injuries'],
    'Witnesses': ['witness', 'testimony', 'deposed', 'statement', 'eye-witness', 'complainant', 'evidence by', 'prosecution witnesses', 'PWs'],
    'Proofs': ['evidence', 'proof', 'found', 'recovery', 'forensic', 'medical report', 'ballistics', 'documentation', 'exhibits'],
    'Findings': ['findings', 'conclusion', 'opinion', 'established', 'result', 'determined'],
    'Court Proceedings': ['trial', 'proceedings', 'prosecution', 'defense', 'cross-examination', 'evidence submitted', 'arguments', 'denied allegations', 'statements', 'plea', 'examination', 'allegations', 'conviction', 'charges']
}

output_keywords = {
    'Verdict': ['verdict', 'judgment', 'decision', 'final order', 'conviction', 'acquittal', 'dismissal'],
    'Law Sections Imposed': ['section', 'article', 'law', 'imposed', 'code', 'penal code', 'PPC', 'clause', 'sub-clause', 'legal reference'],
    'Charges': ['charged', 'alleged', 'accused', 'indicted', 'offence', 'crime', 'conviction', 'count'],
    'Punishment Given': ['sentence', 'punishment', 'death penalty', 'life imprisonment', 'fine', 'additional imprisonment', 'compensation', 'penalized']
}

def keyword_match(line, keywords):
    """Helper function to check if any keyword matches the line."""
    for keyword in keywords:
        if keyword.lower() in line:
            return True
    return False

def extract_input_output(text):
    # Use regex or string matching to identify sections of input and output
    input_data = {
        'Crime': '',
        'Witnesses': '',
        'Proofs': '',
        'Findings': '',
        'Court Proceedings': ''
    }

    output_data = {
        'Verdict': '',
        'Law Sections Imposed': '',
        'Charges': '',
        'Punishment Given': ''
    }

    # Split the text into lines for processing
    lines = text.split('\n')

    # Process each line and classify it as input or output based on keyword matching
    for line in lines:
        line_lower = line.strip().lower()

        # Match against input keywords
        if keyword_match(line_lower, input_keywords['Crime']):
            input_data['Crime'] += line + '\n'
        elif keyword_match(line_lower, input_keywords['Witnesses']):
            input_data['Witnesses'] += line + '\n'
        elif keyword_match(line_lower, input_keywords['Proofs']):
            input_data['Proofs'] += line + '\n'
        elif keyword_match(line_lower, input_keywords['Findings']):
            input_data['Findings'] += line + '\n'
        elif keyword_match(line_lower, input_keywords['Court Proceedings']):
            input_data['Court Proceedings'] += line + '\n'

        # Match against output keywords
        elif keyword_match(line_lower, output_keywords['Verdict']):
            output_data['Verdict'] += line + '\n'
        elif keyword_match(line_lower, output_keywords['Law Sections Imposed']):
            output_data['Law Sections Imposed'] += line + '\n'
        elif keyword_match(line_lower, output_keywords['Charges']):
            output_data['Charges'] += line + '\n'
        elif keyword_match(line_lower, output_keywords['Punishment Given']):
            output_data['Punishment Given'] += line + '\n'

    return input_data, output_data

def save_to_excel(input_data, output_data, excel_file):
    # Creating a DataFrame to store the input and output data
    sub_columns = {
        'Input': ['Crime', 'Witnesses', 'Proofs', 'Findings', 'Court Proceedings'],
        'Output': ['Verdict', 'Law Sections Imposed', 'Charges', 'Punishment Given']
    }

    df_input = pd.DataFrame([input_data], columns=sub_columns['Input'])
    df_output = pd.DataFrame([output_data], columns=sub_columns['Output'])

    # Create an Excel writer and write to two separate sheets
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_input.to_excel(writer, sheet_name='Input', index=False)
        df_output.to_excel(writer, sheet_name='Output', index=False)

    print(f"Data saved to {excel_file}")

def process_txt_file(txt_file_path, excel_file_path):
    # Read the .txt file
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract inputs and outputs
    input_data, output_data = extract_input_output(text)

    # Save to Excel
    save_to_excel(input_data, output_data, excel_file_path)

if __name__ == '__main__':
    # Path to the .txt file and the Excel output file
    # txt_file_path = 'ocr_output/2024LHC4027.txt'
    # excel_file_path = 'input_output/2024LHC4027.xlsx'

    # # Process the text and save results to Excel
    # process_txt_file(txt_file_path, excel_file_path)
    
    for file_name in os.listdir('ocr_output'):
    # Check if the file is a PDF
        if file_name.endswith('.txt'):
            txt_file_path = os.path.join('ocr_output', file_name)
            print(f"Processing: {txt_file_path}")
            
            excel_file_path = os.path.join('input_output', file_name.replace('.txt', '.xlsx'))
            
            # Perform OCR on each PDF
            process_txt_file(txt_file_path, excel_file_path)