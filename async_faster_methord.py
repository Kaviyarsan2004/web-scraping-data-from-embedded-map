import csv
import asyncio
import aiohttp

# URL of the API endpoint
url = "https://gis.broomecountyny.gov/arcgis/rest/services/parcels/br_parcels/MapServer/identify"

# Set to store unique IDs
unique_ids = set()

# Load existing IDs from the CSV file
with open('extracted_data_summa.csv', mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        unique_ids.add(row['ID'])

# Open CSV file in append mode
with open('extracted_data_summa.csv', mode='a', newline='') as csv_file:
    fieldnames = ['ID', 'NAME', 'ADDRESS', 'LANDUSE']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Define the step size for the grid
    step_x = 200
    step_y = 150

    # Define the initial x value
    x = 992295.4897688426

    # Define the maximum values for x and y
    max_x = 1151663.622417932
    max_y = 801669.4572406365

    async def fetch_data(session, x, y):
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
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
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
                return extracted_data
        except Exception as e:
            print(f"Failed to fetch data for ({x}, {y}): {e}")
            return []

    async def main():
        y = 730611.7386886613  # Define the initial y value
        async with aiohttp.ClientSession() as session:
            tasks = []
            while y <= max_y:
                x_val = x
                while x_val <= max_x:
                    tasks.append(fetch_data(session, x_val, y))
                    x_val += step_x
                y += step_y
            await asyncio.gather(*tasks)

    asyncio.run(main())

print("Data extraction and saving to CSV complete.")
