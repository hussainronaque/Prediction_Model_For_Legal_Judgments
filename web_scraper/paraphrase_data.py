import os
import pandas as pd
from transformers import pipeline
from dotenv import load_dotenv
from groq import Groq

# Load API key from environment
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Path to the folder containing your Excel files
folder_path = r'C:\Users\hp-15\Disc D\University Files\fifth semester\DL\Deep_Learning_Project\web_scraper\check-judgement.xlsx'

# Ensure the output folder exists
output_folder = os.path.join(folder_path, "augmented_data")
os.makedirs(output_folder, exist_ok=True)

# List all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Load all Excel files into a dictionary
excel_data = {file: pd.read_excel(os.path.join(folder_path, file)) for file in excel_files}

# Paraphrase generator using Groq API
def generate_paraphrase(text):
    try:
        prompt = f""" 
        Here is an excel file of a legal judgment. Rephrase the following text:
        - Crime Scenario: [Brief description of what happened, how, when, and who was involved, what were the charges]
        - Witnesses: [Witnesses and their testimonies]
        - Judgment: [Summarized verdict, sentencing, and basis of decision, section of law applied]
        Judgment: {text}
        Answer: """
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": "paraphraser."},
                      {"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.5
        )
        paraphrased_text = response.choices[0].message.content.strip()
        return paraphrased_text
    except Exception as e:
        print(f"Error generating paraphrase: {e}")
        return text  # Return the original text if paraphrasing fails

# Function to augment the DataFrame
def augment_data(df):
    augmented_data = []

    for _, row in df.iterrows():
        try:
            # Get the original columns
            original_scenario = row.get('scenario', "")
            original_witnesses = row.get('witnesses', "")
            original_judgment = row.get('judgment', "")

            # Generate paraphrases
            paraphrased_scenario = generate_paraphrase(original_scenario)
            paraphrased_witnesses = generate_paraphrase(original_witnesses)
            paraphrased_judgment = generate_paraphrase(original_judgment)

            # Append to augmented data
            augmented_data.append({
                'scenario': paraphrased_scenario,
                'witnesses': paraphrased_witnesses,
                'judgment': paraphrased_judgment
            })
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    # Return the new DataFrame
    return pd.DataFrame(augmented_data)

# Save augmented data to a new file (not combining with the original)
def save_augmented_data(augmented_df, output_file_path):
    augmented_df.to_excel(output_file_path, index=False)
    print(f"Augmented data saved to {output_file_path}")

# Loop through each Excel file and process
for input_excel_file in excel_files:
    print(f"Processing file: {input_excel_file}")
    try:
        # Load the DataFrame
        df = excel_data[input_excel_file]

        # Augment the data
        augmented_df = augment_data(df)

        # Define the output file path
        output_excel_file = os.path.join(output_folder, f"augmented_{input_excel_file}")

        # Save only the augmented data to a new file
        save_augmented_data(augmented_df, output_excel_file)
    except Exception as e:
        print(f"Error processing file {input_excel_file}: {e}")
