
import requests

def scrape_github_readme(repo_url: str) -> str:
    if not repo_url.endswith("/"):
        repo_url += "/"
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "main/README.md"
    response = requests.get(raw_url)
    return response.text if response.status_code == 200 else "README not found."
