## How do the scripts work?
### Prerequisites
 - Install pymongo library
### Upload.py
 - Change the uri defined in line 14 by your own (after adding you to the database, you should be able to have access to it. Let me know if there are problems!:).
    - Open the database overview site in MongoDB Atlas
    - Click "connect"
    - Click "MongoDB for VSCode"
    - Replace the uri in our script by the link in the 3rd step indicated on the website.
 - Place the script and folder of the asset in the same directory
 - Run `python upload.py <assetName>` and the asset should appear in the database.

 ### Download.py
- Change the uri defined in line 16 by by your own.
 - Run `python download.py <assetName>` and the asset should be downloaded into a separate folder named by assetName under current directory.