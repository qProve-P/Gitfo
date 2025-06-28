import typer
from typing_extensions import Annotated, Optional
from gitfo import __appName__, __version__
from .github_api import getRepoInfo, getLanguagesInfo,getReleasesInfo, getOpenPRCount, getBranchesInfo, getRateLimit, getUserInfo
from .util import printOutput, printOutputToFile

app = typer.Typer(name=__appName__)

def _versionCallback(value: bool, ctx: typer.Context):
    if value:
        typer.echo(f"{__appName__} v{__version__}")
        raise typer.Exit()

@app.callback()
def version(version: Annotated[Optional[bool], typer.Option("--version", "-v", help="Show the application's version.", callback=_versionCallback, is_eager=True)]=False):
    return

@app.command()
def limit(auth: Annotated[str, typer.Argument(help="Your Github token for authorization.")]):
    info = getRateLimit(auth)

    if "message" in info and info["message"] == "Bad credentials":
        typer.secho(f"Authorization token incorrect!", fg=typer.colors.RED)
        return

    printOutput(info)

@app.command()
def repo(
    target: Annotated[str, typer.Argument(help="Target Github repository.(owner/repository)")], 
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="Name of output file. Supported file types: .txt|.csv|.json.")]=None,
    full: Annotated[Optional[bool], typer.Option("--full", help="Retrieve full details about the repository.(Requires more requests)")]=False,
    languages: Annotated[Optional[bool], typer.Option("--with-languages", help="Get full language breakdown.(Requires more requests)")]=False,
    auth: Annotated[Optional[str], typer.Option("--auth", "-a", help="Your Github token for authorization.")]=None,
):
    info = getRepoInfo(target, auth)

    if "message" in info:
        if "Not Found" in info["message"]:
            typer.secho(f"Repository '{target}' not found!", fg=typer.colors.RED)
            return
        elif "Bad credentials" in info["message"]:
            typer.secho(f"Authorization token incorrect!", fg=typer.colors.RED)
            return
        elif "rate limit exceeded" in info["message"].lower():
            typer.secho("Rate limit exceeded! Try again tomorrow or use authorization.", fg=typer.colors.RED)
            return

    if full:
        languages = True

        releasesInfo = getReleasesInfo(target, auth)
        info.update(releasesInfo)

        pRCountInfo = getOpenPRCount(target, auth)
        info.update(pRCountInfo)

        branchesInfo = getBranchesInfo(target, auth)
        info.update(branchesInfo)
    
    if languages:
        langInfo = getLanguagesInfo(target, auth)
        info.update(langInfo)
    
    if output:
        printOutputToFile(info, output)
    else:
        printOutput(info)

@app.command()
def user(
    target: Annotated[str, typer.Argument(help="Target Github username.")],
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="Name of output file. Supported file types: .txt|.csv|.json.")]=None,
    auth: Annotated[Optional[str], typer.Option("--auth", "-a", help="Your Github token for authorization.")]=None,
):
    info = getUserInfo(target, auth)

    if "message" in info:
        if info["message"] == "Not Found":
            typer.secho(f"User '{target}' not found!", fg=typer.colors.RED)
            return
        elif info["message"] == "Bad credentials":
            typer.secho(f"Authorization token incorrect!", fg=typer.colors.RED)
            return
        elif "rate limit exceeded" in info["message"].lower():
            typer.secho("Rate limit exceeded! Try again tomorrow or use authorization.", fg=typer.colors.RED)
            return
    
    if output:
        printOutputToFile(info, output)
    else:
        printOutput(info)