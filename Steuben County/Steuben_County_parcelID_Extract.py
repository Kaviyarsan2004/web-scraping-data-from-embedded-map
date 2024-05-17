import requests
import csv


fieldnames = [
    "FID", "PIN", "Type", "PA_KEY_NO", "PRINTKEY", "TM_OWNAM", 
    "TM_MAILAD1", "TM_MAILAD2", "TM_SWIS", "TM_ASSES_U", 
    "TM_RECLIB", "TM_RECPG", "TM_RECDATE", "ADDITL_DEE", 
    "TM_FILE_NO", "FIRE_NBR", "FIRE_A", "TM_RDSTRT", 
    "PA_FRONT", "PA_DEPTH", "PA_ACRES", "TM_CALC", 
    "GIS_SCHDIS", "Shape__Area", "Shape__Length"
]

def fetch_and_save_batch(url, params, csvfile, unique_entries):
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        features = data.get("features", [])
        for feature in features:
            attributes = feature.get("attributes", {})
            print("PRINTKEY:", attributes.get("PRINTKEY"))
            print("TM_OWNAM:", attributes.get("TM_OWNAM"))
            print() 
            if attributes["PRINTKEY"] not in unique_entries:
                unique_entries.add(attributes["PRINTKEY"]) 
                writer.writerow(attributes)
        
        return data.get("exceededTransferLimit", False)
    else:
        print("Request failed with status code:", response.status_code)
        return False

def fetch_all_features(url, params):
    with open('map_data.csv', 'w', newline='', encoding='utf-8') as csvfile:  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        unique_entries = set()  
        
        while True:
            if not fetch_and_save_batch(url, params, csvfile, unique_entries):
                break
            params["resultOffset"] = params.get("resultOffset", 0) + 1000


url = "https://services2.arcgis.com/NZkLeERo9XICXiuy/arcgis/rest/services/Real_Property_Parcel_Viewer/FeatureServer/1/query"


params = {
    "f": "json",  
    "returnGeometry": "false",
    "spatialRel": "esriSpatialRelIntersects",
    "geometry": '{"xmin":-20037700,"ymin":-30241100,"xmax":20037700,"ymax":30241100,"spatialReference":{"wkid":102100}}',
    "geometryType": "esriGeometryEnvelope",
    "inSR": 102100,
    "outFields": ",".join(fieldnames),
    "returnCentroid": "false",
    "returnExceededLimitFeatures": "true",  
    "outSR": 102100,
    "resultType": "tile",
    "quantizationParameters": '{"mode":"view","originPosition":"upperLeft","tolerance":9.55462853564454,"extent":{"xmin":-20037700,"ymin":-30241100,"xmax":20037700,"ymax":30241100,"spatialReference":{"wkid":102100,"_geVersion":{"pp":"","ou":null,"gg":102100,"Ho":-1,"$H":-1,"wh":null}}}}'
}

fetch_all_features(url, params)
