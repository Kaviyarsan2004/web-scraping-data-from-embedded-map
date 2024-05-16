import requests
import csv

def fetch_all_parcel_data():
    base_url = "https://maps2.cattco.org/arcgiswebadaptor/rest/services/ParcelandSales_Viewer/MapServer/3/query"

    all_features = []
    start = 0
    batch_size = 1000  

    while True:
        params = {
            "f": "json",
            "returnGeometry": True,
            "spatialRel": "esriSpatialRelIntersects",
            "geometry": '{"xmin":-17299100,"ymin":-47344700,"xmax":137250050.35703713,"ymax":137250050.35703713,"spatialReference":{"wkid":102717}}',
            "geometryType": "esriGeometryEnvelope",
            "inSR": 102717,
            "outFields": "*",
            "outSR": 102100,
            "resultType": "tile",
            "quantizationParameters": '{"mode":"view","originPosition":"upperLeft","tolerance":611.4962262812505,"extent":{"xmin":-17299100,"ymin":-47344700,"xmax":137250050.35703713,"ymax":137250050.35703713,"spatialReference":{"wkid":102717}}}',
            "returnIdsOnly": False,
            "returnCountOnly": False,
            "resultOffset": start,
            "resultRecordCount": batch_size
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            features = data.get('features', [])
            if not features:
                break  
            all_features.extend(features)
            start += batch_size
        else:
            print("Error:", response.status_code)
            return None

    return all_features

def save_to_csv(features):
    if not features:
        print("No data to save.")
        return

    with open('parcel_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(features[0]['attributes'].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        for i, feature in enumerate(features, 1):
            attributes = feature.get('attributes', {})
            writer.writerow(attributes)
            count += 1
            if i % 1000 == 0:
                print(f"Processed {count} records")
    print("Data saved to parcel_data.csv")

if __name__ == "__main__":
    all_features = fetch_all_parcel_data()
    if all_features:
        save_to_csv(all_features)
