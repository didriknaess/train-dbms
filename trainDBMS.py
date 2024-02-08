import sqlite3, os
from datetime import datetime
# importing of useful functions from other files in the project
from C_brukerhistorie import fetchStations, showDepartures
from D_brukerhistorie import findRoute, validDateTimeString, sortResultsByTime
from E_brukerhistorie import inputName, inputEmail, inputPhoneNo, registerCustomer
from H_brukerhistorie import showPurchases
from G_brukerhistorie import freeSeats, freeBeds, buyBedInCompartment, buySeatTicket, generateOrderID

# function which executes .sql-files
def executeSQL(filename):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    # Open and read the file as a single buffer
    fd = open(filename + ".sql", 'r')
    sqlFile = fd.read()
    fd.close()
    # isolate all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')
    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over the DROP TABLE commands
        try:
            cursor.execute(command + ";")
        except:
            print(f"Error! Command skipped:\n{command}")

# Initaliziation function to be used on corruption of database, resetting of non-scripted data, etc. 
# Not accessible from the DBSM, must be called from the python program. 
def initProject():
    try: 
        os.remove("trainData.db")
        print("Deleted old database!")
    except: 
        print("No existing database found!")
    print("\nInitializing data...")
    f = open("trainData.db", "x")
    f.close()
    executeSQL("project_init")
    executeSQL("A_brukerhistorie")
    executeSQL("B_brukerhistorie")
    executeSQL("F_brukerhistorie")

### DBMS MAIN FUNCTIONS FOR HANDLING INPUT AND DELEGATING TO 'brukerhistorie'-FILES
# text interface for brukerhistorie C
def departures():
    print("  home ->departures   route   user   tickets   purchases")
    stations = fetchStations();
    station = str(input(f'Select a station from the list below to show departures:\n{stations}\n> '))
    while station not in stations:
        if station.lower() == "back": return
        elif station.lower() == "quit": quit()
        station = str(input(f'Invalid station, please enter a valid station from the list:\n{stations}\n> '))

    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    _ = input('Enter which weekday you would like to display departures for:\n> ')
    while _.lower() not in weekdays:
        if _.lower() == "back": return
        elif _.lower() == "quit": quit()
        _ = input(f'Invalid weekday. Please enter a weekday from the following list:\n{weekdays}\n> ')
    weekday = weekdays.index(_.lower())
    showDepartures(station, weekday)

# text interface for brukerhistorie D
def route():
    print("  home   departures ->route   user   tickets   purchases")
    stations = fetchStations()
    print(f"Available stations: {stations}")
    startStation = str(input("Where do you want to travel from?\n> "))
    while startStation not in stations:
        if startStation.lower() == "quit": quit()
        elif startStation.lower() == "back" or startStation.lower() == "home": return
        startStation = str(input(f'Invalid station, please enter a valid station from the list:\n{stations}\n> '));
    endStation = str(input("Where do you want to travel to?\n> "))
    while endStation not in stations or endStation == startStation:
        if endStation.lower() == "quit": quit()
        elif endStation.lower() == "back" or endStation.lower() == "home": return
        if (endStation == startStation): endStation = str(input(f'Start and end stations cannot be the same. Please select another valid station from the list:\n{stations}\n> '));
        else: endStation = str(input(f'Invalid station, please enter a valid station from the list:\n{stations}\n> '));
    print("Date format is: 'yyyy-mm-dd hh:mm'")
    dateString = str(input("Which date and time would you like to begin your travel?\n> "))
    while not validDateTimeString(dateString):
        if dateString.lower() == "quit": quit()
        elif dateString.lower() == "back" or dateString.lower() == "home": return
        dateString = str(input("Invalid datetime! Which date would you like to begin your travel?\n> "))

    results = findRoute(startStation, endStation, dateString)
    if len(results) == 0:
        print("No available routes found!")
    else:
        print("Available train routes:")
        sorted = sortResultsByTime(results)
        for result in sorted:
            print(f"{result[0]} '{result[1]}'-'{result[2]}': {result[3]}-{result[4]} (startdate: {result[5]})")

