import requests
import csv

# Define the API URL
url = "https://spatialags.vhb.com/arcgis/rest/services/20327_Schoharie/NY_County_Schoharie2/MapServer/5/query"

# Define parameters for the request
params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json"
}

# Function to fetch data from the API and save it to a CSV file
def fetch_and_save_data():
    # Initialize variables
    offset = 0
    chunk_size = 1000
    total_records = 0
    
    # Open CSV file for writing
    with open("schoharie_parcels.csv", "w", newline="", encoding="utf-8") as csvfile:
        # Send request to the API
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract field names from the first record
        fieldnames = list(data["features"][0]["attributes"].keys())
        
        # Initialize CSV writer with correct field names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write CSV header
        writer.writeheader()
        
        # Fetch data in chunks
        while True:
            # Set offset and limit for the request
            params["resultOffset"] = offset
            params["resultRecordCount"] = chunk_size
            
            # Send request to the API
            response = requests.get(url, params=params)
            data = response.json()
            
            # Check if data is empty or no more records
            if "features" not in data or len(data["features"]) == 0:
                break
            
            # Extract and save attributes to CSV
            for feature in data["features"]:
                # Write attributes to CSV
                writer.writerow(feature["attributes"])
            
            # Update total records count and offset for the next chunk
            total_records += len(data["features"])
            offset += chunk_size
            
            # Print progress
            print("Number of data collected:", total_records)
    
    print("Data collection completed.")

# Call the function to fetch and save data
fetch_and_save_data()
