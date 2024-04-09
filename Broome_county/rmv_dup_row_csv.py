import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("Extracted_data.csv", delimiter='\t')

# Identify duplicate rows based on all columns
duplicate_rows = df[df.duplicated()]

if len(duplicate_rows) > 0:
    print("Duplicate rows found. Removing them...")
    # Drop duplicate rows
    df = df.drop_duplicates()
    # Write the DataFrame back to a CSV file
    df.to_csv("your_file_without_duplicates.csv", sep='\t', index=False)
    print("Duplicate rows removed. Updated file saved.")
else:
    print("No duplicate rows found.")
