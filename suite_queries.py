import string
import random
import mysql.connector
import global_vars
from mysql.connector import Error

def getSuiteSummaryForSuite(suiteID):
    '''
    Get the summary data for a specified suite
    '''
    try:
        global_vars.cursor.callproc('GetSuiteSummaryForSuite', [suiteID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getSuiteSummaryForSuiteGeneric(suiteID):
    '''
    Get the summary data for a specified suite
    '''
    try:
        global_vars.cursor.callproc('GetSuiteSummaryForSuiteGeneric', [suiteID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def searchForSuites(info):
    '''
    Searches for and returns the suite data whose search criteria is contained in the info dictionary
    Dynamically builds the query string to handle variable input
    '''
    queryString = '''SELECT s.suiteID, s.numPeople, s.isSubFree, s.dormName FROM Suite AS s'''
    isFirstCond = True
    for key, value in info.items():
        if value != '': # empty input
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

    queryString += ' ORDER BY s.dormName;'
    try:
        global_vars.cursor.execute(queryString)
        suites = global_vars.cursor.fetchall()

        results = []
        for suite in suites:
            suiteID = suite[0] # suites is a list tuples, e.g. [('hjeshkgd',...), ('kadzvtir',...)], with suiteID as the first elem of each tuple
            results.append(getSuiteSummaryForSuite(suiteID))
        return results
    except mysql.connector.Error as error:
        print("Failed to execute query string: {}".format(error))

def getSuiteSummaryForDorm(info):
    '''
    Get the data for the suites of a specified dorm (contained in the info dictionary)
    Gets data for ALL suites, including those that are selected: this is for informational purposes ONLY,
    to be used in View Dorms dorm information page, NOT search for suites where the selection actually happens
    '''
    try:
        global_vars.cursor.callproc('GetSuitesForDorm', [info['dormName']])
        suites = []
        for resultSuite in global_vars.cursor.stored_results():
            suites.append(resultSuite.fetchall())
        results = []
        for suite in suites[0]:
            suiteID = suite[0] # suites is a list tuples, e.g. [('hjeshkgd',...), ('kadzvtir',...)], with suiteID as the first elem of each tuple
            suiteSummary = getSuiteSummaryForSuiteGeneric(suiteID)
            # if len(suiteSummary[0]) > 0:
            results.append(suiteSummary)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMySuiteDetails():
    '''
    Get the data for the suite my group has selected
    '''
    try:
        global_vars.cursor.callproc('GetMySuiteDetails', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def removeMyselfFromSuiteGroup():
    '''
    Remove myself from my current suite group
    '''
    try:
        global_vars.cursor.callproc('RemoveMyselfFromSuiteGroup', [global_vars.emailID])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addMyselfToSuiteGroup(info):
    '''
    Add myself to a specified suite group (determined by the emailID of someone in the suite group that
    is contained in the info dict). Also handle errors relating to invalid input of the suite memeber emailID
    '''
    try:
        emailIDInSG = info['emailIDInSG']
        global_vars.cursor.callproc('GetMySuiteGroup', [emailIDInSG])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        existingSuiteGroup = results[0]
        if len(existingSuiteGroup) == 0:
            return "ERROR: Your must enter someone who is already in a suite group!"
        if len(existingSuiteGroup) == 6:
            return "ERROR: This suite group is already full with 6 people. Try a different group."

        global_vars.cursor.callproc('AddMyselfToSuiteGroup', [global_vars.emailID, info['emailIDInSG'], False])
        return "" # no error message
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMySuiteGroup():
    '''
    Get the data for the people in my suite group
    '''
    try:
        global_vars.cursor.callproc('GetMySuiteGroup', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def setSuite(info):
    '''
    Set the suite (contained in the info dict) for myself and all members of my suite group
    '''
    try:
        global_vars.cursor.callproc('SetSuite', [info['suiteID'], info['emailIDSuiteRep']])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def isCurrentUserSuiteRepresentative():
    '''
    Determine if I (the logged in user) am the current suite rep for my group
    '''
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
    '''
    Get the number of people in a particular suite, specified in the info dict
    '''
    try:
        suiteID = info['suiteID']
        queryString = f'SELECT s.numPeople FROM Suite AS s WHERE s.suiteID = \'{suiteID}\';'
        global_vars.cursor.execute(queryString)
        info = global_vars.cursor.fetchall()
        return info[0][0]
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def setSuiteRepresentative(info):
    '''
    Set the suite rep (specified in the info dict) for my group (the logged in user's group)
    '''
    try:
        mySuiteGroup = getMySuiteGroup()[0]
        emailID = info['emailID']
        suiteGroupIDs = [person[1] for person in mySuiteGroup]

        if emailID not in suiteGroupIDs:
            return "ERROR: You must enter a suite rep that is in your group!"
        global_vars.cursor.callproc('SetSuiteRepresentative', [info['emailID']])
        return "" # no error message
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def createSuiteGroup(info):
    '''
    Create a suite group based in the info in the info dict
    Dynamically build the SQL query to reflect variable input
    First make sure input of suite memebers is valid
    Then calculate the average draw num for all of you
    Then create the suite group
    Return an error message if at any point an error is encountered
    '''
    try:
        # note: we know you are not already in a suite group and have not selected a single, since that is the only way you can access this page
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

        if global_vars.emailID not in emailIDsToAdd:
            return "ERROR: You must be in the suite group that you create"

        # ensure that no one in the suite group hasn't already selected a single
        suiteGroupSinglesQueryString = f'SELECT s.dormName FROM Student AS s'
        isFirstCond = True
        for emailID in emailIDsToAdd:
            if isFirstCond:
                suiteGroupSinglesQueryString += f' WHERE s.emailID = \'{emailID}\''
                isFirstCond = False
            else:
                suiteGroupSinglesQueryString += f' OR s.emailID = \'{emailID}\''
        suiteGroupSinglesQueryString += ';'
        global_vars.cursor.execute(suiteGroupSinglesQueryString)
        rooms = global_vars.cursor.fetchall()
        if len(rooms) - rooms.count((None,)) > 0:
            return "ERROR: Someone in your suite group has already selected a room. They can't be in a suite group."

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
        global_vars.cursor.execute(addStudentsQueryString)

        mySuiteGroup = getMySuiteGroup()[0]
        if len(mySuiteGroup) == 0:
            return "ERROR: Suite group was not successfully created. Did you enter the email IDs of everyone correctly? Remember -- you cannot enter someone who is already in a different suite group."
        return "" # no error message # no error message
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
        return "ERROR: Suite group was not successfully created. Did you enter the email IDs of everyone correctly? Remember -- you cannot enter someone who is already in a different suite group."
