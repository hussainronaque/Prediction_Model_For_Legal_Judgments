import os
import re
import pandas as pd

def extract_input_output(text):
    # Use regex or string matching to identify sections of input and output
    input_data = {
        'Crime Committed': '',
        'Crime Scenario': '',
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

    # Example: You can improve this with more sophisticated patterns if needed
    crime_pattern = r'(crime committed|offence|incident|accused|Crime|Offence|Incident|Accused|Committed|Murder|Assault|Shooting|Firearm|Injuries).+'
    witnesses_pattern = r'(witnesses|statements).+'
    proofs_pattern = r'(evidence|proofs|findings).+'
    verdict_pattern = r'(verdict|judgment|conclusion).+'
    sections_pattern = r'(section|law|punishment).+'

    # Identify sections of the input and output
    lines = text.split('\n')

    for line in lines:
        line = line.strip().lower()

        if re.search(crime_pattern, line):
            input_data['Crime Committed'] += line + '\n'
        elif re.search(witnesses_pattern, line):
            input_data['Witnesses'] += line + '\n'
        elif re.search(proofs_pattern, line):
            input_data['Proofs'] += line + '\n'
        elif re.search(verdict_pattern, line):
            output_data['Verdict'] += line + '\n'
        elif re.search(sections_pattern, line):
            output_data['Law Sections Imposed'] += line + '\n'

    return input_data, output_data

def save_to_excel(input_data, output_data, excel_file):
    # Creating a DataFrame to store the input and output data
    data = {
        'Input': [
            input_data['Crime Committed'],
            input_data['Crime Scenario'],
            input_data['Witnesses'],
            input_data['Proofs'],
            input_data['Findings'],
            input_data['Court Proceedings']
        ],
        'Output': [
            output_data['Verdict'],
            output_data['Law Sections Imposed'],
            output_data['Charges'],
            output_data['Punishment Given']
        ]
    }

    sub_columns = {
        'Input': ['Crime Committed', 'Crime Scenario', 'Witnesses', 'Proofs', 'Findings', 'Court Proceedings'],
        'Output': ['Verdict', 'Law Sections Imposed', 'Charges', 'Clause','sub-Clause', 'Punishment Given']
    }

    # Create a Pandas DataFrame
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
    txt_file_path = 'ocr_output/2024LHC4027.txt'
    excel_file_path = 'input_output/2024LHC4027.xlsx'

    # Process the text and save results to Excel
    process_txt_file(txt_file_path, excel_file_path)
