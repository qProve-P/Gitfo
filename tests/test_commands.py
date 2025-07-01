#################################
#       Tests for main.py       #
#################################

import pytest, typer
from typer.testing import CliRunner
from unittest.mock import patch
from gitfo import __appName__, __version__
from gitfo.main import version, limit, repo, user, repobatch, userbatch, app

runner = CliRunner()

def testVersionOption():
    result = runner.invoke(app, ["--version"])

    assert f"{__appName__} v{__version__}" in result.output
    assert result.exit_code == 0

@patch("gitfo.main.getRateLimit")
@patch("gitfo.main.printOutput")
def testLimitValidToken(mockPrintOutput, mockgetRateLimit):
    mockgetRateLimit.return_value = {
        "limit": 5000,
        "used": 100,
        "remaining": 4900
    }

    result = runner.invoke(app, ["limit", "validToken"])

    assert result.exit_code == 0
    mockPrintOutput.assert_called_once_with({
        "limit": 5000,
        "used": 100,
        "remaining": 4900
    })

@patch("gitfo.main.getRateLimit")
def testLimitBadToken(mockgetRateLimit):
    mockgetRateLimit.return_value = {
        "message": "Bad credentials"
    }

    result = runner.invoke(app, ["limit", "badToken"])

    assert result.exit_code == 0
    assert "authorization token incorrect" in result.output.lower()

@patch("gitfo.main.getRepoInfo")
@patch("gitfo.main.printOutput")
def testRepoBasic(mockPrintOutput, mockGetRepoInfo):
    mockGetRepoInfo.return_value = {
        "name": "Hello-World",
        "stars": 3004
    }

    result = runner.invoke(app, ["repo", "octocat/Hello-World"])

    assert result.exit_code == 0
    mockPrintOutput.assert_called_once_with({
        "name": "Hello-World",
        "stars": 3004
    })

@patch("gitfo.main.getRepoInfo")
def testRepoNotFound(mockGetRepoInfo):
    mockGetRepoInfo.return_value = {
        "message": "Not Found"
    }

    result = runner.invoke(app, ["repo", "nonexistent/repo"])

    assert "not found" in result.output.lower()
    assert result.exit_code == 0

@patch("gitfo.main.getRepoInfo")
def testRepoBadCredentials(mockGetRepoInfo):
    mockGetRepoInfo.return_value = {
        "message": "Bad credentials"
    }

    result = runner.invoke(app, ["repo", "octocat/Hello-World", "--auth", "BadToken"])

    assert "authorization token incorrect" in result.output.lower()
    assert result.exit_code == 0

@patch("gitfo.main.getRepoInfo")
def testRepoRateLimitExceeded(mockGetRepoInfo):
    mockGetRepoInfo.return_value = {
        "message": "API Rate Limit Exceeded"
    }

    result = runner.invoke(app, ["repo", "octocat/Hello-World"])

    assert "rate limit exceeded" in result.output.lower()
    assert result.exit_code == 0

@patch("gitfo.main.printOutputToFile")
@patch("gitfo.main.getRepoInfo")
@patch("gitfo.main.getReleasesInfo")
@patch("gitfo.main.getOpenPRCount")
@patch("gitfo.main.getBranchesInfo")
@patch("gitfo.main.getLanguagesInfo")
def testRepoFullOutputToFile(
    mockGetLanguages,
    mockGetBranches,
    mockGetPRS,
    mockGetReleases,
    mockGetRepoInfo,
    mockOutputFile
):
    mockGetRepoInfo.return_value = {"name": "Repo"}
    mockGetReleases.return_value = {"release": "data"}
    mockGetPRS.return_value = {"prs": 42}
    mockGetBranches.return_value = {"branches": ["main"]}
    mockGetLanguages.return_value = {"languages": {"Python": 95}}

    result = runner.invoke(app, [
        "repo", "octocat/Hello-World", "--full", "--output", "repo.json", "--auth", "token"
    ])

    assert result.exit_code == 0
    mockOutputFile.assert_called_once()

@patch("gitfo.main.getUserInfo")
@patch("gitfo.main.printOutput")
def testUserBasic(mockPrintOutput, mockGetUserInfo):
    mockGetUserInfo.return_value = {
        "login": "octocat", 
        "id": 1
    }
    
    result = runner.invoke(app, ["user", "octocat"])
    
    assert result.exit_code == 0
    mockPrintOutput.assert_called_once_with({
        "login": "octocat", 
        "id": 1
    })

@patch("gitfo.main.getUserInfo")
@patch("gitfo.main.printOutputToFile")
def testUserToFile(mockOutputFile, mockGetUserInfo):
    mockGetUserInfo.return_value = {
        "login": "octocat", 
        "id": 1
    }

    result = runner.invoke(app, ["user", "octocat", "--output", "user.json"])

    assert result.exit_code == 0
    mockOutputFile.assert_called_once_with({"login": "octocat", "id": 1}, "user.json")


