import sqlite3;
import re;

# validate- and input-functions for input upon registrations
def inputName():
    name = str(input('Name: '))
    if (name == 'quit'): quit();
    return name
def inputEmail():
    email = str(input('E-Mail Address: '))
    while not validateEmail(email):
        if (email == 'quit'): quit();
        print("* Email must be on the format username@domain.countryCode")
        email = str(input('E-Mail Address: '))
    return email
def validateEmail(input: str):
    pattern = re.compile("[a-zA-Z0-9]{1,}@[a-zA-Z]{1,}[.]{1,1}[a-zA-Z]{2,3}")
    if not pattern.match(input): return False
    return True
def inputPhoneNo():
    phoneNo = str(input('Phone Number: '))
    while not phoneNo.isdigit() or not len(phoneNo) == 8:
        if (phoneNo == 'quit'): quit();
        print("* Phone Number must consist of 8 numbers")
        phoneNo = str(input('Phone Number: '))
    return int(phoneNo)

# registers a new customer into the database
def registerCustomer(name: str, email: str, phoneNo: int):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    
    # generates a new customerID
    cursor.execute('''
        SELECT max(kundeNr) FROM Kunde;
    ''')
    customerNum = cursor.fetchone()[0]
    if customerNum == None: customerNum = 1
    else: customerNum = int(customerNum) + 1
    
    # inserts the value into trainData.db
    print(f'Registrering new user: [{customerNum}, {name}, {email}, {phoneNo}]')
    cursor.execute(f'''
        INSERT INTO Kunde VALUES ({customerNum}, "{name}", "{email}", {phoneNo});
    ''')
    con.commit()
    cursor.close()
    return customerNum

# fetches a customer based on their ID from the database. Used for login in DBMS
def getCustomer(kundeNr: int):
    con = sqlite3.connect('trainData.db')
    cursor = con.cursor()
    cursor.execute(f'''
        SELECT *
        FROM Kunde
        WHERE kundeNr = {kundeNr};
    ''')
    tuple = cursor.fetchone()
    cursor.close()
    return [tuple[0], tuple[1], tuple[2], tuple[3]]