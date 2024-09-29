"""
References:
- BoilerPy3: https://pypi.org/project/boilerpy3/
"""

from boilerpy3 import extractors
import os
import shutil

# Check if the 'processed_html' directory exists, and if so, delete it and its contents
if os.path.exists('processed_html'):
    print("processed_html directory exists. Deleting all files within it.\n")
    shutil.rmtree('processed_html')

os.makedirs('processed_html', exist_ok=True)

# Initialize the ArticleExtractor from the boilerpy3 library, which will be used to extract
# the main content from HTML files.
extractor = extractors.ArticleExtractor()

# Initialize a counter to track how many files contain meaningful content.
count = 0

# Iterate through all files in the 'homework2/raw_html' directory
for filename in os.listdir('homework-2/raw_html'):
    with open(f"homework-2/raw_html/{filename}", 'r', encoding='utf-8') as file:
        html_content = file.read() # Read the full HTML content of the file

    try:
        # Extract the main content from the HTML using the ArticleExtractor
        main_content = extractor.get_content(html_content)

        # If the extracted content is not empty (contains meaningful text), 
        # write it to the 'processed_html' directory
        if main_content.strip():
            with open(f"homework-2/processed_html/{filename}", 'w', encoding='utf-8') as file:
                file.write(main_content) # Write the extracted content to a new file in 'processed_html'
            count = count + 1 # Increment the counter for files containing meaningful content.
        else:
            # If the extracted content is empty, print a message indicating that the file was skipped.
            print(f"No useful content found in {filename}. Skipping.\n")

    # Catch and print any errors that occur during processing (e.g., issues with extraction or reading files)
    except Exception as e:
        print(f"Error processing {filename}: {e}\n")

# After processing all files, print the total number of files that contained meaningful content.
print(f"Only {count} HTML files contain meaningful content.\n")