import json

def saveSettings(filename, settings):
    with open(filename, 'w') as f:
        json.dump(settings, f)

def loadSettings(filename):
    with open(filename, 'r') as f:
        return json.load(f)