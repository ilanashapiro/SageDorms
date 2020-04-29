import traceback
import mysql.connector
import sys
import names
import random
import app
import csv
import re
from datetime import datetime
from mysql.connector import Error
from random import getrandbits

def init_db(cursor):
    """Creates the sagedorms database

    Keyword arguments:
    cursor -- executes SQL commands
    """

    # get created databases
    cursor.execute("SHOW DATABASES like 'sagedormsdb';")
    db_names = [i[0] for i in cursor.fetchall()]

    # create database if not yet already
    if('sagedormsdb' not in db_names):
        cursor.execute("CREATE DATABASE IF NOT EXISTS sagedormsdb;")

    cursor.execute("USE sagedormsdb;")
    executeScriptsFromFile("tables.sql", cursor)

def generate_fake_students(sagedormsdb, cursor):
    """ Generates many fake students for 'room draw'

    Keyword arguments:
    cursor -- executes SQL commands
    """

    for i in range(100):
        sid = 10000000 + i
        name = names.get_full_name()
        year = 2020 + (i%10)
        drawNum = random.randrange(1,101)
        drawTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drawGroup = str(random.randrange(1, 10))
        isDrawing = 1

        cursor.execute(f'''INSERT INTO Student VALUES(
                {sid}, '{name}', {year}, {drawNum}, '{drawTime}',
                '{drawGroup}', {isDrawing}, dormRoomNum, dormName,
                1, avgSuiteGroupDrawNum , '{drawTime}')''')
        sagedormsdb.commit()

def executeScriptsFromFile(filename, cursor):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            if (command.rstrip() != ""):
                cursor.execute(command + ";")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

def selectDormRooms(cursor, info):
    queryString = '''SELECT *
        FROM DormRoom AS dr, Room AS r
        WHERE r.isReservedForSponsorGroup = FALSE'''
    for key, value in info.items():
        if info[value] is not None: # or "" or whatever means empty input
            if (key == "dormNum" or
                key == "dormName" or
                key == "numOccupants" or
                key == "hasPrivateBathroom" or
                key == "numDoors" or
                key == "closetsDescription" or
                key == "bathroomDescription" or
                key == "hasConnectingRoom"):
                    if (key == "hasConnectingRoom"):
                        queryString += f' AND dr.connectingRoomNum IS NOT NULL'
                    else:
                        queryString += f' AND dr.{info[key]} = {info[value]}'
                        if key == "dormName" or key == "dormNum":
                            queryString += f' AND dr.{info[key]} = r.{info[key]}'
            else: # or "" or whatever means empty input
                queryString += f' AND r.{info[key]} = {info[value]}'
    queryString += ';'

    cursor.execute(queryString)
    cursor.fetchall()

# https://pynative.com/python-mysql-execute-stored-procedure/
def setStudentRoom(cursor, info):
    try:
        cursor.callproc('SetStudentRoom', [app.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addToWishList(cursor, info):
    try:
        cursor.callproc('AddToWishlist', [app.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def deleteFromWishList(cursor, info):
    try:
        cursor.callproc('DeleteFromWishList', [app.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def createSuiteGroup(cursor, info):
    try:
        # query the students in the prospective suite group to calculate average draw num. (note: the emailIDs entered is everyone ELSE in the list,
        # not including the student doing the entering -- that person is app.emailID
        getAvgDrawNumQueryString = f'SELECT avg(s.drawNum) FROM Student AS s WHERE s.emailID = {app.emailID}'
        for key, value in info.items():
            if info[value] is not None: # or "" or whatever means empty input
                emailID = info[value]
                queryString += f' OR s.emailID = {emailID}'
                emailIDsToAdd.append(emailID)
        getAvgDrawNumQueryString += ';'
        cursor.execute(getAvgDrawNumQueryString)
        avgDrawNum = cursor.fetchone()[0] # there's only one (single-value) result tuple that contains the average

        # now that we have the avg draw num, add all students to the SuiteGroup table with this avg draw num
        # the avg draw times will be calculated later, just before the draw, after all groups have been created (so it's null for now)
        # The student doing the entering becomes the suite representative
        # If a student is already in a different prospective suite group, that data will be overwritten and they will be part of the new group
        # If a group wants to add another student, they'll need to fill out the form again to register the group for everyone
        addStudentsQueryString = f'''REPLACE INTO SuiteGroup (emailID, avgDrawNum, avgDrawTime, isSuiteRepresentative, suiteID) VALUES
                                     ({app.emailID}, {avgDrawNum}, NULL, TRUE, NULL)'''
        for emailID in emailIDsToAdd:
            addStudentsQueryString += f', ({emailID}, {avgDrawNum}, NULL, FALSE, NULL)'
        # addStudentsQueryString += ' ON DUPLICATE KEY UPDATE avgDrawNum = VALUES(avgDrawNum), isSuiteRepresentative = VALUES(isSuiteRepresentative)'THIS LINE UPDATES EXISTING DATA
        # RATHER THAN REPLACING, COULD USE THIS IF WE WANT TO UPDATE RATHER THAN REPLACE

        addStudentsQueryString += ';'
        cursor.execute(addStudentsQueryString)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def populateRooms(cursor):
    csv_file = open('rooms.csv')
    csv_data = csv.reader(csv_file)
    for row in csv_data:
        isSubFree = random.getrandbits(1)
        # print(row)
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
            query = f"""UPDATE DormRoom SET connectingRoomNum = '{connectingRoomNum}' WHERE number = '{row[1]}' AND dormName = '{row[0]}'"""
            print(query)
            cursor.execute(query)
    csv_file.close()

def main(info = None):
    """ Main method runs hello world app

        TODO:
            - invalid entry
            - SQL injection???
            - from what database will we get student information
    """
    try:
        # connect to localhost mysql server
        sagedormsdb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="databases133",
                auth_plugin='mysql_native_password',
                autocommit=True)

        # cursor executes SQL commands
        cursor = sagedormsdb.cursor()
        init_db(cursor)
        addToWishList(cursor, {'dormName': 'CLARK-I', 'dormRoomNum': '100A'})
        # generate_fake_students(sagedormsdb, cursor)
        cursor.close()

    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
