import typer
import requests
from typing_extensions import Annotated, Optional
from gitfo import __appName__, __version__

app = typer.Typer(name=__appName__)

def _versionCallback(value: bool, ctx: typer.Context):
    if value:
        typer.echo(f"{__appName__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Annotated[bool, typer.Option("--version", "-v", help="Show the application's version.", callback=_versionCallback, is_eager=True)]=False):
    return

@app.command()
def info(url: Annotated[str, typer.Argument(help="Url of git repo.")], output: Annotated[Optional[str], typer.Option("--output", "-o", help="Name of output file.")]=None):
    pass

@app.command()
def analyse(url: Annotated[str, typer.Argument(help="Url of git repo.")], output: Annotated[Optional[str], typer.Option("--output", "-o", help="Name of output file.")]=None):
    pass