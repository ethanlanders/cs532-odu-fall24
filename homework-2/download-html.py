"""
References:
- Python Hashing: https://www.geeksforgeeks.org/md5-hash-python/
- Python shutil.rmtree() Method: https://www.geeksforgeeks.org/delete-an-entire-directory-tree-using-python-shutil-rmtree-method/
"""

import requests
import hashlib
import os
import shutil

uris=[]

# Read the list of URIs from a file called uris.txt file
# located in the ouptut folder of homework-1
with open("homework-1/output/uris.txt", 'r', encoding='utf-8') as file:
    uris = file.readlines()

# Remove extra spaces or newline characters from each URI
uris = [uri.strip() for uri in uris]

print(f"Loaded {len(uris)} URIs.\n")

uri_hash_map = {}

# If the raw_html directory already exists from a previous run,
# it deletes the folder and all its contents
if os.path.exists('homework-2/raw_html'):
    print("raw_html directory exists. Deleting all files within it.\n")
    shutil.rmtree('homework-2/raw_html')

# Create a new raw_html directory to store the downloaded HTML files
os.makedirs("homework-2/raw_html")

# For each URI, the script generates an MD5 hash to use as the filename,
# downloads the corresponding HTML content, and saves it to a file
for uri in uris:
    hash_object = hashlib.md5(uri.encode())
    filename = f"{hash_object.hexdigest()}.html"

    try:
        # Fetches the HTML content from the URI
        response = requests.get(uri, timeout=5)
        # Writes the HTML content to a file using the hash as the filename
        with open(f"homework-2/raw_html/{filename}", 'w', encoding='utf-8') as file:
            file.write(response.text)

        # Saves the URI-to-hash mapping in a dictionary for future reference
        uri_hash_map[filename] = uri

    except requests.exceptions.RequestException as e:
        # Handles exceptions that may occur during the request (e.g. timeouts, connection errors)
        print(f"Error fetching {uri}: \n{e}\n")

# Write the mapping of the HTML file names (hashes) to the original URIs in uri_mapping.txt
with open('homework-2/uri_mapping.txt', 'w', encoding='utf-8') as f:
    for filename, uri in uri_hash_map.items():
        f.write(f"{filename}: {uri}\n")

print("HTML files and URI mappings have been successfully saved.\n")