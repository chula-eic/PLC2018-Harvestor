import json

def load():
    with open('color.json', 'r') as f:
        color = json.load(f)
    return color

def yellow():
    return load['yellow']

def brown():
    return load()['brown']

def green():
    return load()['green']