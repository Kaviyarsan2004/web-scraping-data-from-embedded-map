import requests
import csv

# API URL
url = "https://spatialags.vhb.com/arcgis/rest/services/29822_Delaware/NY_County_Delaware2/MapServer/25/query"

# Parameters
params = {
    "f": "json",
    "returnGeometry": False,  # Exclude geometry
    "where": "1=1",  # Retrieve all features
    "outFields": "*",  # Retrieve all fields
    "outSR": 4326,  # Spatial reference (WGS84)
    "resultOffset": 0,  # Start from the first record
    "resultRecordCount": 3000  # Number of records to retrieve per request
}

# CSV file path
csv_file = "attributes.csv"

# Pagination loop
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = None  # Initialize CSV writer

    # Loop to retrieve all data
    while True:
        # Make the request
        response = requests.get(url, params=params)

        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            # Extract features
            if "features" in data:
                features = data["features"]

                # Write attributes for each feature
                for feature in features:
                    attributes = feature["attributes"]

                    # Initialize CSV writer if not already initialized
                    if writer is None:
                        # Set fieldnames based on the first response attributes
                        fieldnames = list(attributes.keys())
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()

                    # Write attributes to CSV
                    writer.writerow(attributes)

                # Flush the data to the file
                file.flush()

                # Update offset for next request
                params["resultOffset"] += len(features)

                # Print number of data collected
                print("Number of data collected:", params["resultOffset"])

                # Check if all records are collected
                if len(features) < params["resultRecordCount"]:
                    break
            else:
                break  # No more features found
        else:
            print("Error:", response.status_code)
            break

print("Attributes saved to:", csv_file)
