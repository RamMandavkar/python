# https://github.com/dashboard
# ram.mandavkar@gmail.com/Ckmvrushali@1
# https://github.com/settings/personal-access-tokens/11019343
# pip install requests

from google import genai
from google.genai import types
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()  # loads .env into environment

GITHUB_TOKEN = os.getenv("github_token")
USERNAME = os.getenv("github_username")

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