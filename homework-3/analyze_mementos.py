import json
import os
from prettytable import PrettyTable
from collections import defaultdict

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
    for filename in os.listdir(timemap_dir):
        # Load the TimeMap from each file.
        timemap = load_timemap(os.path.join(timemap_dir, filename))
        # Count the mementos in the TimeMap.
        memento_count = count_mementos(timemap)
        # Store the result in the dictionary.
        memento_counts[filename] = memento_count

    return memento_counts # Return the dictionary of memento counts.

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

def generate_summary_table(occurrencess):
    """
    Generate and print a summary table of memento counts and the number of URIs with those counts.

    Args:
        occurrences (dict): A dictionary of memento count occurrences.
    """
    table = PrettyTable() # Initialize the table
    table.field_names = ["Mementos", "URI-Rs"]  # Set column headers.

    # Add rows to the table for each memento count and its occurrence count.
    for memento_count, uri_count in sorted(occurrencess.items()):
        table.add_row([memento_count, uri_count])

    print(table) # Print the table to the console.

# Main process: Set directory path and run analysis.
timemap_dir = "homework-3/timemaps"

# Analyze the TimeMaps and count mementos.
memento_counts = analyze_timemaps(timemap_dir)

# Count how many URIs have the same memento count.
occurrences = count_memento_occurrences(memento_counts)

# Generate and display the summary table.
generate_summary_table(occurrences)