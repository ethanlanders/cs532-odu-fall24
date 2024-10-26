import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

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
        dict: A dictionary where the keys are filenames and values are tuples (memento_count, earliest_datetime).
    """
    analysis_results = {} # Dictionary to store the counts for each file.

    # Loop over all files in the directory.
    for filename in os.listdir(timemaps_dir):
        # Load the TimeMap from each file.
        timemap = load_timemap(os.path.join(timemaps_dir, filename))
        # Count the mementos in the TimeMap.
        memento_count = count_mementos(timemap)
        
        # Only include TimeMaps with more than 0 mementos.
        if memento_count > 0:
            earliest_dt = extract_earliest_datetime(timemap) # Get the earliest datetime.
            analysis_results[filename] = (memento_count, earliest_dt)

    return analysis_results # Return the filtered dictionary of memento counts.

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

def extract_earliest_datetime(timemap):
    """
    Extract the earliest datetime from the mementos within the TimeMap.

    Args:
        timemap (dict or None): The TimeMap object. If None, return None.

    Returns:
        datetime or None: The datetime of the first memento or None if no valid mementos are present.
    """
    if timemap is None or 'mementos' not in timemap:
        return None  # Return None if no mementos section in the TimeMap.
    
    first_memento = timemap.get('mementos', {}).get('first', None)

    # Convert the datetime string to a datetime object if available.
    if first_memento is not None and 'datetime' in first_memento:
        return datetime.strptime(first_memento['datetime'], "%Y-%m-%dT%H:%M:%SZ")

    return None

def calculate_memento_age(earliest_datetime):
    """
    Calculate the age in days from the earliest memento datetime to the current date.
    
    Args:
        earliest_datetime (datetime or None): the datetime of the first memento.

    Returns:
        int or None: The age in days of the memento or None if no valid datetime is provided.
    """
    if earliest_datetime is None:
        return None  # Return None if no valid datetime.
    
    # Calculate the age by subtracting from the current date.
    current_datetime = datetime.now()
    age = current_datetime - earliest_datetime

    return age.days  # Return the age in days.

if __name__ == "__main__":
    # Define the directory containing TimeMap files.
    timemaps_dir = "homework-3/timemaps"
    
    # Analyze all TimeMaps and obtain memento count and earliest datetime for each.
    analysis_results = analyze_timemaps(timemaps_dir)

    # List to hold the calculated memento ages for plotting. 
    uri_memento_ages = []

    # Print the results and store ages for plotting.
    for filename, (count, earliest_dt) in analysis_results.items():
        # Calculate the age of the earliest memento.
        memento_age = calculate_memento_age(earliest_dt)    
        if memento_age is not None:
            uri_memento_ages.append(memento_age)  # Add age to list for plotting.
        
        # Print details for each TimeMap file.
        print(f"File: {filename}, Memento Count: {count}, Earliest Datetime: {earliest_dt}, Memento Age: {memento_age} days\n")

    # Plot the distribution of memento ages as a boxplot.
    plt.boxplot(uri_memento_ages, vert=False)  # Horizontal boxplot for readability.
    plt.xlabel('Age of Mementos (Days)')  # Label for x-axis.
    plt.yticks([])  # Remove y-axis ticks as there's only one data category.
    plt.title('Distribution of Memento Ages Across URIs')  # Title of the plot.
    plt.show()  # Display the plot.