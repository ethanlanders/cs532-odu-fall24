import requests
import hashlib

uris=[]

# Read the uris.txt file generated from Homework 1
with open("homework-1/output/uris.txt", 'r', encoding='utf-8') as file:
    uris = file.readlines()

# Clean up the URIs by stripping any extra whitespace/newline characters
uris = [uri.strip() for uri in uris]

print(f"Loaded {len(uris)} URIs.")

uri_hash_map = {}