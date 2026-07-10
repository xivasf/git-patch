import requests
import re
import os
import time

def get_repo_2url(url):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2)
def find_email(ptxt):
    match = re.search(r"^From:\s+(.+ <.+@.+>)", ptxt, re.MULTILINE)
    if match:
        return match.group(1)
    else:
        return None
def get_email(repo_url):
    try:
        owner, repo = get_repo_2url(repo_url)
        api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        commit_data = response.json()[0]
        new_commit = commit_data['sha']
        owner_user = commit_data['author']['login'].lower()
        if owner_user in [username.lower() for username in blacklist]:
            print("user is blacklisted.")
            time.sleep(2)
            return
        patch_url = f"https://github.com/{owner}/{repo}/commit/{new_commit}.patch"
        patch_response = requests.get(patch_url)
        patch_response.raise_for_status()
        ptxt = patch_response.text
        email_line = find_email(ptxt)

        
        if email_line:
            print(email_line)
            os.system("pause") 
        else: 
            print("email not found.") 
            os.system("pause")
    except Exception:
        print("cant fetch/invalid repo")
        os.system("pause")

if __name__ == "__main__":
    os.system("cls")
    repo_url = input("\033[31mWARNING: IT CAN ONLY BE FROM THEIR COMMITS!\033[0m \nenter repo url: ")
    get_email(repo_url)