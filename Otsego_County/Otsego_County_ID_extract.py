import requests
import csv


fieldnames = [
    "UNIQUE_ID", "OWNER_NAME", "ACRES", "HOUSE_NO", "STREET",
    "GIS_LINK", "LOCATION", "IMAGE_LINK", "MBL", "X", "Y",
    "LAT", "LON", "TOWN", "SCHDISTR", "MBL2"
]

def fetch_and_save_all_parcel(url, params, csvfile):
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    total_fetched = 0
    
    while True:
        print("Fetching parcels. Total fetched:", total_fetched)
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
                   
            features = data.get("features", [])
            for feature in features:
                attributes = feature.get("attributes", {})
                writer.writerow(attributes)
                total_fetched += 1
            
            has_more = data.get("exceededTransferLimit", False)
            if has_more:
                params["resultOffset"] = total_fetched
            else:
                break  
        else:
            print("Request failed with status code:", response.status_code)
            return False
    
    print("All parcel data fetched and saved to CSV. Total:", total_fetched)
    return True

def main():
    url = "https://server1.mapxpress.net/arcgis/rest/services/Otsego/Parcels_I/MapServer/0/query"
    

    params = {
        "f": "json",
        "where": "",
        "returnGeometry": "true",
        "spatialRel": "esriSpatialRelIntersects",
        "geometry": '{"xmin":0,"ymin":1100000,"xmax":500000,"ymax":1500000,"spatialReference":{"wkid":2260}}',
        "geometryType": "esriGeometryEnvelope",
        "inSR": 2260,
        "outFields": ",".join(fieldnames),
        "outSR": 2260,
        "resultOffset": 0
    }

    with open('Otsego_County_parcel_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fetch_and_save_all_parcel(url, params, csvfile)

if __name__ == "__main__":
    main()
