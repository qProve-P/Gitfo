import csv, json, typer

def prepareForCsv(info: dict)-> dict:
    out = {}
    for key, value in info.items():
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
                typer.secho(f"File type '.{fileType}' is not supported. Use .txt|.csv|.json.", fg=typer.colors.RED)
                return

def printMultipleToFile(infos: list, outputFile: str)-> None:
    fileType = outputFile.split(".")[-1]
    with open(outputFile, "w+") as f:
        match fileType:
            case "txt":
                for info in infos:
                    for key, value in info.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            case "csv":
                fieldnames = infos[0].keys()
                for i in range(len(infos)):
                    infos[i] = prepareForCsv(infos[i])

                writer = csv.DictWriter(f, fieldnames)
                writer.writeheader()
                writer.writerows(infos)
            case "json":
                json.dump(infos, f, ensure_ascii=False, indent=2)
            case _:
                typer.secho(f"File type '.{fileType}' is not supported. Use .txt|.csv|.json.", fg=typer.colors.RED)
                return

def getHeaders(token: str)-> dict:
    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
    }

    if token != None:
        headers["Authorization"] = f"token {token}"

    return headers

def getItems(source: str)-> list:
    fileType = source.split(".")[-1]
    if fileType != "txt":
        typer.secho(f"File type '.{fileType}' is not supported as a source file. Use .txt.", fg=typer.colors.RED)
        raise typer.Exit()
    
    with open(source, "r") as s:
        out = [line.strip() for line in s]

    return out