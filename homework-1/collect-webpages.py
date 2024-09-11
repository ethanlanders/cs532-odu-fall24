"""
Webpage URI Collector Script

This script collects URIs from web pages starting from a given seed URI,
then saving them to a file.

References:
- Python Virtual Environments: https://python.land/virtual-environments/virtualenv
- Python Data Types: # https://www.geeksforgeeks.org/python-data-types/
- Implementing Web Scraping with BeautifulSoup: https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
- BeautifulSoup Scraping Link from HTML: https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/?ref=header_outind
- Exception Handling in Python Requests Module: # https://www.geeksforgeeks.org/exception-handling-of-python-requests-module/
- Python Random Choice Method: # https://www.w3schools.com/python/ref_random_choice.asp
- Writing to File in Python: # https://www.geeksforgeeks.org/writing-to-file-in-python/

To activate the virtual environment to access BeautifulSoup funcionality,
run `source venv/bin/activate`
"""

from bs4 import BeautifulSoup # Import BeautifulSoup for HTML parsing
import requests # Import requests for making HTTP requests
import random
import sys
import re

def main(seed_uri):
    """
    Main function to start the process of collectiong URIs.

    Args:
    - seed_uri (str): The starting URI to begin the collection process.
    
    References:
    - Python Data Types: # https://www.geeksforgeeks.org/python-data-types/
    """
    print(f"\nStarting with seed URI: {seed_uri}")

    # Initialize a set to store unique URIs
    unique_uris = set()
    max_attempts = 1000  # Set a maximum number of attempts to avoid infinite loops
    attempt = 0

    # Collect URIs from the seed webpage
    collect_uris(seed_uri, unique_uris)
    print(f"Initial URIs collected: {len(unique_uris)}")

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
    """
    Collect URIs from a given seed URI and add them to the set of unique URIs.

    Args:
    - seed_uri (str): The URI from which to extract links.
    - unique_uris (set): Set to store unique URIs.
    """
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
    """
    Extract all links from a given webpage.

    Args:
    - uri (str): The URI of the webpage to fetch.

    Returns:
    - set: A set of links found on the webpage.

    References:
    - Implementing Web Scraping with BeautifulSoup: https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
    - BeautifulSoup Scraping Link from HTML: https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/?ref=header_outind
    """ 
    print(f"Fetching page: {uri}")
    try:
        response = requests.get(uri, timeout=5, verify=False) # 5 second timeout
        
        # Parse the HTMl content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        
        for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            href = link.get('href')
            if href:
                links.add(href)

        print(f"Found {len(links)} links on page")
        return links
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {uri}: {e}")
        return set() # Return an empty set if there is an error

def is_valid_html_page(uri):
    """
    Check if a given URI points to a valid HTML page.

    Args:
    - uri (str): The URI to validate.

    Returns:
    - bool: True if the URI is a valid HTML page; False otherwise.

    References:
    - Exception Handling in Python Requests Module: # https://www.geeksforgeeks.org/exception-handling-of-python-requests-module/
    """
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
    """
    Pick a random URI from the given set of URIs.

    Args:
    - uri_set: A randomly chosen URI from the set.

    Returns:
    - str: A randomly chosen URI from the set.
    
    References:
    - Python Random Choice Method: # https://www.w3schools.com/python/ref_random_choice.asp
    """
    if not uri_set:
        print("No URIs available to pick from.")
    else:
        print(f"Picking a random URI from {len(uri_set)} available URIs")
        return random.choice(list(uri_set))

def save_uris_to_file(uris, filename):
    """
    Save the collected URIs to a text file.

    Args:
    - uris (set): Set of URIs to save.
    - filename (str): The name of the file to save the URIs.
    
    References:
    - Writing to File in Python: # https://www.geeksforgeeks.org/writing-to-file-in-python/
    """
    print(f"Saving {len(uris)} URIs to file: {filename}")
    with open(filename, 'w') as f:
        for uri in uris:
            f.write(uri + '\n')

if __name__ == "__main__":
    # Ensure the user provided a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 collect-webpages.py <seed_uri>")
        sys.exit(1)

# Start the main process with the provided seed URI
main(sys.argv[1])