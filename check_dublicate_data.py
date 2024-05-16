import pandas as pd

df = pd.read_csv('attributesV1.csv')

duplicates = df[df.duplicated()]

if duplicates.empty:
    print("No duplicates found.")
else:
    print("Duplicates found:")
    print(duplicates)