# text interface for brukerhistorie E
def user():
    print("  home   departures   route ->user   tickets   purchases")
    global currentUserID
    # must log out before registering or logging in as a different user
    if (currentUserID != None):
        confirm = input("You must log out before registering or logging in as a new user. \nWrite 'confirm' to proceed with this. Else you will be returned to the home menu.\n> ")
        if (confirm.lower() == 'confirm'): currentUserID = None
        elif (confirm.lower() == 'quit'): quit()
        else: return
    # selection of login or registering of user
    selection = str(input('Would you like to register as a new user or log in? (reg/login):\n> '))
    # forces valid input
    while selection.lower() != "reg" and selection.lower() != "login" and selection.lower() != "back" and selection.lower() != "quit" and selection.lower() != "home":
        print("Invalid command! Please use one of the following commands:")
        print("[reg, login, back, home, quit]")
        selection = str(input('> '))
    if selection.lower() == "quit": quit()
    elif selection.lower() == "back" or selection.lower() == "home": return
    elif selection.lower() == "reg":
        print('Please fill out the following information:')
        name = inputName()
        email = inputEmail()
        phoneNo = inputPhoneNo()
        id = registerCustomer(name, email, phoneNo)
        currentUserID = int(id)
    elif selection.lower() == "login": 
        search = input('Please enter a name to search for your customer number:\n> ')
        con = sqlite3.connect('trainData.db')
        cursor = con.cursor()
        cursor.execute('''
            SELECT *
            FROM Kunde
        ''')
        customers = cursor.fetchall()
        cursor.close()
        customerIDs = [customer[0] for customer in customers]
        if len(customerIDs) == 0: return
        id = None
        while id == None:
            if search.lower() == 'quit': quit()
            elif search.lower() == 'back' or search.lower() == 'home': return
            print("Available users:")
            for customer in customers:
                if search in customer[1]: print(customer)
            id = input("> ")
            if not id.isnumeric(): pass
            elif int(id) in customerIDs: 
                break
            search = input('Please enter a name to search for your customer number:\n> ')
        currentUserID = int(id)

