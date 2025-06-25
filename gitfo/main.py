import typer, csv, json
from typing_extensions import Annotated, Optional
from gitfo import __appName__, __version__
from .github_api import getRepoInfo, getUserInfo
from .util import prepareForCsv

app = typer.Typer(name=__appName__)

def _versionCallback(value: bool, ctx: typer.Context):
    if value:
        typer.echo(f"{__appName__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Annotated[bool, typer.Option("--version", "-v", help="Show the application's version.", callback=_versionCallback, is_eager=True)]=False):
    return

@app.command()
def repo(
    url: Annotated[str, typer.Argument(help="Url of git repository.")], 
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="Name of output file. Supported file types: .txt, .csv, .json.")]=None,
    full: Annotated[Optional[bool], typer.Option("--full", help="Retrieve full details about the repository.(Requires more requests)")]=False,
    languages: Annotated[Optional[bool], typer.Option("--with-languages", help="Get full language breakdown.(Requires more requests)")]=False
):
    info = getRepoInfo(url)
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
        for key, value in info.items():
            key = typer.style(key, fg=typer.colors.GREEN)
            if isinstance(value, list):
                typer.echo(f"{key}:")
                for elem in value:
                    typer.echo(f"\t{elem}")
            elif isinstance(value, dict):
                typer.echo(f"{key}:")
                for valKey, valVal in value.items():
                    valKey = typer.style(valKey, fg=typer.colors.BLUE)
                    typer.echo(f"\t{valKey}: {valVal}")
            else:
                typer.echo(f"{key}: {value}")
    
    if full:
        print(f"--full")
    
    if languages:
        print(f"--lang")

@app.command()
def user():
    pass