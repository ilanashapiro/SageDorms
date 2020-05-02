import string
import random
import mysql.connector
import global_vars
from mysql.connector import Error

# NOTE: the keys in the info dict are preliminary

def searchForSuites(cursor, info):
    queryString = '''SELECT s.suiteID FROM Suite AS s WHERE'''
    isFirstCond = True
    for key, value in info.items():
        if value is not None: # or "" or whatever means empty input
            if (isFirstCond):
                queryString += f' r.{key} = {value}'
                isFirstCond = False
            else:
                queryString += f' r.{key} = {value}'

    queryString += ';'

    print(queryString)
    cursor.execute(queryString)
    print(cursor.fetchall())

def getDormRoomsAndSuiteSummaryForDorm(cursor, info):
    try:
        cursor.callproc('GetDormRoomsAndSuiteSummaryForDorm', [info['dormName']])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMySuiteRooms(cursor, info):
    try:
        cursor.callproc('GetMySuiteRooms', [info['emailID']])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getAllSuitesSummary(cursor):
    try:
        cursor.callproc('GetAllSuitesSummary', [])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getDormRoomAndSuiteSummaryForSuite(cursor, info):
    try:
        cursor.callproc('GetDormRoomsAndSuiteSummaryForSuite', [info['suiteID']])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getDormRoomAndSuiteSummaryForDorm(cursor):
    try:
        cursor.callproc('GetDormRoomsAndSuiteSummaryForDorm', [info['dormName']])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def removeMyselfFromSuiteGroup(cursor, info):
    try:
        cursor.callproc('RemoveMyselfFromSuiteGroup', [global_vars.emailID, info['newSuiteRepID']])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addMyselfToSuiteGroup(cursor, info):
    try:
        cursor.callproc('AddMyselfToSuiteGroup', [global_vars.emailID, info['emailIDInSG'], info['isNewSuiteRep']])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMySuiteGroup(cursor):
    try:
        cursor.callproc('GetMySuiteGroup', [global_vars.emailID])
        results = []
        for result in cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def setSuite(cursor, info):
    try:
        cursor.callproc('setSuite', [info['suiteID'], info['emailIDSuiteRep']])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def createSuiteGroup(cursor, info):
    try:
        # query the students in the prospective suite group to calculate average draw num. (note: the emailIDs entered is everyone ELSE in the list,
        # not including the student doing the entering -- that person is global_vars.emailID
        getAvgDrawNumQueryString = f'SELECT avg(s.drawNum) FROM Student AS s WHERE s.emailID = \'{global_vars.emailID}\''
        emailIDsToAdd = []
        for key, value in info.items():
            if value is not None: # or "" or whatever means empty input
                emailID = value
                getAvgDrawNumQueryString += f' OR s.emailID = \'{emailID}\''
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

        # add the students to the suite group
        for emailID in emailIDsToAdd:
            #the suite representative is automatically the person creating the suite for their group
            if emailID == global_vars.emailID:
                addStudentsQueryString += f', (\'{emailID}\', {avgDrawNum}, NULL, TRUE, NULL)'
            else:
                addStudentsQueryString += f', (\'{emailID}\', {avgDrawNum}, NULL, FALSE, NULL)'

        addStudentsQueryString += ';'
        cursor.execute(addStudentsQueryString)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
