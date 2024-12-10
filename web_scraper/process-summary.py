import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from groq import Groq


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

    # Define maximum allowed length for input content (tokens)
    max_token_limit = 4000  # Adjust based on your model's token limit
    max_chunk_size = int(max_token_limit * 4)  # Estimate 4 characters per token

     ## overlap some charcters to avoid missing any important information as context will be lost
    overlap = 200  # Number of overlapping characters
    content_chunks = [
        content[i:i + max_chunk_size] for i in range(0, len(content), max_chunk_size - overlap)
    ]


    # Initialize full response dictionary
    full_response = {'scenario': '', 'witnesses': '', 'judgment': ''}

    for idx, chunk in enumerate(content_chunks):
        print(f"Processing chunk {idx + 1}/{len(content_chunks)}...")

        # Prompt for the LLaMA API
        prompt = f""" 
           Here is a part of a legal judgment. Extract and summarize the crime scenario and the final judgment in the following format:
            - Crime Scenario: [Provide a complete description of the events, including what happened, how, when, who was involved, and the charges.]
            - Witnesses: [List all witnesses and summarize their testimonies, including all prosecution witnesses (PWs).]
            - Judgment: [ section of law applied in the judgment, Summarized verdict, findings of the court, sentencing, and basis of decision]


        Important:
        - If this text is part of a longer document, ensure the response is complete and consistent with the context.
        - Avoid truncating or omitting key details.
        Input: {chunk}
        Answer: """

        # Generate response using LLaMA API
        response_of_api = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a legal assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,  # Ensure this is within your model's response limit
            temperature=0.5
        )

        # Extract response content
        response_text = response_of_api.choices[0].message.content
        with open(f'response{idx}.txt', 'w') as f:
            f.write(response_text)

        # print(f"Response for chunk {idx + 1}: {response_text}")

        # Parse and append each section to `full_response`
        in_scenario, in_witnesses, in_judgment = False, False, False
        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith("**Crime Scenario:"):
                in_scenario, in_witnesses, in_judgment = True, False, False
                full_response['scenario'] += line.replace("**Crime Scenario:", "").strip() + ' '
            elif line.startswith("**Witnesses:"):
                in_witnesses, in_scenario, in_judgment = True, False, False
                full_response['witnesses'] += line.replace("**Witnesses:", "").strip() + ' '
            elif line.startswith("**Judgment:"):
                in_judgment, in_scenario, in_witnesses = True, False, False
                full_response['judgment'] += line.replace("**Judgment:", "").strip() + ' '
            elif in_scenario:
                full_response['scenario'] += line + ' '
            elif in_witnesses:
                full_response['witnesses'] += line + ' '
            elif in_judgment: 
                full_response['judgment'] += line + ' '
            else:
                full_response['judgment'] += line + ' '

    return full_response


def process_files(input_directory, output_directory, checking_path, processed_directory):
    """
    Process text files in the input directory, extract required sections using LLaMA, and save them to Excel.
    """
    # Ensure the processed directory exists
    if not os.path.exists(processed_directory):
        os.makedirs(processed_directory)

    # Loop through each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):  # Only process text files
            file_path = os.path.join(input_directory, filename)
            
            # Check if the corresponding Excel file already exists in checking_path
            checking_file_path = os.path.join(checking_path, filename.replace('.txt', '.xlsx'))
            if os.path.exists(checking_file_path):
                print(f"Skipping {filename}, Excel file already exists at {checking_file_path}.")
                continue  # Skip processing if Excel file already exists
            
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

            # # Move the processed .txt file to the processed directory
            # processed_path = os.path.join(processed_directory, filename)
            # shutil.move(file_path, processed_path)
            # print(f"Moved {filename} to {processed_path}.")

# Set the path for input files, output directory, checking path, and processed directory
input_directory = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\check_folder"
output_directory = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\check_output"

checking_path = "C:\\path\\to\\your\\checking\\files"
processed_directory = "C:\\path\\to\\your\\processed\\files"

if __name__ == '__main__':
    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        # Run the processing function
        process_files(input_directory, output_directory, checking_path, processed_directory)
