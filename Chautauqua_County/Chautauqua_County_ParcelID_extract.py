import requests
import csv

def fetch_all_parcel_data():
    url = "https://maps.chautauquacounty.com/server/rest/services/Public/Parcel_Test/MapServer/layers"
    params = {"f": "pjson"}
    response = requests.get(url, params=params)
    data = response.json()
    layer_id = data["layers"][0]["id"]
    fields = [field["name"] for field in data["layers"][0]["fields"]]

    parcels = []

    offset = 0
    limit = 1000  

    while True:
        print("Fetching records starting from offset:", offset)
        query_url = f"https://maps.chautauquacounty.com/server/rest/services/Public/Parcel_Test/MapServer/{layer_id}/query"
        query_params = {
            "f": "json",
            "where": "1=1",
            "outFields": ",".join(fields),
            "returnGeometry": "false",
            "resultOffset": offset,
            "resultRecordCount": limit
        }
        query_response = requests.get(query_url, params=query_params)
        query_data = query_response.json()
        parcels.extend(query_data.get("features", []))

        if "exceededTransferLimit" not in query_data:
            break

        offset += limit

    return parcels

def save_to_csv(parcels):
    with open("parcels.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = parcels[0]["attributes"].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for parcel in parcels:
            writer.writerow(parcel["attributes"])

if __name__ == "__main__":
    parcel_data = fetch_all_parcel_data()
    save_to_csv(parcel_data)
