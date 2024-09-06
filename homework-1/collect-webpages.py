from bs4 import BeautifulSoup # Import BeautifulSoup for HTML parsing
import requests # Import requests for making HTTP requests
import re
import sys

def main(seed_uri):
    # Initialize a set to store unique URIs
    # https://www.geeksforgeeks.org/python-data-types/
    unique_uris = set()
    
    # Collect URIs from the seed webpage
    collect_uris(seed_uri, unique_uris)

    while len(unique_uris) < 500:
        new_seed = pick_random_uri(unique_uris)
        collect_uris(new_seed, unique_uris)

    # Save the collected URIs to an output file
    save_uris_to_file(unique_uris, "output/uris.txt")
    pass

def collect_uris(seed_uri, unique_uris):
    # Extract links from the webpage content
    links = extract_links_from_page(seed_uri)
    
    for link in links:
        # Check if the link is an HTML page and contains more than 1000 bytes
        if is_valid_html_page(link):
            # Add valid link to set of unique URIs
            unique_uris.add(link)

def extract_links_from_page(uri):
    # https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/
    # Request the webpage and parse HTML to extract links
    response = requests.get(uri, timeout=5) # 5 second timeout
    
    # Parse the HTMl content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    links = set()

    # https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/?ref=header_outind
    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        href = link.get('href')
        if href:
            links.add(link)
    # links = [a['href'] for a in soup.find_all('a', href=True)]

    # Return the list of links
    return links

def is_valid_html_page(uri):
    pass

def pick_random_uri(uri_set):
    # Return a random URI from the URI set
    pass

def save_uris_to_file():
    # Save the list of URIs to a text file
    pass

if __name__ == "___main__":
    # Ensure the user provided a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 collect-webpages.py <seed_uri>")
        sys.exit(1)

# Start the main process
# main(sys.argv[1])
extract_links_from_page(sys.argv[1])