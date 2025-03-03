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
        print("Warning: Content truncated to fit within token limits")
   
    # Prompt for the LLaMA API
    prompt = f""" 
    You are a legal assistant. Your task is to analyze legal judgments and extract key information in a structured format. Here are two examples:

    Example 1:
    Input: In a case from 2018, John Doe was charged with robbery under Section 392 IPC. According to prosecution, he threatened a shopkeeper with a knife and stole Rs. 50,000. Two witnesses - the shopkeeper and a customer - identified the accused. The court found the accused guilty based on consistent witness testimonies and CCTV footage, sentencing him to 5 years imprisonment.

    Output:
    **Crime Scenario:** On an unspecified date in 2018, the accused John Doe committed robbery at a shop by threatening the shopkeeper with a knife and stealing Rs. 50,000. He was charged under Section 392 IPC.

    **Witnesses:** 
    1. PW1 - Shopkeeper (victim) who identified the accused and described the robbery
    2. PW2 - Customer who was present during incident and identified the accused

    **Judgment:** The accused was found guilty under Section 392 IPC based on consistent witness testimonies and CCTV evidence. Sentenced to 5 years imprisonment.

    Example 2:
    Input: The accused was charged with murder under Section 302 IPC for killing his wife by strangulation on 15th March 2019. Medical evidence confirmed death by asphyxiation. The daughter witnessed the incident and testified in court. Neighbors testified hearing screams. The accused claimed mental illness but medical board found him fit. Court convicted him based on eyewitness account and circumstantial evidence.

    Output:
    **Crime Scenario:** On 15th March 2019, the accused murdered his wife by strangulation at their residence. He was charged under Section 302 IPC for murder.

    **Witnesses:**
    1. PW1 - Daughter (primary eyewitness who saw the incident)
    2. PW2 & PW3 - Neighbors who heard screams
    3. PW4 - Medical expert who confirmed death by asphyxiation
    4. PW5 - Medical board members who assessed accused's mental state

    **Judgment:** Accused convicted under Section 302 IPC based on daughter's eyewitness testimony, circumstantial evidence from neighbors, and medical evidence. Mental illness defense rejected based on medical board assessment.

    Now analyze the following legal judgment and extract information in the same format:

    Input: {content}

    Extract and structure the information as follows:
    **Crime Scenario:** [Provide complete description including what happened, how, when, who was involved, and the charges]

    **Witnesses:** [List all witnesses chronologically with their roles and key testimony points]

    **Judgment:** [Include applicable sections of law, court's findings, reasoning, and final verdict with sentencing]
    """
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
    for filename in os.listdir(input_directory):
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
input_directory = "/Users/hussainronaque/Documents/GitHub/Prediction_Model_For_Legal_Judgments/src/dataset/ocr_output"
output_directory = "/Users/hussainronaque/Documents/GitHub/Prediction_Model_For_Legal_Judgments/src/dataset/data_llama70b"

if __name__ == '__main__':
    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        # Run the processing function
        process_files(input_directory, output_directory)
