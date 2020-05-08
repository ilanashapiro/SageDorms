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

def executeScriptsFromFile(filename):
    '''
    Takes in a file name and delimiter, and parses and executes the SQL commands in the file
    '''
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
