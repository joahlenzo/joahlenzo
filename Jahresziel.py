import json

def ziel_speichern(ziel):
    datei = "Jahresziel.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    inhalt = {"Jahresziel":ziel}



    with open(datei, "w") as open_file:
        json.dump(inhalt, open_file, indent=1)

def ziel_laden():
    datei_name = "Jahresziel.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = {}

    return datei_inhalt
