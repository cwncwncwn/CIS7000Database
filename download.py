from pymongo import MongoClient
import base64
import json
from bson.binary import Binary
import gridfs
import os
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('assetName', type=str, help='The name of the asset')
parser.add_argument('--maya', action='store_true')
args = parser.parse_args()

# MongoDB URI and database/collection names
uri = "<your uri, see readme.md>"
db_name = "CIS7000"
collection_name = "Week5"

# Connect to MongoDB
client = MongoClient(uri)
db = client[db_name]
collection = db[collection_name]
fs = gridfs.GridFS(db)

asset_name = args.assetName
# Query the collection for the asset name
document = collection.find_one({"metadata.assetName": asset_name})

if document:
    directory_path = f"{asset_name}\\"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # If a document is found, print its ID
    file_path = f"{asset_name}\\metadata.json"
    metadata = document["metadata"]
    with open(file_path, "w") as json_file:
        json.dump(metadata, json_file)

    if "image" in document:
        image_data = document["image"]
        file_path = f"{asset_name}\\thumb.png"
        with open(file_path, "wb") as image_file:
            image_file.write(image_data)
    
    for i in range(3):
        lod_key = f"LOD{i}"
        if lod_key in document:
            file_id = document[lod_key]
            
            # Retrieve the file from GridFS using its file ID
            grid_out = fs.get(file_id)
            
            # Construct the file path where you want to save the LOD file
            file_path = f"{asset_name}\\{asset_name}{lod_key}.usda"
            
            # Write the file data to a new file
            with open(file_path, 'wb') as output_file:
                output_file.write(grid_out.read())

    if "usda" in document:
        usda_data = document["usda"]
        file_path = f"{asset_name}\\{asset_name}.usda"
        with open(file_path, "w") as usda_file:
            usda_file.write(usda_data)

    if "mayaASCII" in document:
        maya_ascii_data = document["mayaASCII"] 
        file_path = f"{asset_name}\\{asset_name}.ma"
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(maya_ascii_data)) 

        if args.maya:
            maya_executable_path = "C:\\Program Files\\Autodesk\\Maya2024\\bin\\maya.exe"
            subprocess.Popen([maya_executable_path, file_path])
else:
    # If no document is found, handle accordingly
    print(f"No document found for asset '{asset_name}'.")
