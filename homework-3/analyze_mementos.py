import json
import os
from urllib.parse import urlparse
from prettytable import PrettyTable
from collections import defaultdict

from utils import load_uri_mapping

# ====================== TimeMap Handling Functions ======================

def load_timemap(filepath):
    """
    Load a TimeMap from a JSON file. If the file is empty of has invalid JSON, return None.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict or None: The parsed JSON object (TimeMap) or None if the file is invalid/empty.
    """
    try:
        # Open the file and check if it's empty.    
        with open(filepath, 'r') as file:
            if os.stat(filepath).st_size == 0:
                return None # Return None for empty files.
            return json.load(file) # Load the JSON content.
    except json.JSONDecodeError:
        return None # Return None if JSON is invalid.
    
def analyze_timemaps(timemaps_dir):
    """
    Analyze all TimeMaps in a directory, counting the number of mementos for each.

    Args:
        timemaps_dir (str): The directory path containing TimeMap files.

    Returns:
        dict: A dictionary where the keys are filenames and values are memento counts.
    """
    memento_counts = {} # Dictionary to store the counts for each file.

    # Loop over all files in the directory.
    for filename in os.listdir(timemaps_dir):
        # Load the TimeMap from each file.
        timemap = load_timemap(os.path.join(timemaps_dir, filename))
        # Count the mementos in the TimeMap.
        memento_count = count_mementos(timemap)
        # Store the result in the dictionary.
        memento_counts[filename] = memento_count

    return memento_counts # Return the dictionary of memento counts.

# ======================= Memento Counting Functions =======================

def count_mementos(timemap):
    """
    Count the number of mementos in the given TimeMap.

    Args:
        timemap (dict or None): The TimeMap object. If None, assume no mementos.

    Returns:
        int: The number of mementos (0 if the TimeMap is None).

    """
    if timemap is None:
        return 0    # Return 0 if no valid TimeMap.
    return len(timemap.get('mementos', [])) # Count the mementos in the 'mementos' list.

def count_memento_occurrences(memento_counts):
    """
    Count how many times each specific memento count occurs across all URIs.

    Args:
        memento_counts (dict): A dictionary of memento counts per URI file.

    Returns:
        defaultdict(int): A dictionary where the keys are memento counts, and values are the number of URIs with that count.
    """
    occurrences = defaultdict(int) # Default dictionary to count occurrences of each memento count.

    # Iterate over the memento counts and tally the occurrences.
    for count in memento_counts.values():
        occurrences[count] += 1

    return occurrences # Return the dictionary of memento occurrences.

def find_top_mementos (memento_counts, uri_hash_map, top_n=5):
    """
    Find the top URIs with the most mementos.

    Args:
        memento_counts (dict): Dictionary where keys are filenames (hashes) and values are memento counts.
        uri_hash_map (dict): Dictionary mapping hash filenames (without extensions) to their original URIs.
        top_n (int): Number of top URIs to display.

    Returns:
        list: A list of tuples, where each tuple contains the original URI and its corresponding memento count.
            Example: [('http://example.com', 0), ('http://another.com', 3), ...]
    """
    # Sort the memento counts in descending order, so the URIs with the most mementos come first.
    sorted_uris = sorted(memento_counts.items(), key=lambda x: x[1], reverse=True)
    
    top_uris = [] # List to store the top URIs and their memento counts.

    # Iterate over the top N sorted URIs.
    for hash_file, memento_count in sorted_uris[:top_n]:
        # Remove the '.json' extension from the filename to match the keys in uri_hash_map.
        hash_key = hash_file.replace('.json', '')

        # Check if the stripped filename (hash_key) exists in the URI hash map.
        if hash_key in uri_hash_map:
            # Append a tuple of (original URI, memento count) to the top_uris list
            top_uris.append((uri_hash_map[hash_key], memento_count))
        else:
            # If the hash_key is not found in the mapping, print a warning for debugging purposes.
            print(f"Warning: {hash_key} not found in URI hash mapping.")

    # Return the list of top URIs with their corresponding memento counts.
    return top_uris

# ===================== Domain Processing Functions ==================

