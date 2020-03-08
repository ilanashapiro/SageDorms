import traceback
import mysql.connector

def init_db(cursor):
    '''
    Creates the sagedorms database

    Params:
        - cursor    executes SQL commands
    '''

    # get created databases
    cursor.execute("SHOW DATABASES like 'sagedormsdb';")
    db_names = [i[0] for i in cursor.fetchall()]

    # create database if not yet already
    if('sagedormsdb' not in db_names):
        cursor.execute("CREATE DATABASE IF NOT EXISTS sagedormsdb;")

    cursor.execute("USE sagedormsdb;")

def create_tables(cursor):
    '''
    Creates all the schemas (tables) in this database. This will have:
        ClosetType
        CommonRoom
        DrawsUp
        Dorm
        DormRoom
        Room
        Student
        Suite
        WindowType

    Params:
        - cursor    executes SQL commands
    '''

    # dictionary of tables
    tables = {}

    """
    Questions:
        - not null?
        - avgDrawTime: how to get average of time?
    Notes:
        -
    """
    tables['Student'] = '''CREATE TABLE IF NOT EXISTS Student(
        sid INT(9) ZEROFILL UNSIGNED PRIMARY KEY NOT NULL, 
        fname CHAR(31) NOT NULL, 
        lname CHAR(31) NOT NULL, 
        drawNum SMALLINT UNSIGNED NOT NULL, 
        drawGroupNum TINYINT UNSIGNED NOT NULL, 
        drawTime DATETIME NOT NULL, 
        avgDrawTime DATETIME, 
        avgDrawNum NUMERIC UNSIGNED, 
        dormName CHAR(15) NOT NULL DEFAULT 'Deferred', 
        dormRoom CHAR(4) NOT NULL DEFAULT 'Deferred') ENGINE=InnoDB;
        '''

    # add tables to database
    for t in tables:
        cursor.execute(tables[t])


if __name__ == "__main__":
    '''
        Main method runs hello world app
    '''
    try:
        # connect to localhost mysql server
        sagedormsdb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="databases133")

        # cursor executes SQL commands
        cursor = sagedormsdb.cursor()

        init_db(cursor)
        create_tables(cursor)


    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")

        print(traceback.format_exc())


