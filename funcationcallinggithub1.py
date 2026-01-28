
# pip install PyGithub
from github import Github

g = Github("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")

user = g.get_user()
print("Logged in as:", user.login)

for repo in user.get_repos():
    print(repo.name)