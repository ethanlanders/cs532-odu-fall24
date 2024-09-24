"""
References:
- Python Hashing: https://www.geeksforgeeks.org/md5-hash-python/
"""

import requests
import hashlib
import os
import shutil

uris=[]

# Read the uris.txt file generated from Homework 1
with open("homework-1/output/uris.txt", 'r', encoding='utf-8') as file:
    uris = file.readlines()

# Clean up the URIs by stripping any extra whitespace/newline characters
uris = [uri.strip() for uri in uris]

print(f"Loaded {len(uris)} URIs.\n")

uri_hash_map = {}

if os.path.exists('homework-2/raw_html'):
    print("raw_html directory exists. Deleting all files within it.\n")
    shutil.rmtree('homework-2/raw_html')

os.makedirs("homework-2/raw_html")

for uri in uris:
    hash_object = hashlib.md5(uri.encode())
    filename = f"{hash_object.hexdigest()}.html"

    try:
        response = requests.get(uri, timeout=5)
        with open(f"homework-2/raw_html/{filename}", 'w', encoding='utf-8') as file:
            file.write(response.text)

        uri_hash_map[filename] = uri

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {uri}: \n{e}\n")

with open('homework-2/uri_mapping.txt', 'w', encoding='utf-8') as f:
    for filename, uri in uri_hash_map.items():
        f.write(f"{filename}: {uri}\n")

print("HTML files and URI mappings have been successfully saved.\n")