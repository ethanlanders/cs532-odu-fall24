import os
import json
import matplotlib.pyplot as plt
from datetime import datetime


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
    Only keep those with more than 0 mementos.
    
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
        
        # Only include TimeMaps with more than 0 mementos.
        if memento_count > 0:
            memento_counts[filename] = memento_count

    return memento_counts # Return the filtered dictionary of memento counts.

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

def extract_earliest_datetime():
    pass

def calculate_memento_age():
    pass

if __name__ == "__main__":
    timemaps_dir = "homework-3/timemaps"
    memento_counts = analyze_timemaps(timemaps_dir)
    