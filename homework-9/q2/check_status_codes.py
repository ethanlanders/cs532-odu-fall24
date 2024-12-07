import requests

# Read the URI mapping from the URI mapping file
uris = {}
with open('homework-9/q2/uri_mapping.txt', 'r') as file:
    for line in file:
        # Split the line by the colon to separate the filename and URI
        filename, uri = line.split(': ', 1)
        uris[filename.strip()] = uri.strip()

# Check the status code for each URI
for filename, uri in uris.items():
    try:
        response = requests.get(uri, allow_redirects=True)
        if response.status_code != 200:
            print(f'URI {uri} (filename: {filename}) returned status code {response.status_code}')
            print("Not all URIs returned a '200 OK' response.")
            break  # Exit the loop as soon as a non-200 response is encountered
    except requests.RequestException as e:
        print(f'Error with URI {uri} (filename: {filename}): {e}')
        print("Not all URIs returned a '200 OK' response.")
        break  # Exit the loop is there is an exception

else:  # This block runs only if the loop completes without encountering a break
    print("All URIs returned a '200 OK' response.")