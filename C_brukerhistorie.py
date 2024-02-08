import sqlite3;
from datetime import date;

# finner alle gyldige stasjoner og legger de til i en liste
def fetchStations():
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor();

    cursor.execute('''
        SELECT navn FROM Stasjon;
    ''');
    data = cursor.fetchall();
    cursor.close()
    stations = [];
    for entry in data:
        stations.append(entry[0]);
    return stations

# finner alle avganger fra en gitt stasjon, med input på en (gyldig) stasjon og ukedag (int: 0-6). 
def showDepartures(station: str, weekday: int):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor();
    cursor.execute(f'''
        SELECT stasjonNavn, tidspunkt, togruteID, dato
        FROM TogruteGårGjennom NATURAL JOIN (
            SELECT *
            FROM TogruteTabell CROSS JOIN RuteForekomst
            WHERE TogruteTabell.togruteID = RuteForekomst.togruteID
        ) WHERE stasjonNavn = "{station}";
    ''');
    data = cursor.fetchall();
    cursor.close()
    entries = [];
    # finds time for station with departure the given weekdan
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for tuple in data:
        dateValues = tuple[3].split("-");
        d = date(int(dateValues[0]), int(dateValues[1]), int(dateValues[2]));
        if d.weekday() == weekday:
            entries.append((tuple[0], tuple[1], tuple[2], weekdays[d.weekday()]));

    # Rewrites the return-string to a more pleasing format
    formattedData = 'stasjonNavn'.ljust(12) + 'tidspunkt'.ljust(12) + 'togruteID'.ljust(12) + 'weekday\n';
    stringData = '';
    for tuple in entries:
        stringData += str(tuple[0]).ljust(12);
        stringData += str(tuple[1]).ljust(12);
        stringData += str(tuple[2]).ljust(12);
        stringData += str(tuple[3]) + '\n';
    # returns result, if none, result placeholder 'no result'-text
    if stringData == '':
        print("No stations fit the requirements!");
    else:
        print(formattedData + stringData);