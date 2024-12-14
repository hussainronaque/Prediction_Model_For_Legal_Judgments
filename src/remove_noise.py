import pandas as pd

# Load the Excel file
file_path = "/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/data2.xlsx"
df = pd.read_excel(file_path)

# Define the expanded list of keywords related to crime
keywords = [
    "murder", "rape", "assault", "robbery", "theft", "kidnapping", "fraud",
    "homicide", "manslaughter", "burglary", "arson", "extortion", "embezzlement",
    "domestic violence", "child abuse", "sexual harassment", "drug trafficking",
    "cybercrime", "terrorism", "stalking", "human trafficking", "identity theft",
    "vandalism", "bribery", "corruption", "firing", "fired", "pistol", "injured", "injuries"
]

# Check if the "scenario" column exists
if 'scenario' in df.columns:
    # Filter rows where the "scenario" column contains any of the specified keywords
    df = df[df['scenario'].astype(str).str.contains('|'.join(keywords), case=False, na=False)]
else:
    print("Column 'scenario' does not exist in the file.")

# Save the filtered DataFrame back to the original file
df.to_excel(file_path, index=False)
print("Filtered rows based on 'scenario' column and saved back to the original file.")