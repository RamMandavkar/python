# https://github.com/dashboard
# ram.mandavkar@gmail.com/Ckmvrushali@1
# https://github.com/settings/personal-access-tokens/11019343
# pip install requests
import requests
import json

GITHUB_TOKEN = "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"
USERNAME = "RamMandavkar"

url = f"https://api.github.com/users/{USERNAME}/repos"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

response = requests.get(url, headers=headers)
# print("response.json :: " , json.dumps(response.json(), indent=4))

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(repo["full_name"])
else:
    print("Error:", response.status_code, response.text)