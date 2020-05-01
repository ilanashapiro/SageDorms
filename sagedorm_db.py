import traceback
import mysql.connector
import sys
import names
import random
import app
import csv
import re
import global_vars
import populate_database
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

def searchForDormRooms(cursor, info):
    queryString = '''SELECT r.dormName, r.number FROM DormRoom AS dr, Room AS r WHERE r.isReservedForSponsorGroup = FALSE'''
    for key, value in info.items():
        if value is not None: # or "" or whatever means empty input
            # case this is dormRoom info
            if (key == "dormName" or
                key == "number" or
                key == "numOccupants" or
                key == "hasPrivateBathroom" or
                key == "hasConnectingRoom"):
                    if (key == "hasConnectingRoom"):
                        queryString += f' AND dr.connectingRoomNum IS NOT NULL'
                    else:
                        # data is string value, enclose in quote
                        if key == "number" or key == "dormName" or key == "closetsDescription" or key == "bathroomDescription":
                            queryString += f' AND dr.{key} = \'{value}\''
                        # data is not a string value, no quotes
                        else:
                            queryString += f' AND dr.{key} = {value}'
                        # perform the join with room
                        if key == "dormName" or key == "number":
                            queryString += f' AND dr.{key} = r.{key}'
            else: # this is room, rather than dormRoom, information
                queryString += f' AND r.{key} = {value}'
    queryString += ';'

    print(queryString)
    cursor.execute(queryString)
    print(cursor.fetchall())

def searchForSuites(cursor, info):
    queryString = '''SELECT r.dormName, r.number FROM DormRoom AS dr, Room AS r WHERE r.isReservedForSponsorGroup = FALSE'''
    for key, value in info.items():
        if value is not None: # or "" or whatever means empty input
            # case this is dormRoom info
            if (key == "dormName" or
                key == "number" or
                key == "numOccupants" or
                key == "hasPrivateBathroom" or
                key == "hasConnectingRoom"):
                    if (key == "hasConnectingRoom"):
                        queryString += f' AND dr.connectingRoomNum IS NOT NULL'
                    else:
                        # data is string value, enclose in quote
                        if key == "number" or key == "dormName" or key == "closetsDescription" or key == "bathroomDescription":
                            queryString += f' AND dr.{key} = \'{value}\''
                        # data is not a string value, no quotes
                        else:
                            queryString += f' AND dr.{key} = {value}'
                        # perform the join with room
                        if key == "dormName" or key == "number":
                            queryString += f' AND dr.{key} = r.{key}'
            else: # this is room, rather than dormRoom, information
                queryString += f' AND r.{key} = {value}'
    queryString += ';'

    print(queryString)
    cursor.execute(queryString)
    print(cursor.fetchall())


# https://pynative.com/python-mysql-execute-stored-procedure/
def setStudentRoom(cursor, info):
    try:
        cursor.callproc('SetStudentRoom', [global_vars.emailID, info["roommateEID"], info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getDormRoomsSinglesSummary(cursor):
    try:
        cursor.callproc('GetDormRoomsSinglesSummary', [])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getDormRoomsAndSuiteSummaryForDorm(cursor, info):
    try:
        cursor.callproc('GetDormRoomsAndSuiteSummaryForDorm', [info['dormName']])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getRoomDetails(cursor, info):
    try:
        cursor.callproc('GetRoomDetails', [info["dormName"], info["dormRoomNum"]])
        results = []
        for result in cursor.stored_results():
            data = result.fetchall()
            if (len(data) > 0): # if it's a common room, dorm room info will be empty, and vice versa
                results.append(data)
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMyRoomDetails(cursor):
    try:
        cursor.callproc('GetMyRoomDetails', [global_vars.emailID])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMyWishList(cursor):
    try:
        cursor.callproc('GetMyWishList', [global_vars.emailID])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addToWishList(cursor, info):
    try:
        cursor.callproc('AddToWishlist', [global_vars.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def deleteFromWishList(cursor, info):
    try:
        cursor.callproc('DeleteFromWishList', [global_vars.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def createSuiteGroup(cursor, info):
    try:
        # query the students in the prospective suite group to calculate average draw num. (note: the emailIDs entered is everyone ELSE in the list,
        # not including the student doing the entering -- that person is global_vars.emailID
        getAvgDrawNumQueryString = f'SELECT avg(s.drawNum) FROM Student AS s WHERE s.emailID = \'{global_vars.emailID}\''
        for key, value in info.items():
            if info[value] is not None: # or "" or whatever means empty input
                emailID = info[value]
                queryString += f' OR s.emailID = \'{emailID}\''
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
                                     (\'{global_vars.emailID}\', {avgDrawNum}, NULL, TRUE, NULL)'''
        for emailID in emailIDsToAdd:
            addStudentsQueryString += f', (\'{emailID}\', {avgDrawNum}, NULL, FALSE, NULL)'
        # addStudentsQueryString += ' ON DUPLICATE KEY UPDATE avgDrawNum = VALUES(avgDrawNum), isSuiteRepresentative = VALUES(isSuiteRepresentative)'THIS LINE UPDATES EXISTING DATA
        # RATHER THAN REPLACING, COULD USE THIS IF WE WANT TO UPDATE RATHER THAN REPLACE

        addStudentsQueryString += ';'
        cursor.execute(addStudentsQueryString)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))



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
        global_vars.emailID = 'issa2018'
        info = {'dormName': 'CLARK-I', 'number': '100A', 'roommateEID' : None}
        # info['CLARK-I', '100A']
        # getDormRoomsAndSuiteSummaryForDorm(cursor, info)
        populate_database.createSuites(cursor)
        # print(global_vars.emailID, info["dormName"], info["dormRoomNum"])
        # generate_fake_students(sagedormsdb, cursor)
        cursor.close()

    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
