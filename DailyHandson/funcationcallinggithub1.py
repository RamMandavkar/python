
# pip install PyGithub
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into environment

GITHUB_TOKEN = os.getenv("github_token")

g = Github(GITHUB_TOKEN)

user = g.get_user()
print("Logged in as:", user.login)

for repo in user.get_repos():
    print(repo.name)