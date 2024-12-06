def load_uri_mapping(mapping_file):
    """
    Load the URI to hash mapping from a given file. Each line of the file should contain
    a hash and a URI separated by a ': '.

    Args:
        mapping_file (str): Path to the mapping file.

    Returns:
        dict: A dictionary where the keys are hash filenames and the values are URIs.
    """
    uri_hash_mapping = {} # Initialze an empty dictionary to store the hash-URI mapping.

    with open(mapping_file, 'r') as f:
        # Process each line of the file to extract the hash and URI.
        for line in f:
            hash_file, uri = line.split(': ', 1) # Split the line by the first ': ' found.
            uri_hash_mapping[hash_file.strip()] = uri.strip() # Remove any extra spaces and store.

    return uri_hash_mapping # Return the dictionary of hash-URI pairs.
