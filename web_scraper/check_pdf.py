import os

# Specify the paths for the folders
pdf_folder = '/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/judgements_done'    # Path to the folder containing PDF files
txt_folder = '/path/to/txt_folder'    # Path to the folder containing OCR .txt files
xlsx_folder = '/path/to/xlsx_folder'  # Path to the folder containing .xlsx files

# Get a set of PDF file names (without extension)
pdf_files = {os.path.splitext(pdf)[0] for pdf in os.listdir(pdf_folder) if pdf.endswith('.pdf')}

# Iterate over each .txt file in the txt_folder
for txt_file in os.listdir(txt_folder):
    if txt_file.endswith('.txt'):
        txt_name = os.path.splitext(txt_file)[0]  # Get the file name without extension

        # Check if a corresponding PDF file exists
        if txt_name not in pdf_files:
            # If no matching PDF is found, delete the .txt file
            txt_path = os.path.join(txt_folder, txt_file)
            os.remove(txt_path)
            print(f"Deleted {txt_file} as no corresponding PDF file was found.")

            # Check and delete the corresponding .xlsx file if it exists
            xlsx_file = f"{txt_name}.xlsx"
            xlsx_path = os.path.join(xlsx_folder, xlsx_file)
            if os.path.exists(xlsx_path):
                os.remove(xlsx_path)
                print(f"Deleted {xlsx_file} as it corresponds to the missing PDF and TXT files.")
