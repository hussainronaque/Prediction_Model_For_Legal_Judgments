import os
from groq import Groq
from dotenv import load_dotenv


## in this code add a check keh if the summaries of incoming files are already present then skip the file and move to the next file

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY2")
client = Groq(api_key=api_key)


def split_text_into_chunks(text, max_tokens=3500):
    """
    Splits text into chunks of a given token size.
    """
    chunks = []
    current_chunk = []
    current_length = 0
    for word in text.split():
        word_length = len(word) + 1  # Including space
        if current_length + word_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = word_length
        else:
            current_chunk.append(word)
            current_length += word_length
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def summarize_chunk(chunk):
    """
    Summarizes a given text chunk using the LLaMA API.
    """
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": f"Summarize this: {chunk}"}
        ],
        max_tokens=3500
    )
    response_text = response.choices[0].message.content
    return response_text


def recursive_summarization(summaries):
    """
    Combines and summarizes a list of summaries into a single concise summary.
    """
    combined_text = " ".join(summaries)
    if len(combined_text.split()) < 3500:  # Final summary target length
        return combined_text
    else:
        return summarize_chunk(combined_text)


# File paths
input_dir = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\gpt_data_done"
output_dir = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\summaries-judgements"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_dir, filename)

        try:
            # Read the input file
            with open(input_path, "r", encoding="utf-8") as file:
                text = file.read()

            # Split the text into chunks and summarize
            chunks = split_text_into_chunks(text)
            summaries = [summarize_chunk(chunk) for chunk in chunks]
            final_summary = recursive_summarization(summaries)

            # Save the final summary to the output directory
            output_path = os.path.join(output_dir, f"summary_{filename}")
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(final_summary)

            print(f"Summary saved to: {output_path}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
