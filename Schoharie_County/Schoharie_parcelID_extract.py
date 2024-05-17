import requests
import csv

url = "https://spatialags.vhb.com/arcgis/rest/services/20327_Schoharie/NY_County_Schoharie2/MapServer/5/query"


params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json"
}

def fetch_and_save_data():
    
    offset = 0
    chunk_size = 1000
    total_records = 0

    with open("schoharie_parcels.csv", "w", newline="", encoding="utf-8") as csvfile:
       
        response = requests.get(url, params=params)
        data = response.json()
        
        fieldnames = list(data["features"][0]["attributes"].keys())
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        while True:
            params["resultOffset"] = offset
            params["resultRecordCount"] = chunk_size
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "features" not in data or len(data["features"]) == 0:
                break
            
            for feature in data["features"]:
                writer.writerow(feature["attributes"])
            
            total_records += len(data["features"])
            offset += chunk_size
            
            print("Number of data collected:", total_records)
    
    print("Data collection completed.")

fetch_and_save_data()
