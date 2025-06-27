import requests
from .util import getHeaders

def getRepoInfo(url: str, token: str)-> dict:

    headers = getHeaders(token)

    req = requests.get(url, headers=headers)
    data = req.json()

    if data.get("message") != None:
        return {
            "message": data.get("message"),
        }

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

def getLanguagesInfo(url: str, token: str)-> dict:
    headers = getHeaders(token)

    req = requests.get(url+"/languages", headers=headers)
    data = req.json()

    if data.get("message") != None:
        return {
            "message": data.get("message"),
        }
    
    total = sum(data.values())
    if total == 0:
        return {"languages": {}}

    percentages = {
        lang: round((bytes_ / total) * 100, 2)
        for lang, bytes_ in sorted(data.items(), key=lambda x: x[1], reverse=True)
    }

    return {
        "languages": percentages,
    }

def getReleasesInfo(url: str, token: str)-> dict:
    headers = getHeaders(token)

    req = requests.get(url+"/releases/latest", headers=headers)
    data = req.json()

    if data.get("message") == "Not Found":
        return {
            "latest_release": None,
        }
    
    return {
        "latest_release": {
            "tag": data.get("tag_name"),
            "name": data.get("name"),
            "published_at": data.get("published_at"),
            "body": data.get("body", "").split("\n")[0],
            "url": data.get("html_url"),
        }
    }
    
def getOpenPRCount(url: str, token: str)-> dict:
    headers = getHeaders(token)

    parts = url.rstrip("/").split("/")

    req = requests.get(f"https://api.github.com/search/issues?q=repo:{parts[-2]}/{parts[-1]}+type:pr+state:open", headers=headers)
    data = req.json()

    return {"open_pull_requests": data.get("total_count", 0)}

def getBranchesInfo(url: str, token: str)-> dict:
    headers = getHeaders(token)

    req = requests.get(url+"/branches", headers=headers)
    data = req.json()

    return {
        "branches": "|".join([b["name"] for b in data])
    }

def getRateLimit(token: str)-> dict:
    headers = getHeaders(token)

    req = requests.get("https://api.github.com/rate_limit", headers=headers)
    data = req.json()

    if data.get("message") != None:
        return {
            "message": data.get("message"),
        }
    
    return {
        "limit": data.get("resources").get("core", {}).get("limit"),
        "used": data.get("resources").get("core", {}).get("used"),
        "remaining": data.get("resources").get("core", {}).get("remaining"),
    }

def getUserInfo(url: str):
    pass