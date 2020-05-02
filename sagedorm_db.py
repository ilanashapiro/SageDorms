import traceback
import mysql.connector
import sys
import names
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

def init_db(cursor):
    """Creates the sagedorms database

    Keyword arguments:
    cursor -- executes SQL commands
    """

    # get created databases
    cursor.execute("SHOW DATABASES like 'sagedormsdb';")
    db_names = [i[0] for i in cursor.fetchall()]

    # create database if not yet already
    if('sagedormsdb' not in db_names):
        cursor.execute("CREATE DATABASE IF NOT EXISTS sagedormsdb;")
        cursor.execute("USE sagedormsdb;")
        executeScriptsFromFile("tables.sql", cursor)

    cursor.execute("USE sagedormsdb;")

def generate_fake_students(sagedormsdb, cursor):
    """ Generates many fake students for 'room draw'

    Keyword arguments:
    cursor -- executes SQL commands
    """

    for i in range(100):
        sid = 10000000 + i
        name = names.get_full_name()
        year = 2020 + (i%10)
        drawNum = random.randrange(1,101)
        drawTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drawGroup = str(random.randrange(1, 10))
        isDrawing = 1

        cursor.execute(f'''INSERT INTO Student VALUES(
                {sid}, '{name}', {year}, {drawNum}, '{drawTime}',
                '{drawGroup}', {isDrawing}, dormRoomNum, dormName,
                1, avgSuiteGroupDrawNum , '{drawTime}')''')
        sagedormsdb.commit()

def executeScriptsFromFile(filename, cursor):
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
                cursor.execute(command + ";")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

def main(info = None):
    """ Main method runs hello world app

        TODO:
            - invalid entry
            - SQL injection???
            - from what database will we get student information
    """
    try:
         # connect to localhost mysql server
        sagedormsdb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="databases133",
                auth_plugin='mysql_native_password',
                autocommit=True)

        # cursor executes SQL commands
        cursor = sagedormsdb.cursor()
        init_db(cursor)

        global_vars.emailID = 'issa2018'

        # info = {'dormName': 'NORTON-CLARK', 'number': '18'}
        # info = {'numOccupants': 2, 'hasPrivateBathroom': True, 'hasConnectingRoom': True}
        info = {'Ilana': 'issa2018', 'Helen': 'hpaa2018', 'Gabe': 'gpaa2018', 'Alan': 'ayza2018', 'Yurie': 'ymac2018'}
        # info = {'isSubFree': True, 'numPeople': 6}
        suite_queries.createSuiteGroup(cursor, info)

        # populate_database.createDorms(cursor)
        # populate_database.populateRooms(cursor)
        # populate_database.populateDormRooms(cursor)
        # populate_database.addConnectingRoomInfo(cursor)
        # populate_database.addStudents(cursor)
        # populate_database.createSuites(cursor)

        cursor.close()


    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
