import os
import shutil

def split_files(input_folder, output_folder, chunk_size=150):
    # Get list of all files in the input folder
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    

   
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Split files into chunks and move them to new folders
    chunk_index = 1
    for i in range(0, len(files), chunk_size):
        chunk_files = files[i:i + chunk_size]
        chunk_folder = os.path.join(output_folder, f'chunk_{chunk_index}')
        
        # Check if the chunk folder already has 150 files
        while os.path.exists(chunk_folder) and len(os.listdir(chunk_folder)) >= chunk_size:
            chunk_index += 1
            chunk_folder = os.path.join(output_folder, f'chunk_{chunk_index}')
        
        os.makedirs(chunk_folder, exist_ok=True)
        
        for file in chunk_files:
            try:
                shutil.move(os.path.join(input_folder, file), os.path.join(chunk_folder, file))
            except FileNotFoundError as e:
                print(f"Error moving file {file}: {e}")

if __name__ == "__main__":
    input_folder = 'ocr_output'  # Replace with the path to your input folder
    output_folder = 'weekly-judgements'  # Replace with the path to your output folder
    split_files(input_folder, output_folder)