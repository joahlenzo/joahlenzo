from flask import Flask
from flask import render_template
from flask import request
from Datenbankabfrage import eingabe_laden, speichern
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go



app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    #todo: Klare Anzeige von Einnahmen und Ausgaben (mit Minus)
    #todo: Wenn falsche Daten eingegeben werden - Fehler Meldung anzeigen

    # get = Inhalt von eingabe.html dem Client anzeigen
    if request.method.lower() == "get":
        names = ['Bob', 'Cindy', 'Noah']
        names.pop()
        return render_template('index.html',test=names)
    # post = ausgefüllte Daten vom Formular von Client via url /eingabe erhalten
    if request.method.lower() == "post":
        input_ausgaben = int(request.form['Ausgaben'])
        input_kategorie = request.form["Kategorie"]
        input_datum = request.form["Datum"]
    #Speicherung Daten in JSON
        speichern(input_ausgaben, input_kategorie, input_datum)
    #Antwortsatz
        eingabe_gespeichert = "Dein Eintrag wurde erfolgreich gespeichert"
        return render_template("index.html", eingabe=eingabe_gespeichert) #Nach Sendebutton anzeigen
    return render_template("index.html")


@app.route("/ausgaben", methods=["GET", "POST"])
def ausgaben():
    # get = Inhalt der Finanzen.html wird angezeigt
    if request.method.lower() == "get":
        return render_template("Ausgaben.html")
    # post = Formulardaten erhalten
    if request.method.lower() == "post":
        kategorie_filter = request.form['Kategorie']
        monat_filterung = request.form['Monat']

        # Daten filtern und zusammenzählen
        daten_filtern = eingabe_laden()
        gefilterte_elemente = []
        summe = 0
        for liste_elemente in daten_filtern:
            if liste_elemente['Kategorie'] == kategorie_filter and liste_elemente['Datum'].split('-')[1] == monat_filterung:
                gefilterte_elemente.append(liste_elemente)
                summe += liste_elemente["Ausgaben"]
            Aussagesatz = "Du hast im " + monat_filterung + "-ten Monat " + str(summe) + " SFR nur für die Kategorie " + kategorie_filter + " ausgegeben!"
        return render_template("Ausgaben.html", liste_elemente=gefilterte_elemente, summe=summe, Kategorie=kategorie_filter, Aussagesatz=Aussagesatz)
    return render_template("Ausgaben.html")


@app.route("/finanzen")
def finanzen():
    #todo: Kommentare überall (Python & HTML)
    daten_filtern = eingabe_laden()
    ausgaben_kategorie = {}
    #Füllt das leere Dict dynamisch mit Kategorien und Ausgaben/Kategorie
    for elemente in daten_filtern:
        if elemente["Kategorie"] in ausgaben_kategorie:
            ausgaben_kategorie[elemente["Kategorie"]] += elemente["Ausgaben"]
        else:
            ausgaben_kategorie[elemente["Kategorie"]] = elemente["Ausgaben"]
    #Erstellt Listen für Datenvisualsierung
    kategorien = list(ausgaben_kategorie.keys())
    summierte_ausgaben = list(ausgaben_kategorie.values())
    #Visualisierung mit Plotly
    fig = px.bar(x=kategorien, y=summierte_ausgaben)
    fig.update_layout(
        title="Gesamte Ausgaben pro Kategorie",
        xaxis_title="Kategorien",
        yaxis_title="Ausgaben")
    div = plot(fig, output_type="div")
    return render_template("Finanzen.html", visualisierung=div)


@app.route("/jahresziel")
def jahresziel():
    #todo: Jahresziel muss Usereingabe sein - ansonsten sinnlos
    #todo: Flowchart / staticordner / Readme anpassen
    #todo: CSS einbauen
    Jahresziel = 30000
    summe_ausgaben = 0
    namenliste = ["Verfügbare Ausgaben", "Ausgegeben"]
    summenliste = []
    daten_zusammenzählen = eingabe_laden()


    for elemente in daten_zusammenzählen:
        summe_ausgaben += elemente["Ausgaben"]
        goal_jahresziel = Jahresziel - summe_ausgaben
    summenliste.append(goal_jahresziel)
    summenliste.append(summe_ausgaben)

    fig = px.pie(values=summenliste, names=namenliste, title="Jahresziel",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition="inside", textinfo="value")
    div = plot(fig, output_type="div")




    return render_template("Jahresziel.html", summiert=summe_ausgaben, jahresziel=goal_jahresziel, jahresziel_ungerechnet=Jahresziel, visualisierung=div)


if __name__ == "__main__":
    app.run(debug=True, port=5000)