@patch("gitfo.main.getUserInfo")
def testUserNotFound(mockGetUserInfo):
    mockGetUserInfo.return_value = {
        "message": "Not Found"
    }

    result = runner.invoke(app, ["user", "nonexistentuser"])

    assert result.exit_code == 0
    assert "not found" in result.output.lower()

@patch("gitfo.main.getUserInfo")
def testUserBadCredentials(mockGetUserInfo):
    mockGetUserInfo.return_value = {
        "message": "Bad credentials"
    }

    result = runner.invoke(app, ["user", "octocat", "--auth", "BadToken"])
    
    assert result.exit_code == 0
    assert "authorization token incorrect" in result.output.lower()

@patch("gitfo.main.getUserInfo")
def testUserRateLimitExceeded(mockGetUserInfo):
    mockGetUserInfo.return_value = {
        "message": "API rate limit exceeded"
    }

    result = runner.invoke(app, ["user", "octocat"])
    
    assert result.exit_code == 0
    assert "rate limit exceeded" in result.output.lower()

@patch("gitfo.main.printMultipleToFile")
@patch("gitfo.main.getLanguagesInfo")
@patch("gitfo.main.getBranchesInfo")
@patch("gitfo.main.getOpenPRCount")
@patch("gitfo.main.getReleasesInfo")
@patch("gitfo.main.getRepoInfo")
@patch("gitfo.main.getItems")
@patch("pathlib.Path.is_file")
def testRepobatch(
    mockIsFile,
    mockGetItems,
    mockGetRepoInfo,
    mockGetReleasesInfo,
    mockGetOpenPRCount,
    mockGetBranchesInfo,
    mockGetLanguagesInfo,
    mockPrintMultipleToFile,
):
    mockIsFile.return_value = True
    mockGetItems.return_value = ["owner/repo1", "owner/repo2"]

    mockGetRepoInfo.side_effect = lambda repo, auth: {"repo": repo, "basic": True}
    mockGetReleasesInfo.return_value = {"releases": "data"}
    mockGetOpenPRCount.return_value = {"prs": 5}
    mockGetBranchesInfo.return_value = {"branches": ["main"]}
    mockGetLanguagesInfo.return_value = {"languages": {"Python": 100}}

    result = runner.invoke(
        app,
        ["repobatch", "repos.txt", "output.json", "--full", "--with-languages"]
    )

    assert result.exit_code == 0
    mockIsFile.assert_called_once_with()
    mockGetItems.assert_called_once_with("repos.txt")
    assert mockGetRepoInfo.call_count == 2
    assert mockGetReleasesInfo.call_count == 2
    assert mockGetOpenPRCount.call_count == 2
    assert mockGetBranchesInfo.call_count == 2
    assert mockGetLanguagesInfo.call_count >= 2
    mockPrintMultipleToFile.assert_called_once()
    args, kwargs = mockPrintMultipleToFile.call_args
    assert isinstance(args[0], list)
    assert args[1] == "output.json"

@patch("pathlib.Path.is_file")
def testRepobatchBadSource(mockIsFile):
    mockIsFile.return_value = False

    runner = CliRunner()
    result = runner.invoke(app, ["repobatch", "nonexistent.txt", "output.json"])

    assert "does not exist" in result.output

@patch("gitfo.main.printMultipleToFile")
@patch("gitfo.main.getUserInfo")
@patch("gitfo.main.getItems")
@patch("pathlib.Path.is_file")
def testUserbatch(
    mockIsFile,
    mockGetItems,
    mockGetUserInfo,
    mockPrintMultipleToFile,
):
    mockIsFile.return_value = True
    mockGetItems.return_value = ["user1", "user2"]
    mockGetUserInfo.side_effect = lambda user, auth: {"user": user, "info": True}

    result = runner.invoke(
        app,
        ["userbatch", "users.txt", "output.json", "--auth", "mytoken"]
    )

    assert result.exit_code == 0
    mockIsFile.assert_called_once_with()
    mockGetItems.assert_called_once_with("users.txt")
    assert mockGetUserInfo.call_count == 2
    mockGetUserInfo.assert_any_call("user1", "mytoken")
    mockGetUserInfo.assert_any_call("user2", "mytoken")
    mockPrintMultipleToFile.assert_called_once()
    args, kwargs = mockPrintMultipleToFile.call_args
    assert isinstance(args[0], list)
    assert args[1] == "output.json"

@patch("pathlib.Path.is_file")
def testUserbatchBadSource(mockIsFile):
    mockIsFile.return_value = False

    runner = CliRunner()
    result = runner.invoke(app, ["userbatch", "nonexistent.txt", "output.json"])

    assert "does not exist" in result.output