import json


#json-file wird geschrieben mit w = write
def speichern(input_ausgaben, input_kategorie, input_datum):
    datei = "datenbank.json"
    try:
        with open(datei) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []
        print("Sorry, finde nix mit diese")

    inhalt = {"Ausgaben": input_ausgaben,
              "Kategorie": input_kategorie,
              "Datum": input_datum}
    datei_inhalt.append(inhalt)

    with open(datei, "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=3)

#funktion um json file zu laden
def eingabe_laden():
    datei_name = "datenbank.json"

    try:
        with open(datei_name) as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    return datei_inhalt

def viz():
    kategorie, summe = Datenbankabfrage.eingabe_laden()
    fig = px.bar(x=kategorie, y=summe)
    fig.update_layout(
        title="Totale Ausgaben pro Kategorien",
        xaxis_title="Kategorie",
        yaxis_title="Ausgaben")
    div = plot(fig, output_type="div")
    return div