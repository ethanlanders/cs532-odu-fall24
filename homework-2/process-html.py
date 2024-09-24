"""
References:
- https://pypi.org/project/boilerpy3/
"""
from boilerpy3 import extractors
import os
import shutil

if os.path.exists('processed_html'):
    print("processed_html directory exists. Deleting all files within it.\n")
    shutil.rmtree('processed_html')

os.makedirs('processed_html', exist_ok=True)

extractor = extractors.ArticleExtractor()
count = 0

for filename in os.listdir('homework-2/raw_html'):
    with open(f"homework-2/raw_html/{filename}", 'r', encoding='utf-8') as file:
        html_content = file.read()

    try:
        main_content = extractor.get_content(html_content)

        if main_content.strip():
            with open(f"homework-2/processed_html/{filename}", 'w', encoding='utf-8') as file:
                file.write(main_content)
            count = count + 1
        else:
            print(f"No useful content found in {filename}. Skipping.\n")

    except Exception as e:
        print(f"Error processing {filename}: {e}\n")

print(f"Only {count} HTML files contain meaningful content.\n")

