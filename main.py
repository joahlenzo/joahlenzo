from flask import Flask
from flask import render_template
from flask import request
from Datenbankabfrage import eingabe_laden, speichern, loeschen
import plotly.express as px
from plotly.offline import plot
from Jahresziel import ziel_speichern, ziel_laden
from os.path import exists



app = Flask(__name__)

#   Funktion für Dateneingabe und Datenveränderung durch Löschbutton
@app.route("/", methods=["GET", "POST"])
def index():
    #   get = Inhalt von eingabe.html dem Client anzeigen
    if request.method.lower() == "get":
        return render_template('index.html')
    #   post = ausgefüllte Daten vom Formular von Client via url /eingabe erhalten
    if request.method.lower() == "post":
        if request.form.get("action1") == "VALUE1":
            input_ausgaben = request.form['Ausgaben']
            input_kategorie = request.form['Kategorie']
            input_datum = request.form['Datum']
            #   Fehlermeldung falls nicht alle Daten eingegeben wurden
            if not input_ausgaben or not input_kategorie or not input_datum or int(input_ausgaben) == 0:
                error_statement = "Too lazy. Bitte fülle alle Felder aus. Ausgaben dürfen nicht 0 sein!"
                return render_template("index.html",error=error_statement, ausgaben=input_ausgaben, kategorie=input_kategorie, datum=input_datum)

            # Speicherung Daten in JSON
            speichern(int(input_ausgaben), input_kategorie, input_datum)
            # Antwortsatz
            eingabe_gespeichert = "Dein Eintrag wurde erfolgreich gespeichert"  # Nach Sendebutton anzeigen
            return render_template("index.html", speichersatz=eingabe_gespeichert)
        elif request.form.get("action2") == "VALUE2":
            eingaben_loeschen = eingabe_laden()
            #   Wenn keine Daten vorhanden sind, wird ein Hinweis geschaltet (Wenn gelöscht-Button gedrückt wird)
            if not eingaben_loeschen:
                aussagesatz = "Aktuell sind keine Elemente enthalten. Löschen läuft nicht."
                return render_template("index.html", antworten=aussagesatz)
            #   Wenn Daten vorhanden sind, werden die gelöschten Daten ans index.html übermittelt
            else:   # Letztes Element kann hier gelöscht werden
                element_loeschen = eingaben_loeschen.pop()
                loeschen(eingaben_loeschen)
                löschsatz = "Dein Eintrag wurde erfolgreich gelöscht"   # Nach Löschbutton anzeigen
                return render_template("index.html", löschungssatz=löschsatz, loeschung=element_loeschen)


@app.route("/ausgaben", methods=["GET", "POST"])
def ausgaben():
    #   Aussagesatz kommt, wenn keine Daten der Filterung entsprechen
    keine_daten = "In diesem Monat und diesem Genre hast du kein Geld ausgegeben. Gratuliere!"
    # get = Inhalt der Finanzen.html wird angezeigt
    if request.method.lower() == "get":
        daten_anzeigen = eingabe_laden()
        keine_ausgaben = "Deine Ausgaben sind also komplett zero --> 0"
        Hinweissatz = "Hier hast du eine Übersicht über alle getätigten Aussagen"   # Wenn keine Filterung gemacht wurde
        return render_template("Ausgaben.html", liste_elemente=daten_anzeigen, Aussagesatz=Hinweissatz, keine_ausgabe=keine_ausgaben)
    # post = Formulardaten erhalten
    if request.method.lower() == "post":
        if request.form.get("action1") == "VALUE1":     # Da zwei Postübermittlungen - individuelle Übermittlung
            kategorie_filter = request.form['Kategorie']
            monat_filterung = request.form['Monat']
            # Daten filtern und zusammenzählen
            daten_laden = eingabe_laden()
            gefilterte_elemente = []
            summe = 0
            for list_element in daten_laden:
                if list_element['Kategorie'] == kategorie_filter and list_element['Datum'].split('-')[1] == monat_filterung:    # Filterung nach Monat und Kategorie
                    gefilterte_elemente.append(list_element)
                    #   Zusammenzählen alle Ausgaben der Filterungselemente
                    summe += list_element["Ausgaben"]
                    #   Wenn keine Daten vorhanden sind, wird ein Hinweis geschaltet
            Filterungssatz = "Du hast im " + monat_filterung + "-ten Monat " + str(summe) + " SFR nur für die Kategorie " + kategorie_filter + " ausgegeben!"
            return render_template("Ausgaben.html", liste_elemente=gefilterte_elemente, summe=summe, Kategorie=kategorie_filter, Aussagesatz=Filterungssatz)
        else:   # Falls die zweite Übermittlung (Löschen Button in Tabelle)
            daten_löschen = eingabe_laden()
            match = request.form['UID']
            counter = -1    # counter zählt alle Elemente bis zum Match
            for geloescht in daten_löschen:
                counter = counter + 1
                if geloescht["UID"] == match:
                    del daten_löschen[counter]  # Entsprechendes Element wird gelöscht
                    loeschen(daten_löschen) # Angepasstes JSON File wird übermittelt (und dann überschrieben)
                    return render_template("Ausgaben.html", liste_elemente=daten_löschen)
    return render_template("Ausgaben.html", Aussagesatz=keine_daten)


