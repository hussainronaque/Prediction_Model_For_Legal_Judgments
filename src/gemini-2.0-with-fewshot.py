import os
from google import genai  # Hypothetical Gemini package
from openpyxl import Workbook
from openpyxl.styles import Alignment
import shutil

# Configure Gemini API (replace with your actual API key)
api_key = "AIzaSyB9k6XTcl1AfaG4lYqKTcytaOZb3_gIiW8"
client = genai.Client(api_key=api_key)

def extract_text_from_file(file_path) -> str:
    if not os.path.exists(file_path):
        print(f"Error: File does not exist: {file_path}")
        return ''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"Reading file: {file_path}")
            content = file.read()
        if not content.strip():
            print(f"Warning: No text found in {file_path} - folder may remain empty.")
        else:
            print(f"Text extracted successfully from {file_path}. Preview (first 200 chars): {content[:200]}")
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ''
    


def extract_judgment(text) -> dict:
    """
    Extract Crime Scenario, Witnesses, Counsel Statements, and Judgment with inferred counsel statements if not explicit.
    """
    prompt = f"""
    You are a legal assistant. Your task is to analyze a legal judgment and extract key information in a structured format. Below are examples of judgments and their extracted details to guide you. Use these to understand how to extract: (1) Crime Scenario, (2) Witnesses, (3) Prosecution Counsel Statement, (4) Defense Counsel Statement, and (5) Judgment. For counsel statements, if not explicitly provided, infer plausible arguments based on the trial outcome, appeal reasoning, and court findings, ensuring they align with the text’s context.

    ### Example 1: Cr.A No. 5-M/2014
    **Input:** Judgment from Peshawar High Court, Mingora Bench. Appellants Noor Rehman and Dilawar convicted of murdering Mst. Bakhtia (FIR No. 359, 2011) under sections 302(b), 322, 34 PPC and 13 AO. Trial court sentenced them to life imprisonment and fines. Appeal argued a pre-2016 compromise with the deceased’s heirs, allowed as the honor killing law barring compromise came later. Court accepted the compromise, acquitted appellants of murder charges, reduced Dilawar’s 13 AO sentence to time served.
    **Output:**
    - **Crime Scenario:** On 16.07.2011, in Anghapur, Tehsil Daggar, District Buner, Mst. Bakhtia, aged 24/25, was found slaughtered in Noor Rehman’s house by SHO Muhammad Irshad Khan. Complainant Hazrat Rehman reported his sister Bakhtia, married to Abdur Rehman (in Malaysia), lived with Noor Rehman (brother-in-law) and was killed by Noor Rehman and Dilawar, who suspected her of immoral character. Charged under sections 302(b), 322, 34 PPC, and 13 AO.
    - **Witnesses:** PW-5 Hazrat Rehman (complainant, reported murder); PW-6 Muhammad Irshad Khan (SHO, found body); PW-7 Sher Muhammad Khan (recovered weapons); PW-8 Balezar Khan (initial investigator, collected blood). Ten witnesses total, key ones listed.
    - **Prosecution Counsel Statement:** Likely argued that the appellants’ guilt was proven by eyewitness testimony, recovered weapons, and confessions, justifying the life imprisonment for an honor-based murder.
    - **Defense Counsel Statement:** Argued that a pre-2016 compromise with the deceased’s heirs was legally valid, as the 2016 honor killing law barring compromise did not apply retrospectively, seeking acquittal.
    - **Judgment:** Sections 302(b), 322, 34 PPC, and 13 AO applied. Court accepted the compromise (pre-2016 law), acquitted appellants of murder charges, reduced Dilawar’s 13 AO sentence to time served (24.09.2020), citing no retrospective effect of the 2016 Amendment Act.

    ### Example 2: Cr.A No. 56-M/2022
    **Input:** Peshawar High Court, Mingora Bench, heard Cr.A No. 56-M/2022. Appellant Said Afzal convicted under section 15 KP Arms Act, 2013, for possessing an unlicensed Kalashnikov, sentenced to three years RI and fine. Appeal highlighted weak evidence: unproduced case property, unreliable witness testimony, and a flawed confession. Court found prosecution failed to prove guilt beyond doubt, acquitted appellant.
    **Output:**
    - **Crime Scenario:** On an unspecified date in Tehsil Warri, District Dir Upper, Inspector Attaullah Khan (SHO) acted on spy information that Said Afzal and Naseeb Rawan, proclaimed offenders, were at their house armed with Kalashnikovs. During a police raid, both were arrested after fleeing, each with a Kalashnikov, magazines, and rounds. Charged under section 15 KP Arms Act, 2013.
    - **Witnesses:** PW-1 Armourer Wajid Ullah (examined weapon); PW-3 Constable Iqbal (recovery witness); PW-4 ASI Ziaullah (received case property); PW-5 ASI Samiullah (testified); PW-6 Ali Khan (private witness, did not support recovery); PW-7 Inspector Attaullah (seizing officer); PW-8 Constable Rahman Uddin (recovery witness); PW-9 Judicial Magistrate (recorded confession). Nine witnesses total.
    - **Prosecution Counsel Statement:**  Contended that recovery of the Kalashnikov, supported by police witnesses and a confession, sufficiently proved illegal possession, warranting conviction.
    - **Defense Counsel Statement:** Argued the prosecution’s case was flawed due to unproduced case property, unreliable witness testimony (e.g., PW-6), and a procedurally defective confession, seeking acquittal.
    - **Judgment:** Section 15 KP Arms Act, 2013 applied. Court acquitted Said Afzal (14.02.2023), finding evidence insufficient (unproduced property, doubtful confession, witness contradictions), applying the benefit of doubt.

    **Task:** Analyze the following legal judgment text and extract the information in this exact format:
    Input: {text}

    Extract and structure the information:
    - **Crime Scenario:** [Complete description of events, including what happened, how, when, who was involved, and charges.]
    - **Witnesses:** [List all witnesses and summarize their testimonies, including all PWs.]
    - **Prosecution Counsel Statement:** [Summarize key arguments; infer from trial outcome and evidence if not explicit.]
    - **Defense Counsel Statement:** [Summarize key arguments; infer from appeal reasoning if not explicit.]
    - **Judgment:** [Section of law, verdict, findings, sentencing, and basis of decision.]

    Important:
    - Ensure completeness and consistency with the context.
    - Avoid omitting key details or adding unprovided information beyond reasonable inference.
    - Infer counsel statements logically from the text’s implications if not explicitly stated.
  """
    try:
        # Generate response using Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Hypothetical model name
            contents=[prompt]
        )
        
        response_text = response.text
        print(f"API Response: {response_text}")  # Debug: Print raw response

        # Initialize result dictionary with the expected keys
        result = {
            'scenario': '',
            'witnesses': '',
            'prosecution_counsel': '',
            'defense_counsel': '',
            'judgment': ''
        }

        # Parse the response line-by-line, handling both formats
        current_section = None
        for line in response_text.split('\n'):
            line = line.strip()
            # Remove leading '-' if present
            if line.startswith('-'):
                line = line[1:].strip()


            # Format 1: "Key": "Value"
            if line.startswith('"Crime Scenario":'):
                current_section = 'scenario'
                result['scenario'] = line.split(':', 1)[1].strip().strip('",')
            elif line.startswith('"Witnesses":'):
                current_section = 'witnesses'
                result['witnesses'] = line.split(':', 1)[1].strip().strip('",')
            elif line.startswith('"Prosecution Counsel Statement":'):
                current_section = 'prosecution_counsel'
                result['prosecution_counsel'] = line.split(':', 1)[1].strip().strip('",')
            elif line.startswith('"Defense Counsel Statement":'):
                current_section = 'defense_counsel'
                result['defense_counsel'] = line.split(':', 1)[1].strip().strip('",')
            elif line.startswith('"Judgment":'):
                current_section = 'judgment'
                result['judgment'] = line.split(':', 1)[1].strip().strip('",')
            # Format 2: **Key:** Value
            elif line.startswith('**Crime Scenario:**'):
                current_section = 'scenario'
                result['scenario'] = line.replace('**Crime Scenario:**', '').strip()
            elif line.startswith('**Witnesses:**'):
                current_section = 'witnesses'
                result['witnesses'] = line.replace('**Witnesses:**', '').strip()
            elif line.startswith('**Prosecution Counsel Statement:**'):
                current_section = 'prosecution_counsel'
                result['prosecution_counsel'] = line.replace('**Prosecution Counsel Statement:**', '').strip()
            elif line.startswith('**Defense Counsel Statement:**'):
                current_section = 'defense_counsel'
                result['defense_counsel'] = line.replace('**Defense Counsel Statement:**', '').strip()
            elif line.startswith('**Judgment:**'):
                current_section = 'judgment'
                result['judgment'] = line.replace('**Judgment:**', '').strip()
            # Append multi-line content for either format
            elif line and current_section and not line.startswith('}') and not line.startswith('{') and not line.startswith('-') and not line.startswith('"') and not line.startswith('**'):
                result[current_section] += ' ' + line.strip().strip('",')

        # Clean up any trailing whitespace
        for key in result:
            result[key] = result[key].strip()

        print(f"Parsed Result: {result}")  # Debug: Print the parsed result
        return result

    except Exception as e:
        print(f"Error during API call or parsing: {e}")
        return {
            'scenario': 'Error',
            'witnesses': 'Error',
            'prosecution_counsel': 'Error',
            'defense_counsel': 'Error',
            'judgment': f'Error: {str(e)}'
        }
