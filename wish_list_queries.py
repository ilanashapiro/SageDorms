import string
import random
import mysql.connector
import global_vars
from mysql.connector import Error

def getMyWishList():
    try:
        global_vars.cursor.callproc('GetMyWishList', [global_vars.emailID])
        results = []
        for result in global_vars.cursor.stored_results():
            results.append(result.fetchall())
        return results
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addToWishList(info):
    try:
        print(global_vars.emailID)
        global_vars.cursor.callproc('AddToWishlist', [global_vars.emailID, info["dormName"], info["number"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def deleteFromWishList(info):
    try:
        global_vars.cursor.callproc('DeleteFromWishList', [global_vars.emailID, info["dormName"], info["number"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
