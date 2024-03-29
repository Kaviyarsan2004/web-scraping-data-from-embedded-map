import requests
import csv
import random

# URL of the API endpoint
url = "https://gis.broomecountyny.gov/arcgis/rest/services/parcels/br_parcels/MapServer/identify"

# Set to store unique IDs
unique_ids = set()

# Define the range
start_range_x = 100  # Start of the range (inclusive)
end_range_x = 200    # End of the range (exclusive)

# Generate a random number within the range
random_number_x = random.uniform(start_range_x, end_range_x)

# Define the range
start_range_y = 100  # Start of the range (inclusive)
end_range_y = 200    # End of the range (exclusive)

# Generate a random number within the range
random_number_y = random.uniform(start_range_x, end_range_x)

# Load existing IDs from the CSV file
with open('extracted_data_summa.csv', mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        unique_ids.add(row['ID'])

# Open CSV file in append mode
with open('extracted_data_summa_1.csv', mode='a', newline='') as csv_file:
    fieldnames = ['FID', 'ID', 'NAME', 'ADDRESS', 'ZIP', 'MUNI', 'MAIL_ADDR', 'MAIL_CITY', 'LANDUSE', 'LAT', 'LONG', 'SWISID', 'TAXMAP', 'LOCATION']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write CSV header
    # writer.writeheader()

    # Define the step size for the grid
    step_x = random_number_x
    step_y=random_number_y


    # Define the initial x & y value
    x =1062310.6985232728
    y=767545.505026855
    # Increment x until it reaches the maximum value
    while x <=  1151663.622417932:
        image_display = "1532,281,96"
        # Parameters for the API request
        params = {
            "f": "json",
            "tolerance": 3,
            "returnGeometry": True,
            "returnFieldName": False,
            "returnUnformattedValues": False,
            "imageDisplay": image_display,
            "geometry": f'{{"x":{x},"y":{y}}}',
            "geometryType": "esriGeometryPoint",
            "sr": 2261,
            "mapExtent": "925027.4817693165,728504.2332269327,1152879.2787740831,888564.4768391979",
            "layers": "all:1,14,16,9"
        }

        # Send GET request to the API
        response = requests.get(url, params=params)

        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            extracted_data = []
            for result in data.get("results", []):
                attributes = result.get("attributes", {})
                ID = attributes.get("ID")
                if ID not in unique_ids:
                    print("ID:", ID)
                    print("Name:", attributes.get("NAME"))
                    print("Address:", attributes.get("ADDRESS"))
                    print("Landuse:", attributes.get("LANDUSE"))
                    print()  # Add a blank line for clarity
                    writer.writerow({
                        'FID': attributes.get("FID"),
                        'ID': attributes.get("ID"),
                        'NAME': attributes.get("NAME"),
                        'ADDRESS': attributes.get("ADDRESS"),
                        'ZIP': attributes.get("ZIP"),
                        'MUNI': attributes.get("MUNI"),
                        'MAIL_ADDR': attributes.get("MAIL_ADDR"),
                        'MAIL_CITY': attributes.get("MAIL_CITY"),
                        'LANDUSE': attributes.get("LANDUSE"),
                        'LAT': attributes.get("LAT"),
                        'LONG': attributes.get("LONG"),
                        'SWISID': attributes.get("SWISID"),
                        'TAXMAP': attributes.get("TAXMAP"),
                        'LOCATION': attributes.get("LOCATION"),
                    })
                    unique_ids.add(ID)
            print(x)
            print(y)
            print()
        else:
            print("Failed to retrieve data from the API")

        # Increment x by step
        x += step_x
        csv_file.flush()
        if x > 1137023.3364511523:
            x=950095.4897688426
            y+=step_y
        if y>801669.4572406365:
            break

print("Data extraction and saving to CSV complete.")
