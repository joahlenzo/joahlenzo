from flask import Flask
from flask import render_template
from flask import request
import Datenbankabfrage



app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # get = Inhalt von eingabe.html dem Client anzeigen
    if request.method.lower() == "get":
        return render_template('index.html')
    # post = ausgefüllte Daten vom Formular von Client via url /eingabe erhalten
    if request.method.lower() == "post":
        input_ausgaben = int(request.form['Ausgaben'])
        input_kategorie = request.form["Kategorie"]
        input_datum = request.form["Datum"]

        Datenbankabfrage.speichern(input_ausgaben,input_kategorie,input_datum) #Speicherung Daten


        eingabe_gespeichert = "Dein Eintrag wurde erfolgreich gespeichert" #Nach Sendebutton anzeigen
        return render_template("index.html", eingabe=eingabe_gespeichert)
    return render_template("index.html")


@app.route("/ausgaben",methods=["GET", "POST"])
def ausgaben():
    # get = Inhalt der Finanzen.html wird angezeigt
    if request.method.lower() == "get":
        return render_template("Ausgaben.html")
    # post = Formulardaten erhalten
    if request.method.lower() == "post":
        kategorie_filter = request.form['Kategorie']
        monat_filterung = request.form['Monat']

        # Daten filtern und zusammenzählen
        daten_filtern = Datenbankabfrage.eingabe_laden()
        gefilterte_elemente = []
        summe = 0
        for liste_elemente in daten_filtern:
            if liste_elemente['Kategorie'] == kategorie_filter and liste_elemente['Datum'].split('-')[1] == monat_filterung:
                gefilterte_elemente.append(liste_elemente)
                summe += liste_elemente["Ausgaben"]
            Aussagesatz = "Du hast im " + monat_filterung + "-ten Monat " + str(summe) + " SFR nur für die Kategorie " + kategorie_filter + " ausgegeben!"
        return render_template("Ausgaben.html", liste_elemente=gefilterte_elemente, summe=summe, Kategorie=kategorie_filter, aussagesatz=Aussagesatz)
    return render_template("Ausgaben.html")


@app.route("/finanzen")
def finanzen():
    daten_filtern = Datenbankabfrage.eingabe_laden()
    kategorien = []
    summenliste = []
    for elemente in daten_filtern:
        kategorien_elemente = elemente["Kategorie"]
        kategorien.append(kategorien_elemente)
        summen = elemente["Ausgaben"]
        summenliste.append(summen)
    return render_template("Finanzen.html", kategorien=kategorien, summenliste=summenliste)


@app.route("/jahresziel")
def jahresziel():
    Jahresziel = 30000
    summe_ausgaben = 0
    daten_zusammenzählen = Datenbankabfrage.eingabe_laden()
    for elemente in daten_zusammenzählen:
        summe_ausgaben += elemente["Ausgaben"]
        goal_jahresziel = Jahresziel - summe_ausgaben
    return render_template("Jahresziel.html", summiert=summe_ausgaben, jahresziel=goal_jahresziel, jahresziel_ungerechnet=Jahresziel)


if __name__ == "__main__":
    app.run(debug=True, port=5000)