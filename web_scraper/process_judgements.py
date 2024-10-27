import os
from groq import Groq
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key,
)


def extract_judgment(file_path) -> dict:
    # Read the judgment file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()


    # we can add more content to the prompt to make it more specific later
    prompt = f"""
    Here is a legal judgment. Extract and summarize the crime scenario and the final judgment in the following format:
    - Crime Scenario: [Brief description of what happened, how, when, and who was involved, what were the charges]
    - Witnesses: [witnesses and their testimonies]
    - Judgment: [Summarized verdict, sentencing, and basis of decision, section of law applied]
    
    Judgment:
    {content}
    
    Answer:
    """

    response_of_api = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a legal assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5
        )
    # Extract the response content
    # answer = response_of_api['choices'][0]['message']['content']
    # print(answer)
    print("=====================================")
    # return answer

    response_text = response_of_api.choices[0].message.content
    print(response_text)
    scenrio=''
    in_scenrio=False
    witnesses=''
    in_witnesses=False
    judgment=''
    in_judgment=False
    for line in response_text.split('\n'):
        # as soon as you get crime scenario, start adding to the scenario string

        if line.startswith('**Crime Scenario') :
            scenrio += line
            in_scenrio=True
            in_witnesses=False
            in_judgment=False
        elif line.startswith('**Witnesses:'):
            witnesses += line
            in_witnesses=True
            in_scenrio=False
            in_judgment=False
        elif line.startswith('**Judgment:'):
            judgment += line
            in_judgment=True
            in_witnesses=False
            in_scenrio=False
        elif in_scenrio:
            scenrio += line
        elif in_witnesses:
            witnesses += line
        elif in_judgment:
            judgment += line


    # returned a dictionary instead of a string
    return {'scenario': scenrio, 'witnesses': witnesses, 'judgment': judgment} 
    # return response_of_api.choices[0].message.content

def process_files(input_directory):
    # Prepare a list to store data for each file
    data = []
    output_path = ""

    # Loop through each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):  # Only process text files
            file_path = os.path.join(input_directory, filename)
            output_path = os.path.join(input_directory, filename.replace('.txt', '.xlsx'))
            result = extract_judgment(file_path)
            data.append(result)
            print(f"Processed {filename}.")
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    #debug output
    print(df, "=====================")

    # Write the DataFrame to an Excel file
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Results saved to {output_path}.")


# Set the path for input files and output CSV
input_directory = "ocr_output2"  


# Run the processing function
process_files(input_directory)
