<h1>Webapplikation "FINAZUBI"</h1>
<h2>1. Ausgangslage</h2>
Ausgaben sind schwierig zu kontrollieren und zu kategorisieren. Es gibt eine Zunahme in der Anzahl an Konten, da 
Onlinebanken und auch Tradingplattformen nicht über die (Haus)Bank abgewickelt werden. 


<h2>2. Projektidee </h2>
Der FINAZUBI (Finanzen + Azubi) hilft dir dabei, deine kompletten Ausgaben zu dokumentieren und auszuwerten. 
Dabei spielt es keine Rolle, mit welcher Bank du deine Ausgaben tätigst. Berücksichtigt dabei werden verschiedene
Kategorien, die dir zu einem späteren Zeitpunkt zeigen, wo du wieviel Geld ausgegeben hast. Das schafft Sparpotential.


<h2>3. Betrieb</h2>
Folgende Module müssen für den Betrieb implementiert werden:
Flask (Flask, render_template, request)
Plotly (plotly.express as px)
JSON
Pandas
os.path (File Exists check)

<h2>4. Workflow</h2>

!Hier kommt das Flowchart

<h2>5. Architektur</h2>
Die Architektur ist unterteilt in Startseite, Ausgaben, Finanzen & Startseite
Wenn noch keine Daten eingegeben wurden, funktioniert das Programm trotzdem
und zeigt auf verschiedenste Art und Weise an, dass Daten fehlen.

<h3>5.1 Gefilterte Ausgaben ansehen / Ausgaben </h3>
Der User wählt eine Kategorie aus. Als zweite Filteroption wählt er den Monat.
Es zeigt eine geordnete Tabelle an, wo alle Ausgaben aufgezeigt werden (gefilterte Variante).
Falls Einnahmen eingerechnet werden sollten (Zuviel Bezahlung von Rechnungen, Twintgutschriften, falsch getätigte Ausgaben), 
zeigt es diese in grüner Schrift an. Ausgaben sind mit roter Schrift gekennzeichnet.
Zudem werden alle getätigten Ausgaben aufgelistet.


<h3>5.2 Komplette Ausgaben ansehen / Finanzen </h3>
Diese Seite visualisiert alle Ausgaben. Die Ausgaben werden auf die Kategorie unterteilt
Wenn noch keine Ausgaben getätigt wurden, wird ein Hinweis geschaltet 


<h3>5.3 Jahresziel</h3>
Im Programm wird eine Jahreszahl definiert. Die ganzen Ausgaben werden aufgerechnet und angezeigt. 
Weiter zeigt es an, wieviel noch ausgegeben werden darf, bis das Jahresziel erreicht wurde.
Grüne Anzeige =  > 2/3 vom Jahresziel
Orange Anzeige = 1/3 vom Jahresziel bis 2/3 zum Jahresziel
Rote Anzeige = <1/3 vom Jahresziel
Das die Anzeigefarben dynamisch sind, wurden sie nicht in fixe Zahlen, sondern in Relation zum Jahresziel gesetzt.
Wenn noch kein Jahresziel definiert wurde, wird dies in einer Hinweisbox signalisiert


<h2>6. Funktionen</h2>
Dateneingabe: Ausgaben hinzufügen / Kategorie hinzufügen / Datum hinzufügen
Datenspeicherung: Ausgaben aus Dateneingabe werden in einer JSON-Datei gespeichert.
Datenverarbeitung: Die Daten werden zusammengerechnet und gefiltert in Ausgaben.html, Kategorie und Jahresziel (Mit Jinja und Python)
Datenlöschung: Das letzte Element kann mittels eines Formularbuttons gelöscht werden
Datenausgabe: Nach Filterwunsch werden Daten ausgegeben
    Ausgabe nach Monat und Kategorie (Ausgabe)
    Ausgabe nach Genre (Finanzen)
    Ausgabe nach Jahresziel berechnet (Jahresziel)