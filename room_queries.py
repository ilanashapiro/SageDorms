import string
import random
import mysql.connector
from mysql.connector import Error

def searchForDormRooms(cursor, info):
    queryString = '''SELECT DISTINCT r.dormName, r.number FROM DormRoom AS dr, Room AS r WHERE r.isReservedForSponsorGroup = FALSE'''
    for key, value in info.items():
        if value is not None: # or "" or whatever means empty input
            # case this is dormRoom info
            if (key == "dormName" or
                key == "number" or
                key == "numOccupants" or
                key == "hasPrivateBathroom" or
                key == "hasConnectingRoom"):
                    if key == "hasConnectingRoom":
                        if value == False:
                            queryString += f' AND dr.connectingRoomNum IS NULL'
                            print("false")
                        else:
                            queryString += f' AND dr.connectingRoomNum IS NOT NULL'
                    else:
                        if key == "number" or key == "dormName":
                            # data is string value, enclose in quote
                            queryString += f' AND dr.{key} = \'{value}\''
                        else:
                            # data is not a string value, no quotes
                            queryString += f' AND dr.{key} = {value}'
            else: # this is room, rather than dormRoom, information
                queryString += f' AND r.{key} = {value}'
    # perform the join
    queryString += f' AND dr.dormName = r.dormName AND dr.number = r.number;'

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
