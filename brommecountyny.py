import requests
import csv

# URL of the API endpoint
url = "https://gis.broomecountyny.gov/arcgis/rest/services/parcels/br_parcels/MapServer/identify"

# Set to store unique IDs
unique_ids = set()

# Open CSV file in write mode
with open('extracted_data_summa.csv', mode='a', newline='') as csv_file:
    fieldnames = ['ID', 'NAME', 'ADDRESS', 'LANDUSE']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write CSV header
    writer.writeheader()

    # Define the step size for the grid
    step = 100

    # Define the initial x value
    x = 1151563.622417932
    y=729761.7386886613

    # Increment x until it reaches the maximum value
    while x <=  1151663.622417932:
        # Parameters for the API request
        params = {
            "f": "json",
            "tolerance": 3,
            "returnGeometry": True,
            "returnFieldName": False,
            "returnUnformattedValues": False,
            "imageDisplay": "1532,281,96",
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
                extracted_data.append({
                    "ID": attributes.get("ID"),
                    "NAME": attributes.get("NAME"),
                    "ADDRESS": attributes.get("ADDRESS"),
                    "LANDUSE": attributes.get("LANDUSE")
                })
                ID = attributes.get("ID")
                if ID not in unique_ids:
                    writer.writerow({
                        'ID': ID,
                        'NAME': attributes.get("NAME"),
                        'ADDRESS': attributes.get("ADDRESS"),
                        'LANDUSE': attributes.get("LANDUSE")
                    })
                    unique_ids.add(ID)
            print(extracted_data)
        else:
            print("Failed to retrieve data from the API")

        # Increment x by step
        x += step
        csv_file.flush()
        if x > 1151663.622417932:
            x=950095.4897688426
            y+=step
        if y>801669.4572406365:
            break

print("Data extraction and saving to CSV complete.")
