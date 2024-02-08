import sqlite3, copy
from datetime import datetime, date, time, timedelta

def validDateString(dateString: str):
    try:
        toDate(dateString)
        return True
    except:
        return False

def validDateTimeString(dateString: str):
    try:
        toDateTime(dateString)
        return True
    except:
        return False

def toDate(dateString: str):
    # format: yyyy-mm-dd
    return date(year=int(dateString[0:4]), month=int(dateString[5:7]), day=int(dateString[8:10]))

def toTime(dateString: str):
    # format: hh:mm
    return time(hour=int(dateString[0:2]), minute=int(dateString[3:5]))

def toDateTime(dateString: str):
    # format: yyyy-mm-dd hh:mm
    return datetime(year=int(dateString[0:4]), month=int(dateString[5:7]), day=int(dateString[8:10]), hour=int(dateString[11:13]), minute=int(dateString[14:]))

def mapBanestrekninger():
    con = sqlite3.connect('trainData.db');
    cursor = con.cursor();
    # finds all 'delstrekninger'
    cursor.execute('''
        SELECT endepunkt1Navn, endepunkt2Navn, retning, banestrekningID, plassering
        FROM Delstrekning;
    ''')
    data = cursor.fetchall()

    # breaks down all 'banestrekninger' into 'stasjoner' with indexes
    banestrekninger = {}
    for i in range(0, len(data)):
        tuple = data[i]
        banestrekningID = int(tuple[3]);
        if banestrekningID not in banestrekninger.keys():
            banestrekninger[banestrekningID] = {}

        cursor.execute(f'''
            SELECT count(*)
            FROM Delstrekning
            WHERE banestrekningID = {banestrekningID};
        ''')
        delstrekningCount = int(cursor.fetchone()[0])

        # default case: takes the start 'stasjon' of the 'delstrekning' and appends to the list with same index as the 
        # 'delstrekning'. If 'retning' is inverse for the 'delstrekning', you take the end station and invert the 
        # 'plassering'
        if (int(tuple[2]) == 1):
            banestrekninger[banestrekningID][tuple[0]] = [int(tuple[4])]
        else:
            banestrekninger[banestrekningID][tuple[1]] = [delstrekningCount - int(tuple[4])]
        # end case: Takes the end station and appends it as the total number of 'delstrekninger' + 1. If inverted 
        # 'retning', takes the start station of the first 'plassering' and does the same thing. 
        if int(tuple[2]) == 0 and int(tuple[4]) == 0:
            banestrekninger[banestrekningID][tuple[0]] = [delstrekningCount+1]
        elif int(tuple[2]) == 1 and int(tuple[4]) == delstrekningCount:
            banestrekninger[banestrekningID][tuple[1]] = [delstrekningCount+1]
    cursor.close()
    return banestrekninger

# find start station from banestrekningList (used to check routes passing midnight)
def routeStarts(retning, banestrekning):
    station = None
    if retning == 1:
        lowestIdx = float('inf')
        for key in banestrekning.keys():
            if len(banestrekning[key]) < 2: continue
            if banestrekning[key][0] < lowestIdx:
                lowestIdx = banestrekning[key][0]
                station = key
    else: 
        highestIdx = float('-inf')
        for key in banestrekning.keys():
            if len(banestrekning[key]) < 2: continue
            if banestrekning[key][0] > highestIdx:
                highestIdx = banestrekning[key][0]
                station = key
    return station

