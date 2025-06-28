import csv, json, typer

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

def printOutput(info: dict)-> None:
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

def printOutputToFile(info: dict, outputFile: str)-> None:
    fileType = outputFile.split(".")[-1]
    with open(outputFile, "w+") as f:
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
                return

def getHeaders(token: str)-> dict:
    return {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": f"token {token}"
    }