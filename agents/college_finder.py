import os
import requests
from bs4 import BeautifulSoup
from git import Repo

# Constants
REPO_PATH = "../"  # Adjust if needed
OUTPUT_FILE = "../data/college_data.txt"
QUERY = "new colleges in Gujarat 2025"
SEARCH_URL = "https://www.google.com/search?q="

# Scraper function
def fetch_results(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(SEARCH_URL + query.replace(" ", "+"), headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        results.append(g.text)

    return results

# Save results to file
def save_results(data, filename):
    with open(filename, "w") as f:
        for item in data:
            f.write(item + "\n")

# Commit changes to GitHub
def commit_to_git(filename):
    repo = Repo(REPO_PATH)
    repo.git.add(filename)
    repo.index.commit("Updated college data")
    repo.remote(name='origin').push()

# Main execution
def main():
    results = fetch_results(QUERY)
    save_results(results, OUTPUT_FILE)
    commit_to_git(OUTPUT_FILE)

if __name__ == "__main__":
    main()
