import string
import random
import mysql.connector
import global_vars
import room_queries
from mysql.connector import Error

def getMyWishList():
    try:
        global_vars.cursor.callproc('GetMyWishList', [global_vars.emailID])
        rooms = []
        for result in global_vars.cursor.stored_results():
            rooms.append(result.fetchall())
        results = []
        for room in rooms[0]:
            dormName = room[0] # rooms is a list tuples, with dormName and number as elements 0 and 1 of the tuple
            number = room[1]
            roomDetails = room_queries.getSummaryForDormRoom(dormName, number)
            if len(roomDetails) > 0 and len(roomDetails[0]) > 0:
                results.append(roomDetails[0][0])
            # then, the room has been selected and so was not returned in the room query. Delete the selected room from the wish list
            else:
                info = {}
                info['dormName'] = dormName
                info['number'] = number
                deleteFromWishList(info)
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addToWishList(info):
    try:
        global_vars.cursor.callproc('AddToWishlist', [global_vars.emailID, info["dormName"], info["number"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def deleteFromWishList(info):
    try:
        global_vars.cursor.callproc('DeleteFromWishList', [global_vars.emailID, info["dormName"], info["number"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
