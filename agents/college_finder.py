import os
import logging
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths and Configuration
BASE_DIR = os.getcwd()  # Use the current working directory
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'college_data.txt')
QUERY = "new colleges in Gujarat 2025"

def create_requests_session():
    """Create a robust requests session with retry."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]  # DuckDuckGo requires POST for search
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_results(query):
    """Fetch search results from DuckDuckGo."""
    SEARCH_URL = "https://html.duckduckgo.com/html"
    session = create_requests_session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }
    data = {'q': query}
    try:
        response = session.post(SEARCH_URL, data=data, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = [a.text for a in soup.find_all('a', {'class': 'result__a'})]
        logger.info(f"Fetched {len(results)} results.")
        return results[:5]  # Limit to top 5 results
    except requests.RequestException as e:
        logger.error(f"Error fetching results: {e}")
        return []

def save_results(data, filename):
    """Save the fetched results to a file."""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"{item}\n")
        logger.info(f"Results saved to {filename}")
    except IOError as e:
        logger.error(f"Error saving results: {e}")

def main():
    """Main function to fetch and save search results."""
    logger.info(f"Searching for: {QUERY}")
    results = fetch_results(QUERY)
    if results:
        save_results(results, OUTPUT_FILE)
    else:
        logger.warning("No results found.")

if __name__ == "__main__":
    main()