# text interface for brukerhistorie G
def tickets():
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    print("  home   departures   route   user   ->tickets     purchases")
    stations = fetchStations()
    print(f"Select two stations from the list below to show tickets:\n{stations}\n")
    startStation = ""
    endStation = ""
    while startStation not in stations:
        startStation = str(input("Where do you wanna travel from?\n> "))
        if startStation not in stations:
            print(f"Invalid station, please enter a valid station from the list:\n{stations}\n> ")
    while endStation not in stations:
        endStation = str(input("Where do you wanna travel to?\n> "))
        if endStation not in stations:
            print(f"Invalid station, please enter a valid station from the list:\n{stations}\n> ")
    dateString = ""
    while not validDateTimeString(dateString):
        print("Date format is: 'yyyy-mm-dd hh:mm'")
        dateString = str(input("Which date and time would you like to begin your travel?\n> "))
        if not validDateTimeString(dateString):
            print("Invalid datetime!")
    routes = findRoute(startStation, endStation, dateString)
    if len(routes) == 0:
        print("No available routes found!")
    else:
        print("Available train routes:")
        sorted = sortResultsByTime(routes)
        keys = []
        for result in sorted:
            print(f"{result[0]} '{result[1]}'-'{result[2]}': {result[3]}-{result[4]} (startdate: {result[5]})")
            keys.append((result[0], result[5]))
        key = ""
        while key not in keys: 
            key = str(input("Please select routeID and date on the format 'routeID yyyy-mm-dd'\n> "))
            tmp = key.split(" ")
            if len(tmp) == 2:
                key = (int(tmp[0]), tmp[1])
                togruteID = int(tmp[0])
                date = tmp[1] + " 00:01"
            if key not in keys:
                print("Invalid combination!")
        global currentUserID
        freeSeatsList = freeSeats(startStation, endStation, dateString).get(key, [])
        if currentUserID != None:
            freeBedsList = freeBeds(startStation, endStation, dateString, currentUserID).get(key, [])
        else:
            freeBedsList = freeBeds(startStation, endStation, dateString, None).get(key, [])
        if len(freeSeatsList) > 0:
            print("Here are the available seat:")
            print("SeatNr-VognID")
            for element in freeSeatsList:
                print(f'{element[0]}'.ljust(5)+'-'.ljust(5)+f'{element[1]}')
        if len(freeBedsList) > 0:
            print("Here are the available beds:")
            print("BedNr-VognID")
            for element in freeBedsList:
                print(f'{element[0]}'.ljust(5)+'-'.ljust(5)+f'{element[1]}')
        if currentUserID == None:
            print("If you wish to buy tickets, you must be logged in first. Manage this through the 'user'-menu\n")
            cursor.close()
            return
        answer = ""
        while answer != "y" and answer != "n":
            answer = str(input("Do you want to proceed in buying ticket? (y/n)\n> "))
            if answer == "n":
                cursor.close()
                return
            elif answer != "y":
                print("Wrong input!")
            else:
                orderID = generateOrderID()
                cursor.execute(f'''
                        INSERT INTO KundeOrdre VALUES ("{orderID}","{datetime.now()}","{currentUserID}");
                 ''')
                con.commit()
        while True:
            if len(freeBedsList) > 0 and len(freeSeatsList) > 0:
                bedOrSeat = str(input("Do you wish to buy a seat or bed? (b/s)\n> "))
            elif len(freeBedsList) > 0:
                bedOrSeat = "b"
            elif len(freeSeatsList) > 0:
                bedOrSeat = "s"
            else:
                print("No more seats or beds available")
                cursor.close()
                return
            seatNr = ""
            bedNr = ""
            vognId = ""
            if (bedOrSeat == 'b'):
                bedNr = str(input("BedNr\n> "))
                vognId = str(input("VognID\n> "))
                if (bedNr.isdigit() and vognId.isdigit()):
                    buyBedInCompartment(startStation, endStation, togruteID, date, int(bedNr), int(vognId), orderID, currentUserID)
            elif (bedOrSeat == 's'):
                seatNr = str(input("SeatNr\n> "))
                vognId = str(input("VognID\n> "))
                if seatNr.isdigit() and vognId.isdigit():
                    buySeatTicket(startStation, endStation, togruteID, date, int(seatNr), int(vognId), orderID)
            if bedOrSeat == 'quit' or bedNr == "quit" or vognId == "quit" or seatNr == "quit":
                quit()
            elif bedOrSeat in ["home", "back"] or bedNr in ["home", "back"] or vognId in ["home", "back"] or seatNr in ["home", "back"]:
                cursor.close()
                return
            elif bedOrSeat != "s" and bedOrSeat != "b":
                print("Wrong input!")
    cursor.close()
    
# text interface for brukerhistorie H
def purchases():
    print("  home   departures   route   user   tickets ->purchases")
    global currentUserID
    if currentUserID == None: 
        print("Not currently logged in! Log in or register through the 'user'-menu:")
        return
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    cursor.execute('''
        SELECT *
        FROM Kunde
    ''')
    customers = cursor.fetchall()
    cursor.close()
    name = None
    for customer in customers:
        if int(customer[0]) == currentUserID: name = customer[1]
    print(f"Showing purchases for user #{currentUserID} - {name}:")
    print("-" * 40)
    toPrint = showPurchases(customerID=currentUserID)
    print(toPrint)

# stores which user can buy tickets, and which user you show orders for
currentUserID = None
def main():
    # DBMS welcome display
    print()
    print("*" * 36)
    print("*" + " " * 34 + "*");
    print("*" + " " * 12 + "TRAIN DBMS" + " " * 12 + "*")
    print("*" + " " * 34 + "*")
    print("*" * 36)
    print("Type the name of the submenu to navigate:")
    # infinite while loop, broken by typing 'quit' at any time in the program
    while True:
        print(f"Currently logged in as user #{currentUserID}")
        
        # persistent navbar to showcase position in the DBMS
        print("->home   departures   route   user   tickets   purchases")

        print("Input action below:")
        # valid user commands; these delegate to correct 'brukerhistorie'
        nav = str(input("> "))
        if nav.lower() == "quit": quit()
        elif nav.lower() == "back" or nav.lower() == "home": continue
        elif nav.lower() == "departures": departures()
        elif nav.lower() == "route": route()
        elif nav.lower() == "user": user()
        elif nav.lower() == "tickets": tickets()
        elif nav.lower() == "purchases": purchases()
        else: print("Invalid action!")
main()