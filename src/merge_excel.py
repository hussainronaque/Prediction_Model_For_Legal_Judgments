import pandas as pd
import os

# Define the path to the folder containing the .xlsx files
folder_path = 'C:\\Users\\hp-15\\Disc D\\University Files\\fifth semester\\DL\\Deep_Learning_Project\\web_scraper\\data_04'
output_file = 'data4.xlsx'

# List to hold the data from each file
data_frames = []

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is an Excel file
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read the Excel file and select only the required columns
        df = pd.read_excel(file_path, usecols=['scenario', 'witnesses', 'judgment'])
        
        # Append the dataframe to the list
        data_frames.append(df)

# Concatenate all dataframes in the list
merged_df = pd.concat(data_frames, ignore_index=True)

# Write the merged data to a new Excel file
merged_df.to_excel(output_file, index=False)

print(f"All files merged successfully into {output_file}")
