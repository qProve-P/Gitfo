import requests
from typing import Dict

headers = {
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": "token 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"
}

def getRepoInfo(url: str)-> Dict[str, str]:

    req = requests.get(url, headers=headers)
    data = req.json()

    return {
        "name": data.get("name"),
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "html_url": data.get("html_url"),
        "visibility": data.get("visibility", "public"),
        "license": data.get("license", {}).get("name") if data.get("license") else None,
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "watchers": data.get("subscribers_count"),
        "open_issues": data.get("open_issues_count"),
        "default_branch": data.get("default_branch"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "topics": data.get("topics", []),
        "owner": {
            "login": data["owner"]["login"],
            "type": data["owner"]["type"]
        }
    }

def getUserInfo(url: str):
    pass