@app.route("/finanzen")
def finanzen():
    keine_daten = "Du hast noch gar keine Ausgaben eingegeben! Etwas ausgegeben aber wahrscheinlich schon ;-)"  # Hinweissatz wenn keine Elemente vorhanden
    daten_filterung = eingabe_laden()
    #   Fragt ob Daten in Liste enthalten sind
    if not daten_filterung:
        return render_template("Finanzen.html", Aussagesatz=keine_daten)
    else:
        ausgaben_kategorie = {}
        for alle_elemente in daten_filterung:
            if alle_elemente["Kategorie"] in ausgaben_kategorie:  # Fragt ab, ob Kategorie in Dict
                ausgaben_kategorie[alle_elemente["Kategorie"]] += alle_elemente["Ausgaben"]   # Summiert alle Ausgaben einer entsprechenden Kategorie
            else:   # Erstellt Dict und visualisiert
                ausgaben_kategorie[alle_elemente["Kategorie"]] = alle_elemente["Ausgaben"]  # Füllt leeres Dict auf
        #   Erstellt Listen für Datenvisualsierung
        kategorien = list(ausgaben_kategorie.keys())    # Holt alle Kategorien und listet sie auf - wandelt dann in Liste um (f. Plotly)
        summierte_ausgaben = list(ausgaben_kategorie.values())  # Holt alle Summen und listet sie auf - wandelt dann in Liste um (f. Plotly)

        #   Visualisierung mit Plotly
        fig = px.bar(x=kategorien, y=summierte_ausgaben)
        fig.update_layout(
            title="Gesamte Ausgaben pro Kategorie",
            xaxis_title="Kategorien",
            yaxis_title="Ausgaben")
        div = plot(fig, output_type="div")
        return render_template("Finanzen.html", visualisierung=div)


#   Zeigt das Jahresziel an
@app.route("/jahresziel",  methods=["GET", "POST"])
def jahresziel():
    summe_ausgaben = 0
    namenliste = ["Verfügbare Ausgaben", "Ausgegeben"]
    summenliste = []
    daten_zusammenzählen = eingabe_laden()
    file_exists = exists("Jahresziel.json")
    if file_exists:     # Prüft, ob schon ein Jahresziel definiert wurde
        for elemente in daten_zusammenzählen:
            summe_ausgaben += elemente["Ausgaben"]
        #   get = Baut Visual für Datenvisualisierung mit Plotly
        if request.method.lower() == "get":
            #   Datenaufbereitung für Plotly
            jahresziel_anzeigen = ziel_laden()  # Holt Jahresziel Dict
            Jahresziel = jahresziel_anzeigen["Jahresziel"]
            goal_jahresziel = Jahresziel - summe_ausgaben
            summenliste.append(goal_jahresziel)
            summenliste.append(summe_ausgaben)
            #   Datenvisualisierung mit Plotly
            fig = px.pie(values=summenliste, names=namenliste, title="Jahresziel",
                         color_discrete_sequence=px.colors.sequential.matter)
            fig.update_traces(textposition="inside", textinfo="value")
            div = plot(fig, output_type="div")

            return render_template("Jahresziel.html", summiert=summe_ausgaben, jahresziel=goal_jahresziel,
                                   jahresziel_ungerechnet=Jahresziel, visualisierung=div)
        #   post = ausgefüllte Daten vom Formular von Client via url /eingabe erhalten
        if request.method.lower() == "post":
            ziel = int(request.form['Ziel'])
            ziel_speichern(ziel)
            return render_template("landing_page.html")
    else:
        aussagesatz = "Du hast noch kein Jahresziel angegeben. Mach es jetzt!"  # Zeigt an, dass noch kein Jahresziel definiert wurde
        #   post = ausgefüllte Daten vom Formular erhalten und speichern
        if request.method.lower() == "post":
            ziel = int(request.form['Ziel'])
            ziel_speichern(ziel)    # übermittelt Daten an jahresziel.py und speichert da Daten in Jahresziel.json
            return render_template("landing_page.html")
        return render_template("Jahresziel.html", keinfile=aussagesatz)


if __name__ == "__main__":
    app.run(debug=True, port=5001)


