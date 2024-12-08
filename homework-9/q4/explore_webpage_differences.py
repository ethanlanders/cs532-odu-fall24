import difflib
import json
import os

# Load the status codes from the JSON file that stores URI status information
with open('homework-9/q2/status_codes.json', 'r') as f:
    status_codes = json.load(f)

# Create a list of URIs that returned a '200 OK' response based on status_codes
successful_uris = [filename for filename, code in status_codes.items() if code == 200]

# Directories where the processed HTML files from HW2 and the current assignment are stored
processed_dir_hw2 = "homework-2/processed_html"
processed_dir_now = "homework-9/q2/processed_html"
differences = {}  # Dictionary to store the size differences between the files

# Iterate through each URI that returned a '200 OK' and compare the content of the processed files
for filename in successful_uris:
    file_hw2_path = os.path.join(processed_dir_hw2, filename)
    file_now_path = os.path.join(processed_dir_now, filename)

    if os.path.exists(file_hw2_path) and os.path.exists(file_now_path):
        with open(file_hw2_path, 'r', encoding='utf-8') as f1, open(file_now_path, 'r', encoding='utf-8') as f2:
            content_hw2 = f1.read()
            content_now = f2.read()
            
            # Calculate the absolute difference in size (in bytes)
            size_difference = abs(len(content_now) - len(content_hw2))
            differences[filename] = size_difference

# Sort the dictionary by size difference in descending order
sorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

# Get the top 3 URIs with the most significant changes
top_3_changes = sorted_differences[:3]
print("Top 3 URIs with the most significant changes:")
for filename, diff in top_3_changes:
    # Print the URI and the size differences in bytes
    print(f"{filename}: {diff} bytes")

# Print detailed line-by-line differences for the top 3 URIs
for filename, _ in top_3_changes:
    file_hw2_path = os.path.join(processed_dir_hw2, filename)
    file_now_path = os.path.join(processed_dir_now, filename)

    with open(file_hw2_path, 'r', encoding='utf-8') as f1, open(file_now_path, 'r', encoding='utf-8') as f2:
        content_hw2 = f1.readlines()
        content_now = f2.readlines()

        # Use unified_diff to get a detailed line-by-line comparison between the two files
        diff = difflib.unified_diff(content_hw2, content_now, lineterm='')
        print(f"\nDifferences for {filename}:")
        print(''.join(diff))  # Print the differences as a single string