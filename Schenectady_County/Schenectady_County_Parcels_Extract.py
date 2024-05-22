import requests
import csv

url = "https://spatialags.vhb.com/arcgis/rest/services/29816_SIMS/SIMS_100222/MapServer/6/query"
params = {
    "f": "json",
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "resultOffset": 0,
    "resultRecordCount": 2000  
}

all_features = []

while True:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])

        if not features:
            break
        
        all_features.extend(features)
        
        if len(features) < params["resultRecordCount"]:
            break
        
        params["resultOffset"] += params["resultRecordCount"]
    else:
        print(f"Error: {response.status_code}")
        break

if all_features:
    field_names = list(all_features[0]['attributes'].keys())

    with open('Schenectady_County_Parcels.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(field_names)
        
        for feature in all_features:
            row = [feature['attributes'].get(field, "") for field in field_names]
            writer.writerow(row)
    
    print("Data has been written to Schenectady_County_Parcels.csv")
else:
    print("No data retrieved")
