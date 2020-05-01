import string
import random
import mysql.connector
import csv
import re

def createDorms(cursor):
    try:
        cursor.callproc('AddDorms', [])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addStudents(cursor):
    try:
        cursor.callproc('AddStudents', [])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def populateRooms(cursor):
    csv_file = open('rooms.csv')
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        isSubFree = random.getrandbits(1)
        query = f"""REPLACE INTO ROOM (dormName, number, dimensionsDescription, squareFeet, isSubFree, windowsDescription, otherDescription) VALUES('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {isSubFree}, '{row[4]}', '{row[5]}')"""
        print(query)
        cursor.execute(query)
    csv_file.close()

def populateDormRooms(cursor):
    csv_file = open('dormrooms.csv')
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        numOccupants = 1
        if " 2 " in row[2]: # the closet section
            numOccupants = 2
        hasPrivateBathroom = int("Shared" in row[4] or "Private" in row[4])
        query = f"""INSERT INTO DormRoom (dormName, number, numOccupants, hasPrivateBathroom, closetsDescription, bathroomDescription) VALUES('{row[0]}', '{row[1]}', {numOccupants}, {hasPrivateBathroom}, '{row[2]}', '{row[4]}')"""
        print(query)
        cursor.execute(query)
    csv_file.close()
    addConnectingRoomInfo(cursor)

def addConnectingRoomInfo(cursor):
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
            cursor.execute(query)
    csv_file.close()

def createSuites(cursor):
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
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite1ID}\' WHERE dormName = \'NORTON-CLARK\' AND number IN (11, 13, 14, 15, 16);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite2ID}\', TRUE, 4, 4, \'NORTON-CLARK\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite2ID}\' WHERE dormName = \'NORTON-CLARK\' AND number IN (3, 4, 5, 7);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite3ID}\', TRUE, 4, 4, \'NORTON-CLARK\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite3ID}\' WHERE dormName = \'NORTON-CLARK\' AND number IN (27, 28, 29, 30);'
    cursor.execute(queryString)

    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite4ID}\', FALSE, 6, 6, \'SMILEY\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite4ID}\' WHERE dormName = \'SMILEY\' AND number IN (101, 102, 103, 104, 105, 107);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite5ID}\', FALSE, 6, 6, \'SMILEY\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite5ID}\' WHERE dormName = \'SMILEY\' AND number IN (201, 202, 203, 204, 205, 207);'
    cursor.execute(queryString)

    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite6ID}\', FALSE, 6, 6, \'WALKER\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite6ID}\' WHERE dormName = \'WALKER\' AND number IN (646, 647, 650, 651, 652, 653);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite7ID}\', FALSE, 6, 6, \'WALKER\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite7ID}\' WHERE dormName = \'WALKER\' AND number IN (601, 602, 603, 604, 644, 645);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite8ID}\', FALSE, 6, 6, \'WALKER\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite8ID}\' WHERE dormName = \'WALKER\' AND number IN (638, 639, 642, 643, 654, 655);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite9ID}\', FALSE, 6, 6, \'WALKER\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite9ID}\' WHERE dormName = \'WALKER\' AND number IN (630, 631, 632, 635, 656, 657);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite10ID}\', FALSE, 3, 3, \'WALKER\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite10ID}\' WHERE dormName = \'WALKER\' AND number IN (701, 702, 703);'
    cursor.execute(queryString)
    queryString = f'INSERT INTO SUITE (suiteID, isSubFree, numRooms, numPeople, dormName) VALUES (\'{suite11ID}\', FALSE, 5, 5, \'WALKER\');'
    cursor.execute(queryString)
    queryString = f'UPDATE Room SET suite = \'{suite11ID}\' WHERE dormName = \'WALKER\' AND number IN (729, 730, 731, 732, 733);'
    cursor.execute(queryString)
