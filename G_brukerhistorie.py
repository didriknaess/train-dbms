from operator import le
import sqlite3;

from D_brukerhistorie import findRoute, mapBanestrekninger

def trainPassingThrough(startStasjon, endeStasjon, dato):
    # Returns a list of stations a train passes through a given date from start to end
    # Format on date: 'yyyy-mm-dd hh:mm'
    stasjoner = []
    if (len(findRoute(startStasjon, endeStasjon, dato)) > 0):
        for element in mapBanestrekninger().values():
            for key in element.keys():
                if key not in stasjoner:
                    stasjoner.append(key)
        startIndex = stasjoner.index(startStasjon)
        sluttIndex = stasjoner.index(endeStasjon)
        # Finds the indexes of the relevant stations and slices the whole list based on the result
        if sluttIndex > startIndex:
            if sluttIndex + 1 == len(stasjoner):
                return stasjoner[startIndex:]
            else: 
                return stasjoner[startIndex:sluttIndex + 1]  
    else: return None

def freeSeats(startStasjon, endeStasjon, dato):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    # Format on date: 'yyyy-mm-dd hh:mm'
    routes = findRoute(startStasjon, endeStasjon, dato)
    routesAndSeats = {}
    for route in routes:
        togruteID = route[0]
        date = route[5]
        freeSeatsList = []
        cursor.execute(f'''
                        SELECT T.togruteID, S.seteNr, S.vognID, B.startStasjon, B.endeStasjon, R.dato AS avreisedato
                        FROM ((((((Sete AS S NATURAL JOIN Sittevogn)
                        NATURAL JOIN SattSammenAvSittevogn)
                        NATURAL JOIN Vognoppsett)
                        NATURAL JOIN RuteOppsett)
                        NATURAL JOIN Togrute AS T)
                        NATURAL JOIN RuteForekomst AS R)
                        LEFT OUTER JOIN (Billett AS B NATURAL JOIN SeteBillett) USING (dato, togruteID, seteNr, vognID)
                        WHERE R.dato = "{date}" AND T.togruteID = "{togruteID}"                
                        ''')
        seatsAndTickets = cursor.fetchall()
        # Return a list of all seats and connected tickets (if they have any) on that specific date and route
        takenOnStations = {}
        for tuple in seatsAndTickets:
            seat = tuple[1:3]
            if (tuple[4] == None):
                freeSeatsList.append(seat)
                # If a seat has no tickets connected to it during a train route instance, the seat i obviously free
            else:
                cursor.execute(f'''
                SELECT retning 
                FROM Togrute
                WHERE togruteID = {togruteID};
                ''')
                togruteRetning = int(cursor.fetchone()[0])
                if seat not in takenOnStations.keys():
                    takenOnStations[seat] = [trainPassingThrough(tuple[3], tuple[4], dato)]
                else:
                    takenOnStations[seat].append(trainPassingThrough(tuple[3], tuple[4], dato))
        for key in takenOnStations.keys():
            ikkeStart = []
            ikkeStop = []
            bruktRute = []
            # These are used to see which stations a new customer can start or end at a station. The "bruktRute" is to ensure that tou can't buy 
            # a ticket that goes over another instance.
            for strekning in takenOnStations[key]:
                if togruteRetning == 1:
                    ikkeStart += strekning[:len(strekning)-1]
                    ikkeStop += strekning[1:]
                else:
                    ikkeStart += strekning[1:]
                    ikkeStop += strekning[:len(strekning)-1]
                bruktRute += strekning
            planlagtRute = trainPassingThrough(startStasjon, endeStasjon, dato)
            if startStasjon not in ikkeStart and endeStasjon not in ikkeStop and not set(bruktRute).issubset(planlagtRute):
                # Here we find and append all free seats
                freeSeatsList.append(key)
        if len(freeSeatsList) > 0:
            routesAndSeats[(togruteID, date)] = freeSeatsList
            # We only care about routes that have free seats
    cursor.close()
    return routesAndSeats

