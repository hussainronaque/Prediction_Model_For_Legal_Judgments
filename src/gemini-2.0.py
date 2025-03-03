import os
from google import genai  # Adjust based on actual Gemini package (e.g., google.generativeai)
from openpyxl import Workbook
from openpyxl.styles import Alignment

# Configure Gemini API (replace with your actual API key)
api_key = "AIzaSyB9k6XTcl1AfaG4lYqKTcytaOZb3_gIiW8"
client = genai.Client(api_key=api_key)

def extract_text_from_file(file_path) -> str:
    """
    Read text from a .txt file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"Reading file: {file_path}")
            content = file.read()
        if not content.strip():
            print(f"Warning: No text found in {file_path}.")
        else:
            print(f"Text extracted successfully from {file_path}. Preview (first 200 chars): {content[:200]}")
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ''

def extract_judgment(text) -> dict:
    """
    Extract Crime Scenario, Witnesses, and Judgment sections using Gemini API.
    """
    # Detailed prompt similar to the Grok example
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

    Input: {text}

    Extract and structure the information as follows:
    **Crime Scenario:** [Provide complete description including what happened, how, when, who was involved, and the charges]

    **Witnesses:** [List all witnesses chronologically with their roles and key testimony points]

    **Judgment:** [Include applicable sections of law, court's findings, reasoning, and final verdict with sentencing]
    """

    try:
        # Generate response using Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Adjust model name as per Gemini API documentation
            contents=[prompt]
        )

        response_text = response.text

        # Parse the response into a dictionary
        result = {'scenario': '', 'witnesses': '', 'judgment': ''}
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
    except Exception as e:
        print(f"Error during API call: {e}")
        return {'scenario': 'Error', 'witnesses': 'Error', 'judgment': f'Error: {str(e)}'}

def process_files(input_directory, output_directory):
    """
    Process .txt files in the input directory, analyze with Gemini, and save to Excel.
    """
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process each .txt file in the input directory
    # for filename in os.listdir(input_directory):
    for i in range(1):
        filename = "Rahmatullah-Cr.MB.No.337-D-17.txt"
        
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            print(f"Processing {filename}...")

            # Extract text from the file
            text = extract_text_from_file(file_path)
            if text:
                # Analyze text with Gemini API
                result = extract_judgment(text)

                # Define output Excel file path
                output_path = os.path.join(output_directory, filename.replace('.txt', '.xlsx'))

                # Handle long file paths (Windows limitation)
                max_path_length = 260
                if len(output_path) > max_path_length:
                    base_filename = os.path.basename(filename).replace('.txt', '')
                    shortened_filename = base_filename[:50] + '.xlsx'
                    output_path = os.path.join(output_directory, shortened_filename)

                # Create Excel file
                wb = Workbook()
                ws = wb.active
                ws.title = "Judgment Data"

                # Add headers
                headers = ["Scenario", "Witnesses", "Judgment"]
                ws.append(headers)

                # Add extracted data
                ws.append([result["scenario"], result["witnesses"], result["judgment"]])

                # Apply formatting
                for col in ws.columns:
                    for cell in col:
                        cell.alignment = Alignment(wrap_text=True, vertical="top")
                    column_letter = col[0].column_letter
                    ws.column_dimensions[column_letter].width = 50

                # Save the workbook
                wb.save(output_path)
                print(f"Saved processed data to {output_path}")



# Set directories
input_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\ocr_output"  # Replace with your OCR folder path
output_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\data_gemini-2.0"  # Replace with your output folder path

if __name__ == "__main__":
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        process_files(input_directory, output_directory)