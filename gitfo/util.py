import csv

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
