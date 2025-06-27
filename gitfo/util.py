import csv, typer

def prepareForCsv(dictonary: dict)-> dict:
    out = {}
    for key, value in dictonary.items():
        if isinstance(value, list):
            out[key] = "|".join(map(str, value))
        elif isinstance(value, dict):
            out[key] = "|".join(f"{k}:{v}" for k, v in value.items())
        else:
            out[key] = value
    
    return out

def printOutput(inp: dict)-> None:
    for key, value in inp.items():
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

def getHeaders(token: str)-> dict:
    return {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {token}"
    }