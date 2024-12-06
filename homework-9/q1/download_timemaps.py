import subprocess # Module to run external commands and interact with the system shell.
import time # Module to add delays (for pausing between requests)
import os # Module for interacting with the file system.

from utils import load_uri_mapping

def query_memgator(uri, output_file):
    """
    Query MemGator for a TimeMap corresponding to a given URI and save the result.
    """
    # Command to run MemGator with relevant parameters.
    command = f"~/MemGator/memgator -c 'ODU CS532 eland007@odu.edu' -a ~/MemGator/docs/archives.json -f JSON {uri}"
    
    try:
        # Run the command in a subprocess and capture the output, both stdout and stderr.
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=180)
        
        # Check if the command was successful by checking the return code.
        if result.returncode != 0:
            print(f"Error querying MemGator for {uri}: {result.stderr}") # Output error if command fails.
        else:
            # Print raw output for debugging and verification purposes.
            if result.stdout:
                print(f"TimeMap for {uri}: {result.stdout}") # Print the result if TimeMap is found.
            else:
                print(f"No TimeMap for {uri}.") # Notify if no TimeMap is returned.

            # Write the result to the specified output file (in JSON format).
            with open(output_file, 'w') as f:
                f.write(result.stdout)
    
    except subprocess.TimeoutExpired:
        # If the query takes longer than 180 seconds, output a timeout message.
        print(f"Query for {uri} timed out after 180 seconds.")

    # Pause for 10 seconds between queries to avoid server overload.
    time.sleep(10)

def download_timemap(uri_mapping_file, output_dir):
    """
    Download TimeMaps for URIs listed in a mapping file, saving them to a specified directory.

    Args:
        uri_mapping_file (str): Path to the file containing URI-to-hash mappings.
        output_dir (str): Directory to save the TimeMap JSON files.
    """
    # Ensure output directory exists (create it if it doesn't).
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the URI-hash mapping from the provided file.
    uri_hash_map = load_uri_mapping(uri_mapping_file)

    # Initialize a counter for tracking progress.
    uri_count = 1

    # Loop through each hash and URI pair to download the TimeMap.
    for hash_file, uri in uri_hash_map.items():
        output_file = os.path.join(output_dir, f"{hash_file}.json") # Define the output file path.
        print(f"\nURI {uri_count}\nQuerying TimeMap for {uri} and saving as {output_file}")
        query_memgator(uri, output_file) # Query MemGator and save the result.
        uri_count += 1 # Increment the counter for the next URI.

# Start the process by providing the URI mapping file and output directory
download_timemap("homework-2/uri_mapping.txt", "homework-9/q1/timemaps")