def get_core_domain(uri):
    """
    Extract the core domain from a URI, stripping away paths and query parameters.

    Args:
        uri(str): The URI to extract the core domain from.

    Returns:
        str: The core domain of the URI.
    """
    parsed_uri = urlparse(uri) # Break down the URI into components.
    domain = parsed_uri.netloc # Extract the domain (netloc).
    return domain # Return only the core domain.

def count_core_domain_frequencies(uri_hash_map, memento_counts):
    """
    Count the frequencies of core domains based on memento counts.

    Args:
        uri_hash_map (dict): A dictionary mapping hash filenames to URIs.
        memento_counts (dict): A dictionary of memento counts per URI file.
    
    Returns:
        dict: A dictionary where the keys are core domains and value are their frequencies.
    """
    # Use defaultdict to initialize domain counts as 0 by default.
    domain_frequencies = defaultdict(int)

    # Loop through the URI hash map.
    for hash_file, memento_count in uri_hash_map.items():
        # Get the URI associated with the hash.
        uri = uri_hash_map.get(hash_file)

        if uri: # Ensure the URI is valid (i.e., not None).
            core_domain = get_core_domain(uri) # Extract the core domain from the URI.
            domain_frequencies[core_domain] += 1 # Increment the count for that core domain.

    return domain_frequencies # Return the final count of domains

def find_most_frequent_domains(memento_counts, uri_hash_map, top_n=5):
    """
    Find the most frequent core domains among the URIs with a given memento count.

    Args:
        memento_counts (dict): Dictionary where keys are filenames (hashes) and values are memento counts.
        uri_hash_map (dict): Dictionary mapping hash filenames (without extensions) to their original URIs.
        top_n (int): Number of top URIs to display.

    Returns:
        list: A list of tuples with the top core domains and their frequencies.
    """
    # Get the frequency count of all core domains.
    domain_frequencies = count_core_domain_frequencies(uri_hash_map, memento_counts)

    # Sort the domains by their frequency in descending order.
    sorted_domains = sorted(domain_frequencies.items(), key=lambda x: x[1], reverse=True)

    # Return only the top 'n' domains from the sorted list.
    return sorted_domains[:top_n]

# ====================== Table Display Functions =======================

def generate_summary_table(occurrences):
    """
    Generate and print a summary table of memento counts and the number of URIs with those counts.

    Args:
        occurrences (dict): A dictionary of memento count occurrences.
    """
    table = PrettyTable() # Initialize the table
    table.field_names = ["Mementos", "URI-Rs"]

    # Add rows to the table for each memento count and its occurrence count.
    for memento_count, uri_count in sorted(occurrences.items()):
        table.add_row([memento_count, uri_count])

    print(table)

def generate_top_mementos_table(top_mementos):
    """
    Generate and print a table of the top URIs with the most mementos.

    Args:
        top_mementos (list): A list of tuples containing URIs (filenames) and memento counts.
    """
    table = PrettyTable() # Initialize the table
    table.field_names = ["URI-Rs With The Most Mementos", "Memento Count"]

    # Add rows to the table for each URI and its memmento count.
    for uri, memento_count in top_mementos:
        table.add_row([uri, memento_count])

    print(table)

def generate_domain_memento_table(domain_mementos):
    """
    Generate and print a table of the top URIs with the most mementos.

    Args:
        top_mementos (list): A list of tuples containing URIs (filenames) and memento counts.
    """
    table = PrettyTable() # Initialize the table
    table.field_names = ["Domains With The Most Mementos", "Memento Count"]

    # Add rows to the table for each domain and its memento count.
    for domain, memento_count in domain_mementos:
        table.add_row([domain, memento_count])

    print(table)

# ========================= Main Process =========================

if __name__ == "__main__":
    timemaps_dir = "homework-3/timemaps"
    uri_hash_map = load_uri_mapping("homework-2/uri_mapping.txt")

    # Analyze the TimeMaps and count mementos.
    memento_counts = analyze_timemaps(timemaps_dir)

    # Count occurrences and find top URIs/domains.
    occurrences = count_memento_occurrences(memento_counts)
    top_mementos = find_top_mementos(memento_counts, uri_hash_map, top_n=5)
    most_frequent_domains = find_most_frequent_domains(memento_counts, uri_hash_map, top_n=5)

    # Generate and display tables.
    generate_summary_table(occurrences)
    generate_top_mementos_table(top_mementos)
    generate_domain_memento_table(most_frequent_domains)