import seaborn as sns
import matplotlib.pyplot as plt

# Import the analyze_timemaps function from analyze_mementos.py
from analyze_mementos import analyze_timemaps

# Define the directories for the old and new timemaps
old_timemaps_dir = "homework-3/timemaps"
new_timemaps_dir = "homework-9/q1/timemaps"

# Initialize lists to hold memento counts for old and new timemaps
old_memento_count = []
new_memento_count = []

# Analyze the old and new timemaps and store the results as dictionaries
old_memento_count = analyze_timemaps(old_timemaps_dir)
new_memento_count = analyze_timemaps(new_timemaps_dir)

# Initialize a list to store the differences in memento counts between the new and old timemaps
differences = []

# Iterate through each URI in the old memento count dictionary
for uri in old_memento_count:
    # Get the old and new counts for the current URI, defaulting to 0 if not present
    old_count = old_memento_count.get(uri, 0)
    new_count = new_memento_count.get(uri, 0)

    # Print out the current URI and its old and new counts for debugging
    # print(f"URI: {uri} | Old Count: {old_count} | New Count: {new_count}")

    # Calculate the difference between the new and old counts and add it to the list 
    differences.append(new_count - old_count)

# Print the minimum and maximum values of the differences to check for data range
print(f"Min difference: {min(differences)}")
print(f"Max difference: {max(differences)}")

# Create a boxplot of differences to visualize the distribution of growth in mementos
sns.boxplot(differences)

# Set the label for the y-axis of the boxplot
plt.ylabel("Growth in Mementos Since Completing HW3")

# Save the boxplot as an image file
plt.savefig("homework-9/q1/memento_growth_boxplot.png", format="png", dpi=300, bbox_inches="tight")

# Display the boxplot
plt.show()