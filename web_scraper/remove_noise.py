import pandas as pd

# Load the Excel file
file_path = "/Users/hussainronaque/Documents/GitHub/Deep_Learning_Project/web_scraper/data1.xlsx"  # Replace with the path to your file
df = pd.read_excel(file_path)

# Check if column D exists and has any values
if 'D' in df.columns:
    # Filter out rows where column D contains the letter "k"
    df = df[~df['D'].astype(str).str.contains('k', case=False, na=False)]
else:
    print("Column D does not exist in the file.")

# Save the modified DataFrame to a new Excel file
df.to_excel("modified_file.xlsx", index=False)
print("Rows containing 'k' in column D have been removed.")
