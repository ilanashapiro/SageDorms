import string
import random
import mysql.connector
import global_vars
from mysql.connector import Error

def getSummaryForDormRoom(dormName, number):
    try:
        global_vars.cursor.callproc('GetSummaryForDormRoom', [dormName, number])
        results = []
        for result in global_vars.cursor.stored_results():
            data = result.fetchall()
            print(data)
            if len(data) > 0: # if it's a common room, dorm room info will be empty, and vice versa
                results.append(data)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def searchForDormRooms(info):
    queryString = 'SELECT DISTINCT r.dormName, r.number FROM DormRoom AS dr, Room AS r'
    isFirstCond = True
    foundInfo = False
    for key, value in info.items():
        if value != '': # empty input
            foundInfo = True
            # case this is dormRoom info
            if isFirstCond:
                queryString += ' WHERE r.isReservedForSponsorGroup = FALSE'
                isFirstCond = False
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
            else: # this is room, rather than dormRoom, information.
                queryString += f' AND r.{key} = {value}'
    if foundInfo:
        # perform the join
        queryString += f' AND dr.dormName = r.dormName AND dr.number = r.number'
    else:
        queryString += f' WHERE dr.dormName = r.dormName AND dr.number = r.number'

    # order results
    queryString += f' ORDER BY CAST(r.number AS unsigned);'

    # print(queryString)
    global_vars.cursor.execute(queryString)

    rooms = global_vars.cursor.fetchall()
    # print(rooms)
    results = []
    for room in rooms:
        dormName = room[0] # rooms is a list tuples, with dormName and number as elements 0 and 1 of the tuple
        number = room[1]
        results.append(getSummaryForDormRoom(dormName, number))

    # print(results)
    return results

def getDormRoomSummaryForDorm(info):
    try:
        global_vars.cursor.callproc('GetDormRoomSummaryForDorm', [info['dormName']])
        rooms = []
        for resultRoom in global_vars.cursor.stored_results():
            rooms.append(resultRoom.fetchall())
        results = []
        for room in rooms[0]:
            dormName = room[0] # rooms is a list tuples, with dormName and number as elements 0 and 1 of the tuple
            number = room[1]
            print("dormname, number: ", dormName, number)
            results.append(getSummaryForDormRoom(dormName, number))

        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

# https://pynative.com/python-mysql-execute-stored-procedure/
def setStudentRoom(info):
    try:
        # print(global_vars.emailID, info["roommateEID"], info["dormName"], info["dormRoomNum"])
        global_vars.cursor.callproc('SetStudentRoom', [global_vars.emailID, info["roommateEID"], info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getDormRoomsSinglesSummary():
    try:
        global_vars.cursor.callproc('GetDormRoomsSinglesSummary', [])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getDormRoomAndSuiteSummaryForDorm(info):
    try:
        global_vars.cursor.callproc('GetDormRoomAndSuiteSummaryForDorm', [info['dormName']])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        print(results)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getRoomDetails(info):
    try:
        global_vars.cursor.callproc('GetRoomDetails', [info["dormName"], info["dormRoomNum"]])
        results = []
        for result in global_vars.cursor.stored_results():
            data = result.fetchall()
            if (len(data) > 0): # if it's a common room, dorm room info will be empty, and vice versa
                results.append(data)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def getMyRoomDetails():
    try:
        global_vars.cursor.callproc('GetMyRoomDetails', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))

def getMyRoommateInfo():
    try:
        global_vars.cursor.callproc('GetMyRoommateInfo', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))

def isRoomSelected(info):
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
