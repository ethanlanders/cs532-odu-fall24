import subprocess # https://docs.python.org/3/library/subprocess.html
import time
import os

path = "homework-1/output/uris.txt"

def load_uri_mapping(mapping_file):
    uri_hash_mapping = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            hash_file, uri = line.split(': ', 1)
            uri_hash_mapping[hash_file.strip()] = uri.strip()
    return uri_hash_mapping

def query_memgator(uri, output_file):
    command = f"./memgator -c 'ODU CS 532 eland007@odu.edu -a archives.json -f JSON {uri}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    with open(output_file, 'w') as f:
        f.write(result.stdout.decode('utf-8'))

    # Add sleep to avoid overwhelming the server
    time.sleep(10)

def download_timemap(uri_mapping_file, output_dir):
    uri_hash_map = load_uri_mapping(uri_mapping_file)

    # Limit to first 3 items for testing
    test_uri_hash_map = dict(list(uri_hash_map.items())[:3])

    for hash_file, uri in test_uri_hash_map.items():
        output_file = os.path.join(output_dir, f"{hash_file}.json")
        print(f"Querying TimeMap for {uri} and saving as {output_file}")
        query_memgator(uri, output_file)

download_timemap("homework-2/uri_mapping.txt", "homework-3/timemaps")