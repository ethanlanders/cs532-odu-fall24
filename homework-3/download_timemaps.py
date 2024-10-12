import subprocess # https://docs.python.org/3/library/subprocess.html
import time
import os

def load_uri_mapping(mapping_file):
    uri_hash_mapping = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            hash_file, uri = line.split(': ', 1)
            uri_hash_mapping[hash_file.strip()] = uri.strip()
    return uri_hash_mapping

def query_memgator(uri, output_file):
    command = f"~/MemGator/memgator -c 'ODU CS532 eland007@odu.edu' -a ~/MemGator/docs/archives.json -f JSON {uri}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=180)
        
        # Checks for errors in querying MemGator
        if result.returncode != 0:
            print(f"Error querying MemGator for {uri}: {result.stderr}")
        else:
            # Print raw output for debugging purposes
            if result.stdout:
                print(f"TimeMap for {uri}: {result.stdout}")
            else:
                print(f"No TimeMap for {uri}.")

            # Save the stdout to the output file
            with open(output_file, 'w') as f:
                f.write(result.stdout)
    
    except subprocess.TimeoutExpired:
        print(f"Query for {uri} timed out after 180 seconds.")

    # Sleep to avoid overwhelming the MemGator server
    time.sleep(10)

def download_timemap(uri_mapping_file, output_dir, start):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the URI and hash mappings from the file
    uri_hash_map = load_uri_mapping(uri_mapping_file)

    # Limit to URIs from 50 onwards
    test_uri_hash_map = dict(list(uri_hash_map.items())[start:])

    for hash_file, uri in test_uri_hash_map.items():
        output_file = os.path.join(output_dir, f"{hash_file}.json")
        print(f"\nURI {start}\nQuerying TimeMap for {uri} and saving as {output_file}")
        query_memgator(uri, output_file)
        start += 1

# Begin the process with the appropriate files
download_timemap("homework-2/uri_mapping.txt", "homework-3/timemaps", 266)