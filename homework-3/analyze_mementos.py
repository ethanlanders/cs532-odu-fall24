import json
import os
from prettytable import PrettyTable
from collections import defaultdict

def load_timemap(filepath):
    try:    
        with open(filepath, 'r') as file:
            if os.stat(filepath).st_size == 0:
                return None
            return json.load(file)
    except json.JSONDecodeError:
        return None

def count_mementos(timemap):
    if timemap is None:
        return 0
    return len(timemap.get('mementos', []))

def analyze_timemaps(timemaps_dir):
    memento_counts = {}

    for filename in os.listdir(timemap_dir):
        timemap = load_timemap(os.path.join(timemap_dir, filename))
        memento_count = count_mementos(timemap)
        memento_counts[filename] = memento_count

    return memento_counts

def count_memento_occurrences(memento_counts):
    occurrences = defaultdict(int)

    for count in memento_counts.values():
        occurrences[count] += 1

    return occurrences

def generate_summary_table(occurrencess):
    table = PrettyTable()
    table.field_names = ["Mementos", "URI-Rs"]

    for memento_count, uri_count in sorted(occurrencess.items()):
        table.add_row([memento_count, uri_count])

    print(table)

timemap_dir = "homework-3/timemaps"

memento_counts = analyze_timemaps(timemap_dir)
occurrences = count_memento_occurrences(memento_counts)

generate_summary_table(occurrences)