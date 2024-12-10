
import openai
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ```https://codesphere.com/articles/ai-summarization```





def split_text_into_chunks(text, max_tokens=1500):
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



## 


openai.api_key = "your_openai_api_key"
def summarize_chunk(chunk):
   """
   #    response = openai.ChatCompletion.create(
   Summarizes a given text chunk using GPT-4.
   """
   response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
           {"role": "user", "content": f"Summarize this: {chunk}"}
       ],
       max_tokens=1500
   )
     
 
   
   response_text = response.choices[0].message.content
   return response_text



def recursive_summarization(summaries):
   """
   Combines and summarizes a list of summaries into a single concise summary.
   """
   combined_text = " ".join(summaries)
   if len(combined_text.split()) < 1500:  # Final summary target length
       return combined_text
   else:
       return summarize_chunk(combined_text)







# Example usage:
judgement_path = "C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\ocr_output_done\\16-of-2011-_u.-s-9-C-Dismissed.txt"
file = open(judgement_path, "r")
text = file.read()
chunks = split_text_into_chunks(text)
# print(f"Generated {len(chunks)} chunks.")
# print(chunks)


# Example usage:
summaries = [summarize_chunk(chunk) for chunk in chunks]
# print("Summarized Chunks:", summaries)



# Example usage:
final_summary = recursive_summarization(summaries)
print("Final Summary:", final_summary)

