import pandas as pd

# Load the CSV file
file_path = 'overlaped_CPA_parcel_Bm.csv'
df = pd.read_csv(file_path)

# Remove duplicate rows
df_cleaned = df.drop_duplicates()

# Save the cleaned data to a new CSV file
output_file_path = 'cleaned_file.csv'
df_cleaned.to_csv(output_file_path, index=False)

print(f"Duplicates removed. Cleaned data saved to {output_file_path}")
