import traceback
import string
import random
import mysql.connector
import csv
import global_vars
import re

def init_db():
    """Creates the sagedorms database

    Keyword arguments:
    global_vars.cursor -- executes SQL commands
    """

    # get created databases
    global_vars.cursor.execute("SHOW DATABASES like 'sagedormsdb';")
    db_names = [i[0] for i in global_vars.cursor.fetchall()]

    # create database if not yet already
    if('sagedormsdb' not in db_names):
        global_vars.cursor.execute("CREATE DATABASE IF NOT EXISTS sagedormsdb;")
        global_vars.cursor.execute("USE sagedormsdb;")

    else:
        global_vars.cursor.execute("USE sagedormsdb;")

def executeScriptsFromFile(filename, delimiter):
    '''
    Takes in a file name and delimiter, and parses and executes the SQL commands in the file
    '''
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(delimiter)

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            command = command.rstrip()
            if (command != "" and "DELIMITER" not in command):
                global_vars.cursor.execute(command)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

def createDorms():
    '''
    Calls the stored procedure to add all the dorms
    '''
    try:
        global_vars.cursor.callproc('AddDorms', [])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def populateRooms():
    '''
    Uses the csv file that was created from the original txt file with a python script to populate the database with room info
    '''
    csv_file = open('rooms.csv')
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        isSubFree = random.getrandbits(1)
        query = f"""INSERT INTO ROOM (dormName, number, dimensionsDescription, squareFeet, isSubFree, windowsDescription, otherDescription) VALUES('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {isSubFree}, '{row[4]}', '{row[5]}')"""
        global_vars.cursor.execute(query)
    csv_file.close()

def populateDormRooms():
    '''
    Uses the csv file that was created from the original txt file with a python script to populate the database with dorm room info
    '''
    csv_file = open('dormrooms.csv')
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        numOccupants = 1
        if " 2 " in row[2]: # the closet section
            numOccupants = 2
        hasPrivateBathroom = int("Shared" in row[4] or "Private" in row[4])
        query = f"""INSERT INTO DormRoom (dormName, number, numOccupants, hasPrivateBathroom, closetsDescription, bathroomDescription) VALUES('{row[0]}', '{row[1]}', {numOccupants}, {hasPrivateBathroom}, '{row[2]}', '{row[4]}')"""
        global_vars.cursor.execute(query)
    csv_file.close()
    addConnectingRoomInfo()

def addConnectingRoomInfo():
    '''
    Uses the csv file that was created from the original txt file with a python script to populate the database with connecting room info
    '''
    csv_file = open('dormrooms.csv')
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        connectingRoomNum = None
        hasConnectingRoom = False
        if (row[1][-1] == 'A' and row[1][:-1] != "214"): # 214 is in the wrong format
            connectingRoomNum = row[1][:-1] + 'B'
            hasConnectingRoom = True
        elif (row[1][-1] == 'B'):
            connectingRoomNum = row[1][:-1] + 'A'
            hasConnectingRoom = True
        elif "two rooms (w/" in row[5]:
            connectingRoomNum = int(re.sub("[^0-9]", "", row[5]))
            hasConnectingRoom = True
        if hasConnectingRoom:
            query = f"""UPDATE DormRoom SET connectingRoomNum = '{connectingRoomNum}', numOccupants = 2 WHERE number = '{row[1]}' AND dormName = '{row[0]}'"""
            global_vars.cursor.execute(query)
    csv_file.close()

def createSuites():
    '''
    Explicit queries to create suites (hard-coded)
    '''
    def randomString(stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    suite1ID = randomString()
    suite2ID = randomString()
    suite3ID = randomString()
    suite4ID = randomString()
    suite5ID = randomString()
    suite6ID = randomString()
    suite7ID = randomString()
    suite8ID = randomString()
    suite9ID = randomString()
    suite10ID = randomString()
    suite11ID = randomString()

    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite1ID}\', TRUE, 6, 6, \'NORTON-CLARK\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite1ID}\' WHERE dormName = \'NORTON-CLARK\' AND number IN (11, 13, 14, 15, 16);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite2ID}\', TRUE, 4, 4, \'NORTON-CLARK\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite2ID}\' WHERE dormName = \'NORTON-CLARK\' AND number IN (3, 4, 5, 7);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite3ID}\', TRUE, 4, 4, \'NORTON-CLARK\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite3ID}\' WHERE dormName = \'NORTON-CLARK\' AND number IN (27, 28, 29, 30);'
    global_vars.cursor.execute(queryString)

    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite4ID}\', FALSE, 6, 6, \'SMILEY\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite4ID}\' WHERE dormName = \'SMILEY\' AND number IN (101, 102, 103, 104, 105, 107);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite5ID}\', FALSE, 6, 6, \'SMILEY\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite5ID}\' WHERE dormName = \'SMILEY\' AND number IN (201, 202, 203, 204, 205, 207);'
    global_vars.cursor.execute(queryString)

    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite6ID}\', FALSE, 6, 6, \'WALKER\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite6ID}\' WHERE dormName = \'WALKER\' AND number IN (646, 647, 650, 651, 652, 653);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite7ID}\', FALSE, 6, 6, \'WALKER\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite7ID}\' WHERE dormName = \'WALKER\' AND number IN (601, 602, 603, 604, 644, 645);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite8ID}\', FALSE, 6, 6, \'WALKER\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite8ID}\' WHERE dormName = \'WALKER\' AND number IN (638, 639, 642, 643, 654, 655);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite9ID}\', FALSE, 6, 6, \'WALKER\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite9ID}\' WHERE dormName = \'WALKER\' AND number IN (630, 631, 632, 635, 656, 657);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite10ID}\', FALSE, 3, 3, \'WALKER\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite10ID}\' WHERE dormName = \'WALKER\' AND number IN (701, 702, 703);'
    global_vars.cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite11ID}\', FALSE, 5, 5, \'WALKER\');'
    global_vars.cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite11ID}\' WHERE dormName = \'WALKER\' AND number IN (729, 730, 731, 732, 733);'
    global_vars.cursor.execute(queryString)

def addStudents():
    try:
        global_vars.cursor.callproc('AddStudents', [])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def main(info = None):
    """
    Main method populates database in the correct order of function calls
    """
    try:
        # connect to localhost mysql server
        sagedormsdb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="databases133",
                auth_plugin='mysql_native_password',
                autocommit=True)

        # global_vars.cursor executes SQL commands
        global_vars.cursor = sagedormsdb.cursor()
        global_vars.emailID = 'issa2018'
        init_db()

        executeScriptsFromFile("tables.sql", ";")
        executeScriptsFromFile("add_data_stored_procedures.sql", "$$")
        executeScriptsFromFile("room_selection_procedures.sql", "$$")
        executeScriptsFromFile("suite_selection_procedures.sql", "$$")
        executeScriptsFromFile("wish_list_procedures.sql", "$$")
        createDorms()
        populateRooms()
        populateDormRooms()
        addConnectingRoomInfo()
        createSuites()
        addStudents()

        global_vars.cursor.close()

    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
