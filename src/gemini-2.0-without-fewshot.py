import os
from google import genai  # Hypothetical Gemini package
from openpyxl import Workbook
from openpyxl.styles import Alignment

# Configure Gemini API (replace with your actual API key)
api_key = "AIzaSyB9k6XTcl1AfaG4lYqKTcytaOZb3_gIiW8"  # Replace with your actual key
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
    Extract Crime Scenario, Witnesses, and Judgment sections using Gemini API with zero-shot prompt.
    """
    # Zero-shot prompt without examples
    prompt = f"""
    You are a legal assistant. Your task is to analyze a legal judgment and extract key information in a structured format. Analyze the following legal judgment text and extract the information as follows:

    Input: {text}

    Extract and structure the information in this exact format:
    **Crime Scenario:** [Provide a complete description of the events, including what happened, how, when, who was involved, and the charges.]
    **Witnesses:** [List all witnesses and summarize their testimonies, including all prosecution witnesses (PWs).]
    **Judgment:** [Section of law applied in the judgment, summarized verdict, findings of the court, sentencing, and basis of decision]

    Important:
    - Ensure the response is complete and consistent with the context.
    - Avoid truncating or omitting key details.
    - Do not hallucinate or add information not present in the text.
    """

    try:
        # Generate response using Gemini API (adjust model name as needed)
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

    # Process specific file (matching your LLaMA code)
    for i in range(1):
        filename = "Rahmatullah-Cr.MB.No.337-D-17.txt"
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            print(f"Processing {filename}...")

            # Extract text from the file
            text = extract_text_from_file(file_path)
            if text:
                # Truncate if too long (similar to LLaMA approach)
                estimated_tokens = len(text) // 4
                if estimated_tokens > 5000:
                    text = text[:20000]  # Approx 5000 tokens
                    print("Warning: Content truncated to fit within token limits")

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

# Set directories (matching your LLaMA code structure)
input_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\weekly-judgements\chunk_8"
output_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\gemini-zero-shot"

if __name__ == "__main__":
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        process_files(input_directory, output_directory)