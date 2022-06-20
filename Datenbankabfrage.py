import json
from datetime import datetime
from json import JSONEncoder
import os


#   json-file wird geöffnet
def speichern(input_ausgaben, input_kategorie, input_datum):
    datei = "datenbank.json"
    heute = str(datetime.utcnow())
    heute = heute.replace(" ", "")
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []
    #   Dict für Datenbank (Variablen werden von Formular ausfüllen (def index) geholt)
    inhalt = {"Ausgaben": input_ausgaben,
              "Kategorie": input_kategorie,
              "Datum": input_datum,
              "UID": heute
              }
    datei_inhalt.append(inhalt)
    #   json-file wird geschrieben mit w = write
    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4, cls=DateTimeEncoder)


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


#funktion um json file zu laden
def eingabe_laden():
    datei_name = "datenbank.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    return datei_inhalt


#   Funktion holt Daten durch Formular mit Delete Button und überschreibt Datenbankabfrage
def loeschen(geloescht):
    datei = "datenbank.json"
    with open(datei, "w") as open_file:
        json.dump(geloescht, open_file, indent=4)













