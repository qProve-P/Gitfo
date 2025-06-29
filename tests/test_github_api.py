#######################################
#       Tests for github_api.py       #
#######################################

import pytest
from unittest.mock import patch, MagicMock
from gitfo.github_api import getRepoInfo, getLanguagesInfo, getReleasesInfo, getOpenPRCount, getRateLimit, getUserInfo

@patch("gitfo.github_api.requests.get")
def testGetRepoInfo(mockGet):
    mockResponse = {
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "description": "My first repository on GitHub!",
        "html_url": "https://github.com/octocat/Hello-World",
        "visibility": "public",
        "license": None,
        "stargazers_count": 3004,
        "forks_count": 3158,
        "subscribers_count": 1732,
        "open_issues_count": 1764,
        "default_branch": "master",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2025-06-29T14:19:20Z",
        "topics": [],
        "owner": {
            "login": "octocat",
            "type": "User"
        }
    }

    mockGet.return_value = MagicMock(status_code=200, json=lambda: mockResponse)
    result = getRepoInfo("octocat/Hello-World", "TestToken")

    assert result["name"] == "Hello-World"
    assert result["license"] == None
    assert result["stars"] == 3004
    assert result["owner"]["login"] == "octocat"

@patch("gitfo.github_api.requests.get")
def testGetRepoInfoNotFound(mockGet):
    mockResponse = {"message": "Not Found"}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getRepoInfo("nonexistent/repo", "TestToken")

    assert result == {"message": "Not Found"}

@patch("gitfo.github_api.requests.get")
def testGetRepoInfoBadCredentials(mockGet):
    mockResponse = {"message": "Bad credentials"}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getRepoInfo("octocat/Hello-World", "BadToken")

    assert result == {"message": "Bad credentials"}

@patch("gitfo.github_api.requests.get")
def testGetRepoInfoRateLimitExceeded(mockGet):
    mockResponse = {"message": "API rate limit exceeded for user."}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getRepoInfo("octocat/Hello-World", "TestToken")

    assert result == {"message": "API rate limit exceeded for user."}

@patch("gitfo.github_api.requests.get")
def testGetLanguageInfo(mockGet):
    mockResponse = {
        "HTML": 58.1,
        "CSS": 41.9
    }

    mockGet.return_value = MagicMock(status_code=200, json=lambda: mockResponse)
    result = getLanguagesInfo("octocat/Spoon-Knife", "TestToken")

    assert result["languages"]["HTML"] == 58.1
    assert result["languages"]["CSS"] == 41.9

@patch("gitfo.github_api.requests.get")
def testGetReleasesInfo(mockGet):
    mockResponse = {
        "tag_name": "v2.3.1",
        "name": "v2.3.1 (Jun 21,  2025)",
        "published_at": "2025-06-21T13:02:28Z",
        "body": "# NumPy 2.3.1 Release Notes\r",
        "html_url": "https://github.com/numpy/numpy/releases/tag/v2.3.1"
    }

    mockGet.return_value = MagicMock(status_code=200, json=lambda: mockResponse)
    result = getReleasesInfo("octocat/Spoon-Knife", "TestToken")

    assert result["latest_release"]["tag_name"] == "v2.3.1"
    assert result["latest_release"]["name"] == "v2.3.1 (Jun 21,  2025)"
    assert result["latest_release"]["published_at"] == "2025-06-21T13:02:28Z"
    assert result["latest_release"]["body"] == "# NumPy 2.3.1 Release Notes\r"
    assert result["latest_release"]["html_url"] == "https://github.com/numpy/numpy/releases/tag/v2.3.1"

@patch("gitfo.github_api.requests.get")
def testGetOpenPRCount(mockGet):
    mockResponse = {
        "total_count": 600,
        "items": []
    }

    mockGet.return_value = MagicMock(status_code=200, json=lambda: mockResponse)
    result = getOpenPRCount("octocat/Hello-World", "TestToken")

    assert result["open_pull_requests"] == 600

@patch("gitfo.github_api.requests.get")
def testGetRateLimit(mockGet):
    mockResponse = {
        "resources": {
            "core": {
                "limit": 5000,
                "used": 0,
                "remaining": 5000
            }
        }
    }

    mockGet.return_value = MagicMock(status_code=200, json=lambda: mockResponse)
    result = getRateLimit("TestToken")

    assert result["limit"] == 5000
    assert result["used"] == 0
    assert result["remaining"] == 5000

@patch("gitfo.github_api.requests.get")
def testGetRateLimitBadCredentials(mockGet):
    mockResponse = {"message": "Bad credentials"}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getRateLimit("BadToken")

    assert result == {"message": "Bad credentials"}

@patch("gitfo.github_api.requests.get")
def testGetUserInfo(mockGet):
    mockResponse = {
        "login": "octocat",
        "id": 583231,
        "type": "User",
        "name": "The Octocat",
        "company": "@github",
        "blog": "https://github.blog",
        "location": "San Francisco",
        "email": None,
        "bio": None,
        "twitter_username": None,
        "public_repos": 8,
        "public_gists": 8,
        "followers": 18464,
        "following": 9,
        "created_at": "2011-01-25T18:44:36Z",
        "updated_at": "2025-06-22T11:21:58Z"
    }

    mockGet.return_value = MagicMock(status_code=200, json=lambda: mockResponse)
    result = getUserInfo("octocat", "TestToken")

    assert result["login"] == "octocat"
    assert result["company"] == "@github"
    assert result["email"] == None
    assert result["public_repos"] == 8 
    assert result["followers"] == 18464
    assert result["created_at"] == "2011-01-25T18:44:36Z"

@patch("gitfo.github_api.requests.get")
def testGetUserInfoNotFound(mockGet):
    mockResponse = {"message": "Not Found"}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getUserInfo("nonexistentUser", "TestToken")

    assert result == {"message": "Not Found"}

@patch("gitfo.github_api.requests.get")
def testGetUserInfoBadCredentials(mockGet):
    mockResponse = {"message": "Bad credentials"}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getUserInfo("octocat", "BadToken")

    assert result == {"message": "Bad credentials"}

@patch("gitfo.github_api.requests.get")
def testGetUserInfoRateLimitExceeded(mockGet):
    mockResponse = {"message": "API rate limit exceeded for user."}

    mockGet.return_value = MagicMock(status_code=404, json=lambda: mockResponse)
    result = getUserInfo("octocat", "TestToken")

    assert result == {"message": "API rate limit exceeded for user."}