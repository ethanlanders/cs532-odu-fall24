# To activate virtual environment to access BeautifulSoup funcionality,
# run `source venv/bin/activate`

from bs4 import BeautifulSoup # Import BeautifulSoup for HTML parsing
import requests # Import requests for making HTTP requests
import random
import sys
import re

def main(seed_uri):
    print(f"\nStarting with seed URI: {seed_uri}")

    # Initialize a set to store unique URIs
    # https://www.geeksforgeeks.org/python-data-types/
    unique_uris = set()
    max_attempts = 1000  # Set a maximum number of attempts to avoid infinite loops
    attempt = 0

    # Collect URIs from the seed webpage
    collect_uris(seed_uri, unique_uris)
    print(f"Initial URIs collected: {len(unique_uris)}")
    # IT MAKES IT HERE

    while len(unique_uris) < 500 and attempt < max_attempts:
        attempt += 1
        print(f"Attempt {attempt}: Current URIs collected: {len(unique_uris)}")
        new_seed = pick_random_uri(unique_uris)
        print(f"Picked new seed URI: {new_seed}")
        collect_uris(new_seed, unique_uris)
        print(f"Total URIs collected: {len(unique_uris)}")
        
    # Save the collected URIs to an output file
    save_uris_to_file(unique_uris, "output/uris.txt")
    print(f"URIs saved to output/uris.txt")
    print(f"Final number of URIs collected: {len(unique_uris)}")

def collect_uris(seed_uri, unique_uris):
    # Extract links from the webpage content
    print(f"Collecting URIs from: {seed_uri}")
    links = extract_links_from_page(seed_uri)
    print(f"Extracted {len(links)} links")
    
    for link in links:
        # Check if the link is an HTML page and contains more than 1000 bytes
        if is_valid_html_page(link):
            # Add valid link to set of unique URIs
            print(f"Adding valid link: {link}")
            unique_uris.add(link)
        else:
            print(f"Invalid link or not HTML: {link}")

def extract_links_from_page(uri):
    # https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
    # Request the webpage and parse HTML to extract links
    print(f"Fetching page: {uri}")
    try:
        response = requests.get(uri, timeout=5, verify=False) # 5 second timeout
        
        # Parse the HTMl content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()

        # https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/?ref=header_outind
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            href = link.get('href')
            if href:
                links.add(href)
        # links = [a['href'] for a in soup.find_all('a', href=True)]

        # Return the list of links
        print(f"Found {len(links)} links on page")
        return links
    
    # https://www.geeksforgeeks.org/exception-handling-of-python-requests-module/
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {uri}: {e}")
        return [] # Return an empty list if there is an error

def is_valid_html_page(uri):
    print(f"Validating URI: {uri}")
    try:
        response = requests.head(uri, timeout=5, verify=False) # Only fetch headers
        content_type = response.headers.get('Content-Type', '')
        content_length = response.headers.get('Content-Length', 0)

        if 'text/html' in content_type and int(content_length) > 1000:
            print(f"Valid HTML page: {uri}")
            return True
        else:
            print(f"Invalid HTML page or too small: {uri}")
            return False
    
    except requests.exceptions.Timeout as e:
        print(f"Timeout error validating {uri}: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error validating {uri}: {e}")
        return False

def pick_random_uri(uri_set):
    # https://www.w3schools.com/python/ref_random_choice.asp
    # Return a random URI from the URI set
    if not uri_set:
        print("No URIs available to pick from.")
    else:
        print(f"Picking a random URI from {len(uri_set)} available URIs")
    return random.choice(list(uri_set))

def save_uris_to_file(uris, filename):
    # https://www.geeksforgeeks.org/writing-to-file-in-python/
    # Save the list of URIs to a text file
    print(f"Saving {len(uris)} URIs to file: {filename}")
    with open(filename, 'w') as f:
        for uri in uris:
            f.write(uri + '\n')

if __name__ == "__main__":
    # Ensure the user provided a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 collect-webpages.py <seed_uri>")
        sys.exit(1)

# Start the main process
main(sys.argv[1])