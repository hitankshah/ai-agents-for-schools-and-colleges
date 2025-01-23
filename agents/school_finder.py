import os
import logging
import requests
from bs4 import BeautifulSoup
from git import Repo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use absolute paths for file and repo handling
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
REPO_PATH = os.path.join(BASE_DIR, '..')  # Adjust to your repo's location
OUTPUT_FILE = os.path.join(BASE_DIR, '..', 'data', 'school_data.txt')
QUERY = "new schools in Gujarat 2025"
SEARCH_URL = "https://www.google.com/search?q="

def fetch_results(query):
    """Fetch search results from Google."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        # Replace spaces with "+" for the query string
        url = SEARCH_URL + query.replace(" ", "+")
        logger.info(f"Fetching results from: {url}")
        
        # Make the HTTP GET request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML response
        soup = BeautifulSoup(response.text, "html.parser")
        results = [g.text for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')]
        
        logger.info(f"Fetched {len(results)} results.")
        return results
    
    except requests.RequestException as e:
        logger.error(f"Error fetching results: {e}")
        return []

def save_results(data, filename):
    """Save fetched results to a file."""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as f:
            for item in data:
                f.write(item + "\n")
        logger.info(f"Results saved to {filename}")
    except IOError as e:
        logger.error(f"Error saving results: {e}")

def commit_to_git(filename):
    """Commit and push changes to the Git repository."""
    try:
        # Open the repository
        repo = Repo(REPO_PATH)
        
        # Add the file to the git index
        repo.git.add(filename)
        
        # Commit changes with a message
        repo.index.commit("Updated school data")
        
        # Push changes to the remote repository
        repo.remote(name='origin').push()
        logger.info("Changes committed and pushed to GitHub")
    except Exception as e:
        logger.error(f"Git commit error: {e}")

def main():
    """Main function to fetch, save, and commit results."""
    logger.info(f"Starting search for: {QUERY}")
    
    # Fetch results
    results = fetch_results(QUERY)
    
    if results:
        # Save results to the file
        save_results(results, OUTPUT_FILE)
        
        # Commit and push results to the Git repository
        commit_to_git(OUTPUT_FILE)
    else:
        logger.warning("No results found")

if __name__ == "__main__":
    main()
