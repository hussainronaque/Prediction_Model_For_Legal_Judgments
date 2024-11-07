import os
import shutil
from groq import Groq
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def extract_judgment(file_path) -> dict:
    # Read the judgment file
    with open(file_path, 'r', encoding='utf-8') as file:
        print(f"Reading file: {file_path}")
        content = file.read()

    # Define maximum chunk size based on context limit
    max_chunk_size = 17000  # Adjust this as necessary

    # Split content into manageable chunks
    content_chunks = [content[i:i + max_chunk_size] for i in range(0, len(content), max_chunk_size)]

    # Initialize full response dictionary
    full_response = {'scenario': '', 'witnesses': '', 'judgment': ''}

    for chunk in content_chunks:
        prompt = f""" 
        Here is a part of a legal judgment. Extract and summarize the crime scenario and the final judgment in the following format:
        - Crime Scenario: [Brief description of what happened, how, when, and who was involved, what were the charges]
        - Witnesses: [witnesses and their testimonies]
        - Judgment: [Summarized verdict, sentencing, and basis of decision, section of law applied]
        Judgment: {chunk}
        Answer: """
        
        response_of_api = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a legal assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )

        # Extract response content for this chunk
        response_text = response_of_api.choices[0].message.content
        
        # Parse and append each section to `full_response`
        in_scenario, in_witnesses, in_judgment = False, False, False
        for line in response_text.split('\n'):
            if line.startswith('**Crime Scenario'):
                in_scenario, in_witnesses, in_judgment = True, False, False
            elif line.startswith('**Witnesses:'):
                in_witnesses, in_scenario, in_judgment = True, False, False
            elif line.startswith('**Judgment:'):
                in_judgment, in_scenario, in_witnesses = True, False, False
            elif in_scenario:
                full_response['scenario'] += line + ' '
            elif in_witnesses:
                full_response['witnesses'] += line + ' '
            elif in_judgment:
                full_response['judgment'] += line + ' '

    return full_response

def process_files(input_directory, output_directory, checking_path, processed_directory):
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
            
            # Convert result to a DataFrame for saving as Excel
            df = pd.DataFrame([result])
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"Processed {filename} and saved to {output_path}.")

            # Move the processed .txt file to the processed directory
            processed_path = os.path.join(processed_directory, filename)
            shutil.move(file_path, processed_path)
            print(f"Moved {filename} to {processed_path}.")

# Set the path for input files, output directory, checking path, and processed directory
input_directory = "/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/ocr_output"
output_directory = "/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/data3"
checking_path = "/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/data2"
processed_directory = "/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/ocr_output_done"
# input_directory = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\ocr_output"
# output_directory = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\processed_judgements"
# checking_path = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\processed_judgement_done"
# processed_directory = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\ocr_output_done"

if __name__ == '__main__':
    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        # Run the processing function
        process_files(input_directory, output_directory, checking_path, processed_directory)
