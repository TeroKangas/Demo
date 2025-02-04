# Python-Projekt ToDoRPG

## Mitglieder

Klasse: E2FI1
<br>
<br>
Tero Kangas, Lucie Haas

<br>

## Inhalte des Programms:

Dieses Programm kann:

- Erstellen, bearbeiten, löschen, erledigen von ToDo’s (Quests)
   - Name
   - Bezeichnung 
   - Schwierigkeitsgrad 
   - Datum von
   - Datum bis 
   - Status: offen & geschlossen

<br>

- Erstellen, bearbeiten, löschen von Usern
   - Name  
   - Bild 
   - Rasse & Klasse

<br>

## Beschreibung des Programmes

### Beschreibung

Das Programm ist eine webbasierte Applikation, die mithilfe des Frameworks NiceGUI eine Benutzeroberfläche zur Verwaltung von "Quests" bereitstellt.
Quests sind hier Aufgaben oder Ziele mit einem Titel, einer Beschreibung, einem Schwierigkeitsgrad und Start- sowie Enddatum.
Als Datenbank wurde SQLite verwendet. Die Steuerung vom öffnen und schließen eines Tabs im Browser übernimmt Javascript.

<br>

**Die Seiten & deren Funktionen:**

*Create Quest:* Eine neue Quest erstellen
<br>
<br>
*Open Quests:* In einem Dropdown-Menü aus einer Liste, welche alle Quests des aktuellen Users darstellt auswählen und diese ändern, löschen oder auf erledigt setzen
<br>
<br>
*Closed Quests:* Eine Liste aller geschlossenen Quests des aktuellen Users
<br>
<br>
*Create User:* Einen neuen User erstellen
<br>
<br>
*Users Cockpit:* Den User wechseln

<br>

### Start des Programmes & andere Informationen

- Zum Start des Programmes bitte das Python-File "program", welches unter "demo" liegt, ausführen.

- Bitte nach jeder Aktion den aktuellen Tab reloaden.

- Nach einer Weile Inaktivität "lockt" sich die Datenbank, in diesem Fall einfach "program" beenden und erneut starten.

<br>

### Belohnungen

Die Belohnungen sind:
   - ab Level 3: 3. Profilbild zum auswählen
   - ab Level 6: 4. Profilbild zum auswählen

<br>

## Auflistung der Aufteilung der Aufgaben/Inhalte

### Branches

Tero:
   - firstbranche
   - teros_branche
   - teros_new_branche
   - workbranche
   - work_branche
   - 261124
   - 210125
   - 210125-3
   - 210125-4
   - final_b
   - last_one_tk

Lucie:
   - structure
   - levelStructure
   - quest
   - level
   - editUser
   - levelFunctions
   - fixesForMain
   - imageTable
   - morePictures
   - levelRewards
   - quickChangesForMain
   - evenMoreFixesForMain
   - lastFixesForMain

<br>

### Aufgaben

Für mehr Informationen hierzu kann man bei Nutzung von PyCharm die Autoren der jeweiligen Abschnitte rechts neben diesen anschauen.


Tero:
   - einige Funktionen der Klassen für Datenbankinteraktion
     - level.py
     - quest.py
     - user.py
   - Erstellung des "utils" Files und dessen Inhalte
   - Implementierung von nicegui
   - "program" File und dessen Inhalte

<br>
<br>

Lucie:
   - generelle Struktur
   - die sqlite Tables
   - die meisten Funktionen der Files für Datenbankinteraktion
     - level.py
     - quest.py
     - user.py
   - Initiale Erstellung und Funktion der "create_user_page" in "program"
   - kleine Fixes im "program" File
   - readMe
 


