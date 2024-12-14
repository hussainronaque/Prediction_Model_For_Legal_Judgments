import csv

# Path to the input CSV file
input_file = 'input_url.csv'
# Path to the output CSV file
output_file = 'filtered_urls.csv'

# Open the input CSV file in read mode
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    # Create a CSV reader
    reader = csv.reader(infile)
    
    # Read all rows into a list
    rows = list(reader)
    
    # Filter the rows where the URL starts with 'https://caselaw.shc.gov.pk/caselaw/view-file'
 
    filtered_rows = [row for row in rows if len(row) > 0 and row[0].startswith("https://caselaw.shc.gov.pk/caselaw/view-file")]

# Open the output CSV file in write mode
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    # Create a CSV writer
    writer = csv.writer(outfile)
    
    # Write the filtered rows to the output file
    writer.writerows(filtered_rows)

print(f"Filtered URLs saved to {output_file}")




