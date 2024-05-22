import requests
import csv

url = "https://services9.arcgis.com/AzdpqVmJ5GjGWCoI/ArcGIS/rest/services/FranklinCoVA_TaxParcels_View/FeatureServer/0/query"
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
        
        params["resultOffset"] += params["resultRecordCount"]
    else:
        print(f"Error: {response.status_code}")
        break

if all_features:
    field_names = list(all_features[0]['attributes'].keys())

    with open('Franklin_County_Parcels.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(field_names)
        for feature in all_features:
            row = [feature['attributes'].get(field, "") for field in field_names]
            writer.writerow(row)
    
    print("Data has been written to Orleans Wyoming_County_parcel.csv")
else:
    print("No data retrieved")
