import matplotlib.pyplot as plt
from collections import Counter
from warcio.archiveiterator import ArchiveIterator

# Define a dictionary to hold file type counts.
file_type_counts = Counter()

warc_file_path = 'homework-4/hw4-cs532-20241026185953.warc'

# Process the WARC file and count file types.
with open(warc_file_path, 'rb') as stream:
    for record in ArchiveIterator(stream):
        if record.rec_type == 'response':
            file_type = record.http_headers.get_header('Content-Type')
            if file_type:
                file_type_counts[file_type.split(';')[0]] += 1

# Check if there's any data collected.
if not file_type_counts:
    print("No file types found. Check the WARC file.")
else:
    # Plotting
    file_types = list(file_type_counts.keys())            
    counts = list(file_type_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(file_types, counts, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("File Type")
    plt.ylabel("Number of URLs")
    plt.title("Number of URLs by File Type in WARC File")
    plt.tight_layout()
    plt.show()