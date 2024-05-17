import requests
import csv


url = "https://services5.arcgis.com/WcotYUBrYwlGLzUr/ArcGIS/rest/services/Alleg_County_Parcels_2023_Web84/FeatureServer/0/query"


params = {
    "where": "1=1", 
    "outFields": "*",  
    "returnGeometry": "false",  
    "f": "json",  
    "resultRecordCount": 2000, 
    "resultOffset": 0  
}

try:
    
    csv_filename = "parcels_data.csv"

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = None

        while True:
            response = requests.get(url, params=params)
            data = response.json()

            if 'features' in data and len(data['features']) > 0:
    
                if csv_writer is None:
                   
                    field_names = list(data['features'][0]['attributes'].keys())
                    csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    csv_writer.writeheader()

                for feature in data['features']:
                    attributes = feature['attributes']

                    csv_writer.writerow(attributes)

                print(f"{params['resultOffset']} records collected.")

                params['resultOffset'] += 2000

            else:
                print("All records collected.")
                break

    print(f"Data saved to {csv_filename}")

except Exception as e:
    print("An error occurred:", e)
