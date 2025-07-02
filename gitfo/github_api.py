import requests, typer
from .util import getHeaders

def getRepoInfo(target: str, token: str)-> dict:

    headers = getHeaders(token)

    try:
        req = requests.get(f"https://api.github.com/repos/{target}", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()

    data = req.json()

    msg = data.get("message")
    if msg != None:
        if "Not Found" in msg:
            return {
                "full_name": target,
                "error": msg
            }
        else:
            return {
                "message": msg,
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

def getLanguagesInfo(target: str, token: str)-> dict:
    headers = getHeaders(token)

    try:
        req = requests.get(f"https://api.github.com/repos/{target}/languages", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()
    
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

def getReleasesInfo(target: str, token: str)-> dict:
    headers = getHeaders(token)

    try:
        req = requests.get(f"https://api.github.com/repos/{target}/releases/latest", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()
    
    data = req.json()

    if data.get("message") == "Not Found":
        return {
            "latest_release": None,
        }
    
    return {
        "latest_release": {
            "tag_name": data.get("tag_name"),
            "name": data.get("name"),
            "published_at": data.get("published_at"),
            "body": data.get("body", "").split("\n")[0],
            "html_url": data.get("html_url"),
        }
    }
    
def getOpenPRCount(target: str, token: str)-> dict:
    headers = getHeaders(token)

    parts = target.split("/")

    try:
        req = requests.get(f"https://api.github.com/search/issues?q=repo:{parts[0]}/{parts[1]}+type:pr+state:open", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()

    data = req.json()

    return {"open_pull_requests": data.get("total_count", 0)}

def getBranchesInfo(target: str, token: str)-> dict:
    headers = getHeaders(token)

    try:
        req = requests.get(f"https://api.github.com/repos/{target}/branches", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()

    data = req.json()

    return {
        "branches": "|".join([b["name"] for b in data])
    }

def getRateLimit(token: str)-> dict:
    headers = getHeaders(token)

    try:
        req = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()

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

def getUserInfo(target: str, token: str)-> dict:
    headers = getHeaders(token)

    try:
        req = requests.get(f"https://api.github.com/users/{target}", headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        typer.secho("Api not responding. Try again later.", fg=typer.colors.RED)
        raise typer.Exit()

    data = req.json()

    msg = data.get("message")
    if msg != None:
        if "Not Found" in msg:
            return {
                "login": target,
                "error": msg
            }
        else:
            return {
                "message": msg,
            }
    
    return {
        "login": data.get("login"),
        "id": data.get("id"),
        "type": data.get("type"),
        "name": data.get("name"),
        "company": data.get("company"),
        "blog": data.get("blog"),
        "location": data.get("location"),
        "email": data.get("email"),
        "bio": data.get("bio"),
        "twitter_username": data.get("twitter_username", None),
        "public_repos": data.get("public_repos"),
        "public_gists": data.get("public_gists"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }