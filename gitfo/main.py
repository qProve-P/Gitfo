import typer, csv, json
from typing_extensions import Annotated, Optional
from gitfo import __appName__, __version__
from .github_api import getRepoInfo, getLanguagesInfo, getRateLimit, getUserInfo
from .util import prepareForCsv, printOutput

app = typer.Typer(name=__appName__)

def _versionCallback(value: bool, ctx: typer.Context):
    if value:
        typer.echo(f"{__appName__} v{__version__}")
        raise typer.Exit()

@app.callback()
def version(version: Annotated[bool, typer.Option("--version", "-v", help="Show the application's version.", callback=_versionCallback, is_eager=True)]=False):
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
    url: Annotated[str, typer.Argument(help="Url of git repository.")], 
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="Name of output file. Supported file types: .txt|.csv|.json.")]=None,
    full: Annotated[Optional[bool], typer.Option("--full", help="Retrieve full details about the repository.(Requires more requests)")]=False,
    languages: Annotated[Optional[bool], typer.Option("--with-languages", help="Get full language breakdown.(Requires more requests)")]=False,
    auth: Annotated[Optional[str], typer.Option("--auth", "-a", help="Your Github token for authorization.")]="",
):
    info = getRepoInfo(url, auth)

    # if full:
    #     languages = True
    #     requestsInfo = getRequestsInfo(url, auth)
    
    if languages:
        langInfo = getLanguagesInfo(url, auth)
        info.update(langInfo)
    
    if "message" in info:
        if info["message"] == "Not Found":
            typer.secho(f"Repository '{url}' not found!", fg=typer.colors.RED)
            return
        elif info["message"] == "Bad credentials":
            typer.secho(f"Authorization token incorrect!", fg=typer.colors.RED)
            return
    
    if output:
        fileType = output.split(".")[-1]
        with open(output, "w+") as f:
            match fileType:
                case "txt":
                    for key, value in info.items():
                        f.write(f"{key}: {value}\n")
                case "csv":
                    info = prepareForCsv(info)
                    writer = csv.DictWriter(f, info.keys())
                    writer.writeheader()
                    writer.writerow(info)
                case "json":
                    json.dump(info, f, ensure_ascii=False, indent=2)
                case _:
                    typer.secho(f".{fileType} is not supported. Use .txt|.csv|.json.", fg=typer.colors.RED)
    else:
        printOutput(info)

@app.command()
def user():
    pass