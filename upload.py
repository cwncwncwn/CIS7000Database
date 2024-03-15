from pymongo import MongoClient
import base64
import json
from bson.binary import Binary
import gridfs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('assetName', type=str, help='The name of the asset')
args = parser.parse_args()

directory = "C:\\Users\\wanni\\OneDrive\\Documents\\UPenn\\CIS7000\\HW5\\"
# names = ["kitchenaid", "scissors", "paniniPress"]
uri = "<your uri, see readme.md>"

client = MongoClient(uri)

db = client['CIS7000']  # Replace with your database name
collection = db['Week5']  # Replace with your collection name

name = args.assetName
document = collection.find_one({"metadata.assetName": name})

fs = gridfs.GridFS(db)

if not document:
    json_file_path = directory + name + "\\" + "metadata.json"
    with open(json_file_path, 'r') as json_file:
        metadata = json.load(json_file)

    data = {"metadata": metadata}

    image_path = directory + name + "\\" + "thumb.png"
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base64_encoded_data = base64.b64encode(binary_data)
        binary_field = Binary(binary_data)
        data['image'] = binary_field

    file_path = directory + name + "\\" + name + ".usda"
    with open(file_path, "r") as file:
        data['usda'] = file.read()

    for i in range(3):
        file_path = directory + name + "\\" + name + "LOD" + str(i) + ".usda"
        with open(file_path, "rb") as file:
            file_id = fs.put(file, filename = name + "LOD" + str(i) + ".usda")
            n = "LOD" + str(i)
            data[n] = file_id

    maya_file_path = directory + name + "\\" + name + '.ma'
    with open(maya_file_path, 'rb') as file:
        data['mayaASCII'] = base64.b64encode(file.read()).decode('utf-8')




    # Insert the document
    insert_result = collection.insert_one(data)

    print(f"Document inserted with _id: {insert_result.inserted_id}")
else:
    print("invalid name")