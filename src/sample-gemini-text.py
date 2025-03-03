# import os
# import pytesseract
# from PIL import Image
# from google import genai  # Adjust if the import is different (e.g., google.generativeai)

# # Step 1: Extract text from all images in the output folder using OCR
# output_dir = 'pdf_images'  # Directory where images from the PDF are saved
# text = ''

# try:
#     # Loop through all files in the output directory
#     for filename in sorted(os.listdir(output_dir)):  # Sorted to maintain page order
#         if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
#             image_path = os.path.join(output_dir, filename)
#             img = Image.open(image_path)
#             extracted_text = pytesseract.image_to_string(img)
#             text += f"--- {filename} ---\n{extracted_text}\n"
#             img.close()  # Free up memory
#     if not text.strip():
#         print("Warning: No text extracted from the images.")
#     else:
#         print("Text extracted successfully from images. Preview (first 200 chars):", text[:200])
# except Exception as e:
#     print(f"Error during OCR text extraction: {e}")
#     exit()

# # Step 2: Set up the API client and request
# try:
#     client = genai.Client(api_key="AIzaSyB9k6XTcl1AfaG4lYqKTcytaOZb3_gIiW8")
#     request = '''
#      Here is a part of a legal judgment. Extract and summarize the crime scenario and the final judgment in the following format:
#                 - Crime Scenario: [Provide a complete description of the events, including what happened, how, when, who was involved, and the charges.]
#                 - Witnesses: [List all witnesses and summarize their testimonies, including all prosecution witnesses (PWs).]
#                 - Judgment: [Section of law applied in the judgment, summarized verdict, findings of the court, sentencing, and basis of decision]

#             Important:
#             - If this text is part of a longer document, ensure the response is complete and consistent with the context.
#             - Avoid truncating or omitting key details.
#     '''

#     # Combine request and extracted text into a single prompt
#     combined_prompt = request + "\n\nHere is the text to analyze:\n" + text

#     # Step 3: Generate content using the extracted text
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",  # Verify this model name
#         contents=[combined_prompt]  # Pass as a single string in a list
#     )

#     # Step 4: Print the response
#     print(response.text)
# except AttributeError as e:
#     print(f"API Error: {e} - Check if 'models.generate_content' is the correct method.")
# except Exception as e:
#     print(f"Error during API call: {e}")