def freeBeds(startStasjon, endeStasjon, dato, kundeNr):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    # format på dato: 'yyyy-mm-dd hh:mm'
    routes = findRoute(startStasjon, endeStasjon, dato)
    routesAndBeds = {}
    for route in routes:
        togruteID = route[0]
        date = route[5]
        freeBedsList = []
        compartments = []
        cursor.execute(f'''
                        SELECT T.togruteID, S.sengNr, S.vognID, B.startStasjon, B.endeStasjon, R.dato, KO.kundeNr
                        FROM ((((((Soveplass AS S NATURAL JOIN Sovevogn)
                        INNER JOIN SattSammenAvSovevogn USING(vognID))
                        INNER JOIN Vognoppsett USING(vognoppsettID))
                        INNER JOIN RuteOppsett USING(vognoppsettID))
                        INNER JOIN Togrute AS T USING(togruteID))
                        INNER JOIN RuteForekomst AS R USING(togruteID))
                        LEFT OUTER JOIN (Billett AS B NATURAL JOIN SengeBillett) USING (dato, togruteID, sengNr, vognID)
						LEFT OUTER JOIN KundeOrdre AS KO USING(ordreNr)
                        WHERE R.dato = "{date}" AND T.togruteID = "{togruteID}"                
                        ''')      
        beds = cursor.fetchall()
        # Finds all beds and connected tickets (if they have)
        for i in range(int(len(beds)/2)):
            compartments.append((beds[2*i], beds[2*i+1]))
            # Connects pairs of beds that belong to the same compartment
        for tuple in compartments:
            if (tuple[0][4] == None and tuple[1][4] == None):
                freeBedsList.append(tuple[0][1:3])
                freeBedsList.append(tuple[1][1:3])
                # If both beds have no tickets connected to them, they are both available
            elif kundeNr != None:
                if (tuple[0][4] == None and tuple[1][4] != None and tuple[1][6] == kundeNr):
                    freeBedsList.append(tuple[0][1:3])
                    # A bed is only available in this situation if you are the owner of the other bed
                elif (tuple[0][4] != None and tuple[1][4] == None and tuple[0][6] == kundeNr):
                    freeBedsList.append(tuple[1][1:3])
        if len(freeBedsList) > 0:
            routesAndBeds[(togruteID, date)] = freeBedsList
            # We only care about routes that have free beds
    cursor.close()
    return routesAndBeds

def buySeatTicket(startStasjon, endeStasjon, togruteID, dato, seteNr, vognID, ordreNr):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    if (seteNr, vognID) in freeSeats(startStasjon, endeStasjon, dato).get((togruteID, dato.split(" ")[0]), []):
        # Checks that the inputed seat is available
        billettID = generateTicketID()
        cursor.execute(f'''
                        INSERT INTO Billett VALUES ("{billettID}","{startStasjon}","{endeStasjon}","{ordreNr}","{togruteID}","{dato.split(" ")[0]}");
        ''')
        cursor.execute(f'''
                        INSERT INTO SeteBillett VALUES ("{billettID}","{vognID}","{seteNr}");
        ''')
        con.commit()
        print("Seat bought successfully!")
    else:
        print("The seat is taken or does not exist")
    cursor.close()

def buyBedInCompartment(startStasjon, endeStasjon, togruteID, dato, sengNr, vognID, ordreNr, kundeNr):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    if (sengNr,vognID) in freeBeds(startStasjon, endeStasjon, dato, kundeNr).get((togruteID, dato.split(" ")[0]), []):
        # Checks that the inputed seat is available
        billettID = generateTicketID()
        cursor.execute(f'''
                            INSERT INTO Billett VALUES ({billettID},"{startStasjon}","{endeStasjon}",{ordreNr},{togruteID},"{dato.split(" ")[0]}");
            ''')
        cursor.execute(f'''
                            INSERT INTO SengeBillett VALUES ({billettID},{vognID},{sengNr});
            ''')
        con.commit()
        print("Bed bought successfully!")
    else:
        print("The bed is taken or does not exist")  
    cursor.close()

def generateTicketID():
    # Code that makes sure that each ticketID is unique
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    cursor.execute(f'''
                        SELECT max(billettID)
                        FROM Billett        
                        ''')
    billettID = cursor.fetchone()[0]
    cursor.close()
    if billettID == None:
        return 1
    return int(billettID) + 1

def generateOrderID():
    # Code that makes sure that each orderID is unique 
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    cursor.execute(f'''
                        SELECT max(ordreNr)
                        FROM KundeOrdre        
                        ''')
    ordreNr = cursor.fetchone()[0]
    cursor.close()
    if ordreNr == None:
        return 1
    return int(ordreNr) + 1