def process_files(input_directory, output_directory):
    """
    Process .txt files in the input directory, analyze with Gemini, and save to Excel.
    Create a subfolder for each input text file inside the output folder.
    """
  

    # Process each .txt file in the input directory
    for filename in os.listdir(input_directory):
   
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            print(f"Processing {filename}...")

            # Extract text from the file
            text = extract_text_from_file(file_path)
            if text:
                # Create a base name for the folder (without .txt)
                base_name = filename.replace('.txt', '')

                # Handle very long filenames
                if len(base_name) > 50:
                    base_name = base_name[:50]

                # Create a subfolder for this judgment
                case_folder = os.path.join(output_directory, base_name)
                if not os.path.exists(case_folder):
                    os.makedirs(case_folder)

                # Analyze text with Gemini API
                result = extract_judgment(text)

                # Define paths within the subfolder
                excel_path = os.path.join(case_folder, f"{base_name[:10]} - analysis.xlsx")
                text_path = os.path.join(case_folder, f"{base_name[:10]} - original.txt")

                # Create and save Excel file
                wb = Workbook()
                ws = wb.active
                ws.title = "Judgment Data"

                headers = ["Scenario", "Witnesses", "Prosecution Counsel Statement", "Defense Counsel Statement", "Judgment"]
                ws.append(headers)

                ws.append([
                    result.get("scenario", ""),
                    result.get("witnesses", ""),
                    result.get("prosecution_counsel", ""),
                    result.get("defense_counsel", ""),
                    result.get("judgment", "")
                ])

                for col in ws.columns:
                    for cell in col:
                        cell.alignment = Alignment(wrap_text=True, vertical="top")
                    column_letter = col[0].column_letter
                    ws.column_dimensions[column_letter].width = 50

                wb.save(excel_path)

                # Copy the original text file to the case folder
                shutil.copy2(file_path, text_path)

                print(f"Created folder {case_folder} with analysis.xlsx and original.txt")

# Set directories
input_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\weekly-judgements\chunk_1"  # Replace with your OCR folder path
output_directory = r"C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\src\dataset\weekly-judgements\excel-chunk_1"  # Replace with your output folder path

if __name__ == "__main__":
    if not os.path.exists(input_directory):
        print(f"Directory {input_directory} does not exist.")
    else:
        process_files(input_directory, output_directory)