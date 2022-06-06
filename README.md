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

<h2>4. Workflow</h2>

!Hier kommt das Flowchart

<h2>5. Architektur</h2>

<h3>5.1 Gefilterte Ausgaben ansehen / Ausgaben </h3>
Der User wählt eine Kategorie aus. Als zweite Filteroption wählt er den Monat.
Es zeigt eine geordnete Tabelle an, wo alle Ausgaben aufgezeigt werden (gefilterte Variante).
Falls Einnahmen eingerechnet werden sollten (Zuviel Bezahlung von Rechnungen, Twintgutschriften, falsch getätigte Ausgaben), 
zeigt es diese  in grüner Schrift an. Ausgaben sind mit roter Schrift gekennzeichnet.

<h3>5.2 Komplette Ausgaben ansehen / Finanzen </h3>
Diese Seite visualisiert alle Ausgaben. Die Ausgaben werden auf die Kategorie unterteilt


Der Anwender kann danach den Datensatz abspeichern, oder weiteren Lernstoff erfassen.

<h3>5.3 Jahresziel</h3>
Im Programm wird eine Jahreszahl definiert. Die ganzen Ausgaben werden aufgerechnet und angezeigt. 
Weiter zeigt es an, wieviel noch ausgegeben werden darf, bis das Jahresziel erreicht wurde.
Grüne Anzeige =  > 2/3 vom Jahresziel
Orange Anzeige = 1/3 vom Jahresziel bis 2/3 zum Jahresziel
Rote Anzeige = <1/3 vom Jahresziel
Das die Anzeigefarben dynamisch sind, wurden sie nicht in fixe Zahlen, sondern in Relation zum Jahresziel gesetzt.


<h2>6. Funktionen</h2>
Dateneingabe: Ausgaben hinzufügen / Kategorie hinzufügen / Datum hinzufügen
Datenspeicherung: Ausgaben aus Dateneingabe werden in einer JSON-Datei gespeichert.
Datenverarbeitung: Die Daten werden zusammengerechnet und gefiltert in Ausgaben.html, Kategorie und Jahresziel (Mit Jinja und Python)
Datenausgabe: Nach Filterwunsch werden Daten ausgegeben
Ausgabe nach Monat und Kategorie (Ausgabe)
Ausgabe nach Genre (Finanzen)
Ausgabe nach Jahresziel berechnet (Jahresziel)