import string
import random
import mysql.connector
import global_vars
from mysql.connector import Error

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
        print(global_vars.emailID)
        cursor.callproc('AddToWishlist', [global_vars.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def deleteFromWishList(cursor, info):
    try:
        cursor.callproc('DeleteFromWishList', [global_vars.emailID, info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
