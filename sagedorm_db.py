import traceback
import mysql.connector
import sys
import random
import app
import csv
import re
import global_vars
import populate_database
import suite_queries
import room_queries
import wish_list_queries
from datetime import datetime
from mysql.connector import Error
from random import getrandbits

def init_db():
    """Creates the sagedorms database

    Keyword arguments:
    global_vars.cursor -- executes SQL commands
    """

    # get created databases
    global_vars.cursor.execute("SHOW DATABASES like 'sagedormsdb';")
    db_names = [i[0] for i in global_vars.cursor.fetchall()]

    # create database if not yet already
    if('sagedormsdb' not in db_names):
        global_vars.cursor.execute("CREATE DATABASE IF NOT EXISTS sagedormsdb;")
        global_vars.cursor.execute("USE sagedormsdb;")
        executeScriptsFromFile("tables.sql")

    global_vars.cursor.execute("USE sagedormsdb;")

def generate_fake_students(sagedormsdb):
    """ Generates many fake students for 'room draw'

    Keyword arguments:
    global_vars.cursor -- executes SQL commands
    """

    for i in range(100):
        sid = 10000000 + i
        name = names.get_full_name()
        year = 2020 + (i%10)
        drawNum = random.randrange(1,101)
        drawTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drawGroup = str(random.randrange(1, 10))
        isDrawing = 1

        global_vars.cursor.execute(f'''INSERT INTO Student VALUES(
                {sid}, '{name}', {year}, {drawNum}, '{drawTime}',
                '{drawGroup}', {isDrawing}, dormRoomNum, dormName,
                1, avgSuiteGroupDrawNum , '{drawTime}')''')
        sagedormsdb.commit()

def executeScriptsFromFile(filename):
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
                global_vars.cursor.execute(command + ";")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

# def main(info = None):
#     """ Main method runs hello world app
#
#         TODO:
#             - invalid entry
#             - SQL injection???
#             - from what database will we get student information
#     """
    # try:
        # connect to localhost mysql server
        # sagedormsdb = mysql.connector.connect(
        #         host="localhost",
        #         user="root",
        #         passwd="databases133",
        #         auth_plugin='mysql_native_password',
        #         autocommit=True)
        #
        # # global_vars.cursor executes SQL commands
        # global_vars.cursor = sagedormsdb.cursor()
        # global_vars.emailID = 'issa2018'
        # init_db()
        #
        # global_vars.emailID = 'issa2018'

        # info = {'dormName': 'NORTON-CLARK', 'number': '18'}
        # info = {'numOccupants': 2, 'hasPrivateBathroom': True, 'hasConnectingRoom': True}
        # info = {'Ilana': 'issa2018', 'Helen': 'hpaa2018', 'Gabe': 'gpaa2018', 'Alan': 'ayza2018', 'Yurie': 'ymac2018'}
        # info = {'isSubFree': True, 'numPeople': 6}
        # suite_queries.createSuiteGroup(global_vars.cursor, info)


        # info = {'dormName': 'NORTON-CLARK', 'number': '18'}
        # info = {'numOccupants': 2, 'hasPrivateBathroom': True, 'hasConnectingRoom': True}
        # info = {'Ilana': 'issa2018', 'Helen': 'hpaa2018', 'Gabe': 'gpaa2018', 'Alan': 'ayza2018', 'Yurie': 'ymac2018'}
        # info = {'isSubFree': True, 'numPeople': 6}
        # info = {'suiteID': 'oxeoqmej', 'emailIDSuiteRep':'issa2018'}
        # info = {'emailIDInSG': 'gpaa2018', 'isNewSuiteRep': True}
        # info = {'numOccupants': '2'}
        # print(room_queries.searchForDormRooms(info))
        # suite_queries.setSuite(info)

        # populate_database.createDorms(global_vars.cursor)
        # populate_database.populateRooms(global_vars.cursor)
        # populate_database.populateDormRooms(global_vars.cursor)
        # populate_database.addConnectingRoomInfo(global_vars.cursor)
        # populate_database.addStudents(global_vars.cursor)
        # populate_database.createSuites(global_vars.cursor)

        # global_vars.cursor.close()


    # except mysql.connector.Error as e:
    #     if (e.errno == 1045):
    #         print("Wrong password; did you enter databases133 ???")
    #     print(traceback.format_exc())

if __name__ == '__main__':
    main()
