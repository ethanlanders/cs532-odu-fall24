import requests
import json
from collections import Counter

# Read the URI mapping from the URI mapping file
uris = {} 
with open('homework-9/q2/uri_mapping.txt', 'r') as file:
    for line in file:
        # Split the line by the colon to separate the filename and URI
        filename, uri = line.split(': ', 1)
        uris[filename.strip()] = uri.strip()

# Dictionary to store the status codes
status_codes = {}
response_counts = Counter()

# Check the status code for each URI
for filename, uri in uris.items():
    try:
        response = requests.get(uri, allow_redirects=True, timeout=10)
        status_codes[filename] = response.status_code

        # Print non-200 responses for awareness
        if response.status_code == 200:
            response_counts["200_OK"] += 1
        else:
            response_counts["non_200"] += 1
            print(f'URI {uri} (filename: {filename}) returned status code {response.status_code}')

    except requests.RequestException as e:
        status_codes[filename] = f"Error: {e}"
        print(f'Error with URI {uri} (filename: {filename}): {e}')
        response_counts["non_200"] += 1

# Save the status codes to a file for later use
output_file = 'homework-9/q2/status_codes.json'
with open(output_file, 'w') as f:
    json.dump(status_codes, f, indent = 4)
print(f"Status codes saved to {output_file}")

# Print summary
print(f"\nSummary of Responses")
for category, count in response_counts.items():
    print(f"{category}: {count}")