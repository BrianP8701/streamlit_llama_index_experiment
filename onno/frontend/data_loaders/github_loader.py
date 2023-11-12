import requests
import base64
from typing import List

class RepoScraper():
    def __init__(self, github_key):
        self.token = github_key

    def scrape(self, repo_url, ignore_folders=["venv"], ignore_files=[]):
        """
        Fetches the content of all files in a given GitHub repository.

        This function uses the GitHub API to recursively fetch the content of all files in a given repository.
        It returns a dictionary where keys are file paths and values are the content of those files. By default,
        this function will ignore any 'venv' directories. However, specific folders and files can be excluded
        from the results by passing them in `ignore_folders` and `ignore_files` respectively.

        Parameters:
        - repo_url (str): The URL of the GitHub repository. Should be in the format 'https://github.com/{owner}/{repository_name}'.
        - token (str): The GitHub personal access token used for authentication.
        - ignore_folders (list, optional): A list of folder names to ignore. Defaults to ["venv"].
        - ignore_files (list, optional): A list of file names to ignore. Defaults to an empty list.

        Returns:
        - dict: A dictionary where keys are file paths (relative to the root of the repo) and values are the content of those files.

        Raises:
        - HTTPError: If there's an issue with the API request.

        Example usage:
        TOKEN = 'YOUR_PERSONAL_ACCESS_TOKEN'
        REPO_URL = 'https://github.com/BrianP8701/STREAM_GPT'
        content_dict = fetch_github_repo_content(REPO_URL, TOKEN)
        for path, content in content_dict.items():
            print(f"File path: {path}\nContent:\n{content}\n{'-'*40}\n")
        """
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Extract owner and repo from URL
        owner, repo = repo_url.rstrip('/').split('/')[-2:]
        
        # Recursive function to fetch content
        def fetch_path_content(path):
            response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/contents/{path}', headers=headers)
            response.raise_for_status()  # Raises exception for HTTP errors
            contents = response.json()
            
            all_contents = {}
            if isinstance(contents, list):  # Directory contents
                for item in contents:
                    if item['type'] == 'dir' and item['name'] not in ignore_folders:
                        all_contents.update(fetch_path_content(item['path']))
                    elif item['type'] == 'file' and item['name'] not in ignore_files:
                        file_response = requests.get(item['download_url'], headers=headers)
                        file_response.raise_for_status()
                        all_contents[item['path']] = file_response.text
            return all_contents

        return fetch_path_content("")
