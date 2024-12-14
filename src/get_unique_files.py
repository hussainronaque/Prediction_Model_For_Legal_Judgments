import os
import shutil

# Define your folder paths
txt_folder = 'C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\ocr_output_done'git
xlsx_folder = 'C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\processed_judgements'
different_folder = 'C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\ocr_remaining'

# Create the different folder if it doesn't exist
os.makedirs(different_folder, exist_ok=True)

# Get the list of file names without extensions
txt_files = {os.path.splitext(f)[0] for f in os.listdir(txt_folder) if f.endswith('.txt')}
xlsx_files = {os.path.splitext(f)[0] for f in os.listdir(xlsx_folder) if f.endswith('.xlsx')}

# Find common and different files
common_files = txt_files & xlsx_files
different_files = (txt_files ^ xlsx_files)

# Move different files to the 'different_files' folder
for file_name in different_files:
    txt_path = os.path.join(txt_folder, f"{file_name}.txt")


    # Check if file exists in txt_folder and move if it's different
    if file_name in txt_files and os.path.exists(txt_path):
        print("Tere is a unique file named : ", file_name)
        shutil.move(txt_path, different_folder)


print("Files have been moved to the 'different_files' folder.")