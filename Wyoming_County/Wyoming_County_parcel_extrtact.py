import requests
import csv

# Define the URL and initial parameters
url = "https://services3.arcgis.com/Sq7KUOgahdDkqoAp/ArcGIS/rest/services/online_map_layers/FeatureServer/4/query"
params = {
    "f": "json",
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "resultOffset": 0,
    "resultRecordCount": 1000  # Adjust based on the API's max record count per request
}

# Initialize an empty list to hold all features
all_features = []

while True:
    # Make the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])

        # If no features are returned, break the loop
        if not features:
            break
        
        # Append the retrieved features to the list
        all_features.extend(features)
        
        # Update the resultOffset for the next batch
        params["resultOffset"] += params["resultRecordCount"]
    else:
        print(f"Error: {response.status_code}")
        break

# If features were retrieved, write them to a CSV file
if all_features:
    # Extract field names from the first feature
    field_names = list(all_features[0]['attributes'].keys())

    # Open a CSV file to write
    with open('Wyoming_County_parcel.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(field_names)
        
        # Write the rows
        for feature in all_features:
            row = [feature['attributes'].get(field, "") for field in field_names]
            writer.writerow(row)
    
    print("Data has been written to Orleans Wyoming_County_parcel.csv")
else:
    print("No data retrieved")
