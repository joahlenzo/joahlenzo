from flask import Flask
from flask import render_template
from flask import request
from Datenbankabfrage import eingabe_laden, speichern, loeschen
import plotly.express as px
from plotly.offline import plot
from Jahresziel import ziel_speichern, ziel_laden

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # todo: Klare Anzeige von Einnahmen und Ausgaben (mit Minus)
    # todo: Wenn keine Daten eingegeben werden - Fehler Meldung anzeigen
    # get = Inhalt von eingabe.html dem Client anzeigen
    leere_elemente = {0:0}
    if request.method.lower() == "get":
        return render_template('index.html', loeschung=leere_elemente)
    # post = ausgefüllte Daten vom Formular von Client via url /eingabe erhalten
    if request.method.lower() == "post":
        if request.form.get("action1") == "VALUE1":
            input_ausgaben = request.form['Ausgaben']
            input_kategorie = request.form["Kategorie"]
            input_datum = request.form["Datum"]
            #Fehlermeldung falls nicht alle Daten eingegeben wurden
            if not input_ausgaben or not input_kategorie or not input_datum:
                error_statement = "To lazy. Bitte fülle alle Felder aus"
                return render_template("index.html",error=error_statement, ausgaben=input_ausgaben,kategorie=input_kategorie,datum=input_datum, loeschung=leere_elemente)

            # Speicherung Daten in JSON
            speichern(int(input_ausgaben), input_kategorie, input_datum)
            # Antwortsatz
            eingabe_gespeichert = "Dein Eintrag wurde erfolgreich gespeichert"  # Nach Sendebutton anzeigen
            return render_template("index.html", speichersatz=eingabe_gespeichert, loeschung=leere_elemente)  # Nach Sendebutton anzeigen
        elif request.form.get("action2") == "VALUE2":
            eingaben_loeschen = eingabe_laden()
            if not eingaben_loeschen:
                return render_template("index.html", loeschung=leere_elemente)
            else:
                element_loeschen = eingaben_loeschen.pop()
                geloescht = eingaben_loeschen
                loeschen(geloescht)
                löschsatz = "Dein Eintrag wurde erfolgreich gelöscht"   # Nach Löschbutton anzeigen
                return render_template("index.html", löschungssatz=löschsatz, loeschung=element_loeschen)




@app.route("/ausgaben", methods=["GET", "POST"])
def ausgaben():
    keine_daten = "In diesem Monat und diesem Genre hast du kein Geld ausgegeben. Gratuliere!"
    # get = Inhalt der Finanzen.html wird angezeigt
    if request.method.lower() == "get":
        daten_anzeigen = eingabe_laden()
        Hinweissatz = "Hier hast du eine Übersicht über alle getätigten Aussagen"
        return render_template("Ausgaben.html", liste_elemente=daten_anzeigen, Aussagesatz=Hinweissatz)
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
                if not gefilterte_elemente:
                    return render_template("Ausgaben.html", Aussagesatz=keine_daten)
                else:
                    Aussagesatz = "Du hast im " + monat_filterung + "-ten Monat " + str(
                        summe) + " SFR nur für die Kategorie " + kategorie_filter + " ausgegeben!"
                    return render_template("Ausgaben.html", liste_elemente=gefilterte_elemente, summe=summe,Kategorie=kategorie_filter, Aussagesatz=Aussagesatz)
    return render_template("Ausgaben.html", Aussagesatz=keine_daten)


@app.route("/finanzen")
def finanzen():
    # todo: Kommentare überall (Python & HTML)
    daten_filtern = eingabe_laden()
    ausgaben_kategorie = {}
    keine_daten = "Du hast noch gar keine Ausgaben eingegeben! Etwas ausgegeben aber wahrscheinlich schon ;-)"
    # Füllt das leere Dict dynamisch mit Kategorien und Ausgaben/Kategorie
    # Summiert alle Ausgaben einer entsprechenden Kategorie
    if not daten_filtern:
        return render_template("Finanzen.html", Aussagesatz=keine_daten)
    else:
        for elemente in daten_filtern:
            if elemente["Kategorie"] in ausgaben_kategorie:
                ausgaben_kategorie[elemente["Kategorie"]] += elemente["Ausgaben"]
            else:
                ausgaben_kategorie[elemente["Kategorie"]] = elemente["Ausgaben"]
        # Erstellt Listen für Datenvisualsierung
        kategorien = list(ausgaben_kategorie.keys())
        summierte_ausgaben = list(ausgaben_kategorie.values())
        # Visualisierung mit Plotly
        fig = px.bar(x=kategorien, y=summierte_ausgaben)
        fig.update_layout(
            title="Gesamte Ausgaben pro Kategorie",
            xaxis_title="Kategorien",
            yaxis_title="Ausgaben")
        div = plot(fig, output_type="div")
        return render_template("Finanzen.html", visualisierung=div)


@app.route("/jahresziel",  methods=["GET", "POST"])
def jahresziel():
    # todo: Flowchart / staticordner / Readme anpassen
    goal_jahresziel = 0
    summe_ausgaben = 0
    namenliste = ["Verfügbare Ausgaben", "Ausgegeben"]
    summenliste = []
    daten_zusammenzählen = eingabe_laden()
    for elemente in daten_zusammenzählen:
        summe_ausgaben += elemente["Ausgaben"]

    if request.method.lower() == "get":
        jahresziel_anzeigen = ziel_laden()
        Jahresziel = jahresziel_anzeigen["Jahresziel"]
        goal_jahresziel = Jahresziel - summe_ausgaben
        summenliste.append(goal_jahresziel)
        summenliste.append(summe_ausgaben)
        fig = px.pie(values=summenliste, names=namenliste, title="Jahresziel",
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_traces(textposition="inside", textinfo="value")
        div = plot(fig, output_type="div")

        return render_template("Jahresziel.html", summiert=summe_ausgaben, jahresziel=goal_jahresziel,
                               jahresziel_ungerechnet=Jahresziel, visualisierung=div)
    # post = ausgefüllte Daten vom Formular von Client via url /eingabe erhalten
    if request.method.lower() == "post":
        ziel = int(request.form['Ziel'])
        ziel_speichern(ziel)
        return render_template("landing_page.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