# finds all 'RuteForekomster' between two given 'Stasjoner' on a given date, with departures after a given time.
def findRouteOneDay(startStation: str, endStation: str, dateTime: str, dayOne: bool):
    con = sqlite3.connect('trainData.db');
    cursor = con.cursor();
    banestrekninger = mapBanestrekninger()

    cursor.execute('''
        SELECT * FROM 
        TogruteGårGjennom NATURAL JOIN TogruteTabell;
    ''')
    data = cursor.fetchall()

    cursor.execute('''
        SELECT count(*) FROM Togrute
    ''')
    togruteCount = cursor.fetchone()[0]

    # iterates over all known 'Togrute'-instances
    results = []
    for ruteID in range(1, togruteCount+1):
        cursor.execute(f'''
            SELECT banestrekningID
            FROM Togrute
            WHERE togruteID = {ruteID};
        ''')
        banestrekningID = int(cursor.fetchone()[0])
        # must deep copy list to avoid manipulation of original mapping
        banestrekning = copy.deepcopy(banestrekninger[banestrekningID])

        # appends correct arrival/departure times to the mapping of 'Banestrekninger', who now holds:
        # {banestrekningID: [plassering, tidspunkt]}
        for tuple in data:
            if not int(tuple[3]) == ruteID: continue
            banestrekning[tuple[0]].append(tuple[2])

        cursor.execute(f'''
            SELECT retning 
            FROM Togrute
            WHERE togruteID = {ruteID};
        ''')
        togruteRetning = int(cursor.fetchone()[0])

        # creates a boolean check if the start 'Stasjon' is before the end 'Stasjon' in the mapping. 
        if togruteRetning == 1:
            direction = banestrekning[startStation][0] < banestrekning[endStation][0]
        else:
            direction = banestrekning[startStation][0] > banestrekning[endStation][0]

        cursor.execute(f'''
            SELECT togruteID, dato
            FROM RuteForekomst
            WHERE togruteID = {ruteID};
        ''')
        forekomster = cursor.fetchall()
        datoer = [_[1] for _ in forekomster]
        
        # appends correct date to station, with initial date being the queried date (dateTime) from the function variables
        if dateTime[:10] in datoer:
            initial = None
            # find start time
            if togruteRetning == 1:
                lowestIdx = float('inf')
                for key in banestrekning.keys():
                    if len(banestrekning[key]) < 2: continue
                    if banestrekning[key][0] < lowestIdx:
                        lowestIdx = banestrekning[key][0]
                        initial = toTime(banestrekning[key][1])
            else: 
                highestIdx = float('-inf')
                for key in banestrekning.keys():
                    if len(banestrekning[key]) < 2: continue
                    if banestrekning[key][0] > highestIdx:
                        highestIdx = banestrekning[key][0]
                        initial = toTime(banestrekning[key][1])

            # compares station time to initial time and increments date if less
            for key in banestrekning:
                if initial == None: break
                if len(banestrekning[key]) == 1: continue
                if (initial <= toTime(banestrekning[key][1])):
                    banestrekning[key].append(toDate(dateTime[:10]))
                else: 
                    banestrekning[key].append(toDate(dateTime[:10]) + timedelta(days=1))
        # checks if start station in banestrekning has a time, else togrute will not pass through here
        start = len(banestrekning[startStation]) > 1
        if start: startTime = banestrekning[startStation][1]
        
        # checks if end station in banestrekning has a time, else togrute will not pass through here
        end = len(banestrekning[endStation]) > 1
        if end: endTime = banestrekning[endStation][1]
        
        result = []
        # if start, end and direction constraints hold: init the result for further processing
        if start and end and direction:  
            result = [ruteID, startStation, endStation, startTime, endTime]
        # convert the queried date to a python datetime.date-object
        d = toDate(dateTime[:10])
        # iterate over all RuteForekomster for this Togrute
        for forekomst in forekomster:
            if len(result) == 0 or dateTime[:10] not in datoer: break
            routeStart = routeStarts(togruteRetning, banestrekning)
            # If startStation departures the given date, check if it is after the given time. If it is, append the result
            if (toDate(forekomst[1]) == banestrekning[startStation][2]
                        and banestrekning[startStation][2] == toDate(dateTime[:10])
                        and toTime(startTime) > toTime(dateTime[11:16])):
                results.append(result + [str(banestrekning[startStation][2])])
            # Adds departures with total startdate the given date, but station departure tomorrow
            elif (banestrekning[routeStart][2] == toDate(forekomst[1]) and dayOne
                  and toDate(forekomst[1]) + timedelta(days=1) == banestrekning[startStation][2]):
                results.append(result + [str(banestrekning[startStation][2])])
    cursor.close()
    return results

# merges the results from findRouteOneDay() for today and tomorrow
def findRoute(startStation: str, endStation: str, dateTime: str):
    results1 = findRouteOneDay(startStation, endStation, dateTime, True) # removes departures before the set time
    d = toDate(dateTime[:10])
    tomorrow = d + timedelta(days=1)
    results2 = findRouteOneDay(startStation, endStation, str(tomorrow) + " 00:00", False) # adds all departures tomorrow
    return results1 + results2

# uses bubble sort to order results by departure time and date
def sortResultsByTime(results: list):
    arr = copy.deepcopy(results)
    n = len(arr)
    for i in range(len(arr)):
        swapped = False
        for j in range(n-i-1):
            # uses python datetime-class to compare departure times
            date1 = datetime.combine(toDate(arr[j][5]), toTime(arr[j][3]))
            date2 = datetime.combine(toDate(arr[j+1][5]), toTime(arr[j+1][3]))
            # swaps elements if in wrong order
            if date1 > date2:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if swapped == False: break
    return arr