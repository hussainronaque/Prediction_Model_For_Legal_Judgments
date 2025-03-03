import os
import google.generativeai as genai
import pathlib
import PIL.Image

# Set the input and output folder paths
input_folder = "./invoices"
output_folder = "./output/ground_truth"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define prompt template to extract key invoice fields in JSON
prompt = """You are an expert invoice parser.
From the invoice image provided, extract the key fields:
- Invoice Number
- Items with their price, quantity, and total
- Customer Name
- Invoice Date
- Vendor Name
- Vendor Tax ID
- Payment Method
- Payment Withholding Tax Group
- PO Number
- Invoice Type
- Total Amount
Provide your answer in valid JSON format with keys exactly as mentioned.

Answer (in JSON):
"""

# Configure the API with your key
genai.configure(api_key="AIzaSyB9k6XTcl1AfaG4lYqKTcytaOZb3_gIiW8")  # Replace with your actual API key

# Initialize the Gemini 2.0 Flash model
model = genai.GenerativeModel("gemini-2.0-flash")

def process_image(image_path):
    """Process a single image and return the extracted data."""
    try:
        # Open the image with PIL
        pil_image = PIL.Image.open(image_path)
        
        # Generate content using Gemini 2.0 Flash
        response = model.generate_content(
            contents=[prompt, pil_image]  # Pass prompt and image as content
        )
        
        # Print raw response for debugging
        print(f"Raw response for {os.path.basename(image_path)}: {response.text}")
        return response.text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return f"Error: {str(e)}"

def save_result_to_txt(filename, data, output_dir):
    """Save the response to a .txt file in the output directory."""
    try:
        # Remove the file extension from the original filename and add .txt
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # Write the data to a .txt file
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(str(data) if data is not None else "No response")
        print(f"Saved ground truth to: {output_path}")
    except Exception as e:
        print(f"Error saving output for {filename}: {str(e)}")

def process_all_invoices_in_folder(input_dir, output_dir):
    """Process all images in the input folder and save ground truth."""
    # Supported image extensions
    supported_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.bmp')
    
    # Ensure input folder exists
    if not os.path.exists(input_dir):
        print(f"Input folder {input_dir} does not exist!")
        return
    
    # Process each file in the folder
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            image_path = os.path.join(input_dir, filename)
            print(f"\nProcessing: {filename}")
            
            # Process the image and get response
            response = process_image(image_path)
            
            # Save the result to a .txt file
            save_result_to_txt(filename, response, output_dir)

if __name__ == "__main__":
    process_all_invoices_in_folder(input_folder, output_folder)
    print("\nGround truth generation complete!")