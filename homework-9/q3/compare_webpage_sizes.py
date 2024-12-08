import seaborn as sns
import matplotlib.pyplot as plt
import os

# Directories containing raw HTML and processed HTML files from HW2 and current work
raw_html_dir_hw2 = "homework-2/raw_html"
raw_html_dir_now = "homework-9/q2/raw_html"
processed_dir_hw2 = "homework-2/processed_html"
processed_dir_now = "homework-9/q2/processed_html"

def get_file_sizes(directory):
    """
    Computes the sizes in bytes of all files in a given directory.

    Args:
        directory (str): Path to the directory containing files.

    Returns:
        dict: A dictionary mapping file paths to their sizes in bytes.
    """
    sizes = {}
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            sizes[file_name] = os.path.getsize(file_path)
    return sizes

# Get file sizes for raw HTML and processed HTML from HW2 and the current work
raw_html_sizes_hw2 = get_file_sizes(raw_html_dir_hw2)
raw_html_sizes_now = get_file_sizes(raw_html_dir_now)
processed_sizes_hw2 = get_file_sizes(processed_dir_hw2)
processed_sizes_now = get_file_sizes(processed_dir_now)

# Dictionaries to store size differences
raw_html_differences = {}
processed_differences = {}

# Calculate differences in raw HTML sizes
for file_name in raw_html_sizes_now:
    if file_name in raw_html_sizes_hw2:  # Ensure the file exists in both datasets
        raw_html_differences[file_name] = raw_html_sizes_now[file_name] - raw_html_sizes_hw2[file_name]

# Calculate differences in processed HTML sizes
for file_name in processed_sizes_now:
    if file_name in processed_sizes_hw2:  # Ensure the file exists in both datasets
        processed_differences[file_name] = processed_sizes_now[file_name] - processed_sizes_hw2[file_name]

# Extract the size differences into lists for plotting
raw_html_values = list(raw_html_differences.values())
processed_values = list(processed_differences.values())

# Plotting the results
plt.figure(figsize=(10, 5))  # Set the figure size

# First boxplot: Differences in raw HTML sizes
plt.subplot(1, 2, 1)
sns.boxplot(data=raw_html_values)
plt.title("Raw HTML Size Differences")
plt.ylabel("Size Difference (bytes)")

# Second boxplot: Differences in processed HTML sizes
plt.subplot(1, 2, 2)
sns.boxplot(data=processed_values)
plt.title("Processed Text Size Differences")
plt.ylabel("Size Difference (bytes)")

# Adjust the layout to prevent overlap
plt.tight_layout()

# Display the plots
plt.show()