from fileinput import filename
import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
import requests

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def extract_judgment(file_path) -> dict:
    """
    Extract Crime Scenario, Witnesses, and Judgment sections from a legal judgment document using LLaMA.
    Handles long input by splitting it into smaller chunks.
    """
    # Read the judgment file
    with open(file_path, 'r', encoding='utf-8') as file:
        print(f"Reading file: {file_path}")
        content = file.read()
    
    estimated_tokens = len(content) // 4
    
    if estimated_tokens > 5000:  # Leave room for prompt and response
        # Truncate content to roughly 5000 tokens
        content = content[:20000]  # 20000 characters ≈ 5000 tokens
        print("Warning: Content truncated to fit within token limits") # we are trying to keep the content within the token limits else it will throw an error
   
    # Prompt for the LLaMA API
    prompt = f""" 
            Here is a part of a legal judgment. Extract and summarize the crime scenario and the final judgment in the following format:
                - Crime Scenario: [Provide a complete description of the events, including what happened, how, when, who was involved, and the charges.]
                - Witnesses: [List all witnesses and summarize their testimonies, including all prosecution witnesses (PWs).]
                - Judgment: [ section of law applied in the judgment, Summarized verdict, findings of the court, sentencing, and basis of decision]


            Important:
            - If this text is part of a longer document, ensure the response is complete and consistent with the context.
            - Avoid truncating or omitting key details.
            - Do not Hallucinate or add any information that is not present in the text.
            Input: {content}
           
            Answer: """
    response_of_api = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a legal assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )

    # Extract response content for this chunk
    response_text = response_of_api.choices[0].message.content

    # Initialize result dictionary
    result = {'scenario': '', 'witnesses': '', 'judgment': ''}
    
    # Parse the response
    current_section = None
    for line in response_text.split('\n'):
        line = line.strip()
        if line.startswith("**Crime Scenario:"):
            current_section = 'scenario'
            result['scenario'] = line.replace("**Crime Scenario:", "").strip()
        elif line.startswith("**Witnesses:"):
            current_section = 'witnesses'
            result['witnesses'] = line.replace("**Witnesses:", "").strip()
        elif line.startswith("**Judgment:"):
            current_section = 'judgment'
            result['judgment'] = line.replace("**Judgment:", "").strip()
        elif line and current_section:
            result[current_section] += ' ' + line

    # Clean up the extracted text
    for key in result:
        result[key] = result[key].strip()

    return result

def process_files(input_directory, output_directory):
    """
    Process text files in the input directory, extract required sections using LLaMA, and save them to Excel.
    """

    # Loop through each file in the input directory
    # for filename in os.listdir(input_directory):
    for i in range(1):
        filename = "Rahmatullah-Cr.MB.No.337-D-17.txt"
        if filename.endswith(".txt"):  # Only process text files
            file_path = os.path.join(input_directory, filename)
            
            print(f"Processing {filename}...")

            # Ensure the output directory exists
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Extract the judgment data
            result = extract_judgment(file_path)

            # Define the path to save the new Excel file in output_directory
            output_path = os.path.join(output_directory, filename.replace('.txt', '.xlsx'))
            
            # Check if the output path is too long
            max_path_length = 260  # Windows maximum path length
            if len(output_path) > max_path_length:
                # Shorten the filename
                base_filename = os.path.basename(filename).replace('.txt', '')
                shortened_filename = base_filename[:50] + '.xlsx'  # Adjust length as needed
                output_path = os.path.join(output_directory, shortened_filename)

            # Write results to an Excel file using openpyxl
            wb = Workbook()
            ws = wb.active
            ws.title = "Judgment Data"

            # Add headers
            headers = ["Scenario", "Witnesses", "Judgment"]
            ws.append(headers)

            # Add the extracted data
            ws.append([result["scenario"], result["witnesses"], result["judgment"]])

            # Apply formatting to wrap text and adjust column widths
            for col in ws.columns:
                for cell in col:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
                # Auto-adjust column width
                column_letter = col[0].column_letter
                ws.column_dimensions[column_letter].width = 50  # Adjust as needed

            # Save the workbook
            wb.save(output_path)
            print(f"Processed {filename} and saved to {output_path}.")

# Set the path for input files, output directory, checking path, and processed directory
input_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\ocr_output"  # Replace with your OCR folder path
output_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\llama-70b-without-fewshot"  # Replace with your output folder path

if __name__ == '__main__':
    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        # Run the processing function
        process_files(input_directory, output_directory)
