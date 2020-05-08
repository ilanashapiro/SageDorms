import string
import random
import mysql.connector
import global_vars
from mysql.connector import Error

def getSummaryForDormRoom(dormName, number):
    '''
    Get the summary data for a specified dorm room, if the room has NOT yet been selected
    Used for search results for room search, where the student can actually select a room
    '''
    try:
        global_vars.cursor.callproc('GetSummaryForDormRoom', [dormName, number])
        results = []
        for result in global_vars.cursor.stored_results():
            data = result.fetchall()
            if len(data) > 0: # if it's a common room, dorm room info will be empty, and vice versa
                results.append(data)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getSummaryForDormRoomGeneric(dormName, number):
    '''
    Get the summary data for a specified dorm room, REGARDLESS if the room has been selected
    Used for informational summary of dorms in the View Dorms page
    '''
    try:
        global_vars.cursor.callproc('GetSummaryForDormRoomGeneric', [dormName, number])
        results = []
        for result in global_vars.cursor.stored_results():
            data = result.fetchall()
            if len(data) > 0: # if it's a common room, dorm room info will be empty, and vice versa
                results.append(data)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def searchForDormRooms(info):
    '''
    Searches for and returns the dorm room data whose search criteria is contained in the info dictionary
    Dynamically builds the query string to handle variable input
    '''
    queryString = 'SELECT DISTINCT r.dormName, r.number FROM DormRoom AS dr, Room AS r'
    isFirstCond = True
    foundInfo = False
    for key, value in info.items():
        if value != '': # empty input
            foundInfo = True
            if isFirstCond:
                queryString += ' WHERE r.isReservedForSponsorGroup = FALSE'
                isFirstCond = False

            # case this is dormRoom info
            if (key == "dormName" or
                key == "number" or
                key == "numOccupants" or
                key == "hasPrivateBathroom" or
                key == "hasConnectingRoom"):
                    if key == "hasConnectingRoom":
                        if value == False:
                            queryString += f' AND dr.connectingRoomNum IS NULL'
                        else:
                            queryString += f' AND dr.connectingRoomNum IS NOT NULL'
                    else:
                        if key == "number" or key == "dormName":
                            # data is string value, enclose in quote
                            queryString += f' AND dr.{key} = \'{value}\''
                        else:
                            # data is not a string value, no quotes
                            queryString += f' AND dr.{key} = {value}'
            # case this is room, rather than dormRoom, information.
            else:
                queryString += f' AND r.{key} = {value}'
    if foundInfo:
        # perform the join
        queryString += f' AND dr.dormName = r.dormName AND dr.number = r.number'
    else:
        queryString += f' WHERE dr.dormName = r.dormName AND dr.number = r.number'

    # order results
    queryString += f' ORDER BY r.dormName, CAST(r.number AS unsigned);'

    try:
        global_vars.cursor.execute(queryString)
        rooms = global_vars.cursor.fetchall()

        results = []
        for room in rooms:
            dormName = room[0] # rooms is a list tuples, with dormName and number as elements 0 and 1 of the tuple
            number = room[1]
            results.append(getSummaryForDormRoom(dormName, number))
        return results
    except mysql.connector.Error as error:
        print("Failed to execute query string: {}".format(error))

def getDormRoomSummaryForDorm(info):
    '''
    Get the data for the dorm rooms of a specified dorm (contained in the info dictionary)
    '''
    try:
        global_vars.cursor.callproc('GetDormRoomSummaryForDorm', [info['dormName']])
        rooms = []
        for resultRoom in global_vars.cursor.stored_results():
            rooms.append(resultRoom.fetchall())
        results = []
        for room in rooms[0]:
            dormName = room[0] # rooms is a list tuples, with dormName and number as elements 0 and 1 of the tuple
            number = room[1]
            results.append(getSummaryForDormRoomGeneric(dormName, number))
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def setStudentRoom(info):
    '''
    Set the room for the specified student (contained in the info dict) and
    handle errors (return error message) relating to roommate if applicable
    '''
    try:
        # you're trying to select a double and so must have submitted the roommate form
        if info["roommateEID"] != None:
            roommateEID = info["roommateEID"]
            if (roommateEID == global_vars.emailID):
                return "ERROR: You entered you own email ID. You can't be roommates with yourself"

            # make sure the roommate you enter has not already selected a room, and also that they exist in the database
            queryString = f'SELECT s.dormName FROM Student AS s WHERE s.emailID = \'{roommateEID}\';'
            global_vars.cursor.execute(queryString)
            roommateInfo = global_vars.cursor.fetchall()
            if len(roommateInfo) > 0:
                if roommateInfo[0][0] is not None:
                    return "ERROR: Your desired roommate has already selected a room"
            else:
                return "ERROR: Your desired roommate doesn't seem to exist: did you enter their email ID correctly?"

            # make sure the roommate you enter isn't in a suite group
            queryString = f'SELECT * FROM SuiteGroup AS s WHERE s.emailID = \'{roommateEID}\';'
            global_vars.cursor.execute(queryString)
            roommateSuiteGroupInfo = global_vars.cursor.fetchall()
            if len(roommateSuiteGroupInfo) > 0:
                return "ERROR: Your desired roommate is in a suite group so is not eligible to select a double with you"

        global_vars.cursor.callproc('SetStudentRoom', [global_vars.emailID, info["roommateEID"], info["dormName"], info["dormRoomNum"]])
        return "" # no error message
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMyRoomDetails():
    '''
    Get the data for the room I selected
    '''
    try:
        global_vars.cursor.callproc('GetMyRoomDetails', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))

def getMyRoommateInfo():
    '''
    Get the data for the roommate that is sharing a double with me
    '''
    try:
        global_vars.cursor.callproc('GetMyRoommateInfo', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))

def isRoomSelected(info):
    '''
    Determine if a room (specified in the info dict) has been selected by someone
    '''
    try:
        dormName =  info['dormName']
        number = info['number']
        queryString = f'SELECT * FROM Student AS s WHERE s.dormName = \'{dormName}\' AND s.dormRoomNum = \'{number}\';'
        global_vars.cursor.execute(queryString)
        for result in global_vars.cursor.stored_results():
            info = result.fetchall()
            if len(info) == 1:
                return True
        return False
    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))
