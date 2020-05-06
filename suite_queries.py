import string
import random
import mysql.connector
import global_vars
import sagedorm_db
from mysql.connector import Error

def getSuiteSummaryForSuite(suiteID):
    try:
        global_vars.cursor.callproc('GetSuiteSummaryForSuite', [suiteID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def searchForSuites(info):
    queryString = '''SELECT s.suiteID, s.numPeople, s.isSubFree, s.dormName FROM Suite AS s'''
    isFirstCond = True
    for key, value in info.items():
        if value != '': # or "" or whatever means empty input
            if isFirstCond:
                if key == 'isSubFree':
                    queryString += f' WHERE s.{key} = {value}'
                else:
                    queryString += f' WHERE s.{key} = \'{value}\''
                isFirstCond = False
            else: # We don't want the searchtype key, which just told us if the form submitted was for rooms or suites
                if key == 'isSubFree':
                    queryString += f' AND s.{key} = {value}'
                else:
                    queryString += f' AND s.{key} = \'{value}\''

    queryString += ';'

    # print(queryString)
    global_vars.cursor.execute(queryString)

    suites = global_vars.cursor.fetchall()
    results = []
    for suite in suites:
        suiteID = suite[0] # suites is a list tuples, e.g. [('hjeshkgd',...), ('kadzvtir',...)], with suiteID as the first elem of each tuple
        results.append(getSuiteSummaryForSuite(suiteID))


    # print(results)
    return results

def getSuiteSummaryForDorm(info):
    try:
        global_vars.cursor.callproc('GetSuitesForDorm', [info['dormName']])
        suites = []
        for resultSuite in global_vars.cursor.stored_results():
            suites.append(resultSuite.fetchall())
        results = []
        for suite in suites[0]:
            suiteID = suite[0] # suites is a list tuples, e.g. [('hjeshkgd',...), ('kadzvtir',...)], with suiteID as the first elem of each tuple
            results.append(getSuiteSummaryForSuite(suiteID))


        # print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMySuiteDetails():
    try:
        global_vars.cursor.callproc('GetMySuiteDetails', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        print("RESULTS", results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getAllSuitesSummary():
    try:
        global_vars.cursor.callproc('GetAllSuitesSummary', [])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        # print("RESULTS", results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def removeMyselfFromSuiteGroup():
    try:
        global_vars.cursor.callproc('RemoveMyselfFromSuiteGroup', [global_vars.emailID])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addMyselfToSuiteGroup(info):
    try:
        global_vars.cursor.callproc('AddMyselfToSuiteGroup', [global_vars.emailID, info['emailIDInSG'], False])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMySuiteGroup():
    try:
        global_vars.cursor.callproc('GetMySuiteGroup', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def setSuite(info):
    try:
        global_vars.cursor.callproc('SetSuite', [info['suiteID'], info['emailIDSuiteRep']])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def isCurrentUserSuiteRepresentative():
    try:
        queryString = f'SELECT * FROM SuiteGroup AS sg WHERE sg.isSuiteRepresentative = TRUE AND sg.emailID = \'{global_vars.emailID}\';'
        global_vars.cursor.execute(queryString)
        info = global_vars.cursor.fetchall()
        if len(info) == 1:
            return True
        return False
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getNumPeopleInSuite(info):
    try:
        suiteID = info['suiteID']
        queryString = f'SELECT s.numPeople FROM Suite AS s WHERE s.suiteID = \'{suiteID}\';'
        global_vars.cursor.execute(queryString)
        info = global_vars.cursor.fetchall()
        return info[0][0]
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def setSuiteRepresentative(info):
    try:
        global_vars.cursor.callproc('SetSuiteRepresentative', [info['emailID']])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def createSuiteGroup(info):
    try:
        # query the students in the prospective suite group to calculate average draw num. (note: the emailIDs entered is everyone ELSE in the list,
        # not including the student doing the entering -- that person is global_vars.emailID
        getAvgDrawNumQueryString = f'SELECT avg(s.drawNum) FROM Student AS s WHERE s.emailID = \'{global_vars.emailID}\''
        emailIDsToAdd = []
        for key, value in info.items():
            if value != '' and key != 'inputType': # or "" or whatever means empty input
                emailID = value
                getAvgDrawNumQueryString += f' OR s.emailID = \'{emailID}\''
                emailIDsToAdd.append(emailID)
        getAvgDrawNumQueryString += ';'
        global_vars.cursor.execute(getAvgDrawNumQueryString)

        avgDrawNum = global_vars.cursor.fetchone()[0] # there's only one (single-value) result tuple that contains the average

        # now that we have the avg draw num, add all students to the SuiteGroup table with this avg draw num
        # the avg draw times will be calculated later, just before the draw, after all groups have been created (so it's null for now)
        # The student ID entered first becomes the suite rep
        # If a student is already in a different prospective suite group, that data will be overwritten and they will be part of the new group
        addStudentsQueryString = f'''INSERT INTO SuiteGroup (emailID, avgDrawNum, avgDrawTime, isSuiteRepresentative, suiteID) VALUES
                                     (\'{emailIDsToAdd[0]}\', {avgDrawNum}, NULL, TRUE, NULL)'''
        # add the students to the suite group
        for emailID in emailIDsToAdd[1:]:
            if (emailID != ''):
                addStudentsQueryString += f', (\'{emailID}\', {avgDrawNum}, NULL, FALSE, NULL)'

        addStudentsQueryString += ';'
        # print(addStudentsQueryString)
        global_vars.cursor.execute(addStudentsQueryString)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
