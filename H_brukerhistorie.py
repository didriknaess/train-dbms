import sqlite3;

con = sqlite3.connect('trainData.db')
cursor = con.cursor()

def showPurchases(customerID: int):
    # checks if the customerID is valid, else will get SQL errors
    cursor.execute('''
        SELECT kundeNr, navn
        FROM Kunde;
    ''')
    customers = {row[0]: row[1] for row in cursor.fetchall()}
    if customerID not in customers.keys(): return
    # fetches all seteBilletter. The NULL-columns is a placeholder for SengNr, which a seteBillett does not have. 
    cursor.execute(f'''
        SELECT Billett.billettID, ordreNr, tidspunktKjøpt, startStasjon, endeStasjon, togruteID, dato, vognID, seteNr, NULL
        FROM ((Kunde INNER JOIN KundeOrdre USING(kundeNr)) 
            INNER JOIN Billett USING(ordreNr))
			JOIN SeteBillett 
			WHERE (Billett.billettID = SeteBillett.billettID OR SeteBillett.billettID = NULL) AND kundeNr = {customerID};
    ''')
    data = cursor.fetchall()
    purchases = [tuple for tuple in data]
    # fetches all sengeBilletter. The NULL-column is a placeholder for SeteNr, which a sengeBillett does not have. 
    cursor.execute(f'''
        SELECT Billett.billettID, ordreNr, tidspunktKjøpt, startStasjon, endeStasjon, togruteID, dato, vognID, NULL, sengNr
        FROM (((Kunde INNER JOIN KundeOrdre USING(kundeNr)) 
            INNER JOIN Billett USING(ordreNr))
			INNER JOIN SengeBillett USING (billettID))
		WHERE kundeNr = {customerID};
    ''')
    data = cursor.fetchall()
    # merges the two tables to get a singular ticket-table
    for tuple in data: purchases.append(tuple)
    toPrint = ""
    # formatts the data from SQL to appear more readable in the interface
    for entry in purchases:
        toPrint += f"\nOrdreNummer: {entry[1]}, BillettNummer: {entry[0]}"
        toPrint += f"\nTidspunkt for kjøp: {entry[2]}"
        toPrint += f"\nRoute: {entry[5]} '{entry[3]}'-'{entry[4]}', Dato: {entry[6]}"
        if entry[8]:
            toPrint += f"\nVogn: {entry[7]}      -     Sete: {entry[8]}"
        else:
            toPrint += f"\nVogn: {entry[7]} -  Seng: {entry[9]}"
        toPrint += "\n" + "-" * 40
    return toPrint[1:]