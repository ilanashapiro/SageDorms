import traceback
import mysql.connector
import sys
import names
import random
from datetime import datetime

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
    create_tables(cursor)

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


def create_tables(cursor):
    """ Creates all the schemas (tables) in this database. This will have:
        ClosetType, CommonRoom, DrawsUp
        Dorm, DormRoom, Room
        Student, Suite, WindowType

    Keyword arguments:
    cursor -- executes SQL commands
    """

    # dictionary of tables
    tables = {}

    """
    Questions:
        - not null?
        - avgDrawTime: how to get average of time?
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
        dormName CHAR(15) DEFAULT 'Deferred',
        dormRoom CHAR(4) DEFAULT 'Def') ENGINE=InnoDB;
        '''

    # add tables to database
    for t in tables:
        cursor.execute(tables[t])

def selectDormRooms(cursor, info) {
    queryString = '''SELECT *
        FROM DormRoom AS dr, Room AS r
        WHERE r.isReservedForSponsorGroup = FALSE'''
    for key, value in info.items():
        if info[value] is not None:
            if (key == "dormNum" or
                key == "dormName" or
                key == "numOccupants" or
                key == "hasPrivateBathroom" or
                key == "numDoors" or
                key == "closetType" or
                key == "hasConnectingRoom"):
                    if (key == "hasConnectingRoom"):
                        queryString += f' AND dr.connectingRoomNum IS NOT NULL'
                    else:
                        queryString += f' AND dr.{info[key]} = {info[value]}'
                        if key == "dormName" || key == "dormNum":
                            queryString += f' AND dr.{info[key]} = r.{info[key]}'
            else:
                queryString += f' AND r.{info[key]} = {info[value]}'
    queryString += ';'

    cursor.execute(queryString)
    cursor.fetchall()


#old way without loop (could use for debugging, but's it's pretty messy)
    #
    # if info['dormNum'] is not None:
    #         queryString += f' AND dr.number = {info['dormNum']} AND dr.number = r.number'
    # if info['dormName'] is not None:
    #     if (!hasOneCondition):
    #     queryString += f' AND dr.dormName = {info['dormName']} AND dr.dormName = r.dormName'
    # if info['numOccupants'] is not None:
    #     queryString += f' AND dr.numOccupants = {info['numOccupants']}'
    # if info['hasPrivateBathroom'] is not None:
    #     queryString += f' AND dr.hasPrivateBathroom = {info['hasPrivateBathroom']}'
    # if info['numDoors'] is not None:
    #     queryString += f' AND dr.numDoors = {info['numDoors']}'
    # if info['closetType'] is not None:
    #     queryString += f' AND dr.closetType = {info['closetType']}'
    # if info['hasConnectingRoom'] is not None:
    #     queryString += f' AND dr.connectingRoomNum IS NOT NULL'
    # if info['floorNum'] is not None:
    #     queryString += f' AND r.floorNum = {info['floorNum']}'
    # if info['squareFeet'] is not None:
    #     queryString += f' AND r.squareFeet = {info['squareFeet']}'
    # if info['isSubFree'] is not None:
    #     queryString += f' AND r.isSubFree = {info['isSubFree']}'
    # if info['windowType'] is not None:
    #     queryString += f' AND r.windowType = {info['windowType']}'
    # if info['windowType'] is not None:
    #     queryString += f' AND r.windowType = {info['windowType']}'
    # if info['suite'] is not None:=
    #     queryString += f' AND r.suite = {info['suite']}'
    # queryString += ';'
}


def main(option = 'i', info = None):
    """ Main method runs hello world app

        TODO:
            - invalid entry
            - SQL injection???
            - from what database will we get student information
    """
    print("OPTION", option)
    try:
        # connect to localhost mysql server
        sagedormsdb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="databases133")

        # cursor executes SQL commands
        cursor = sagedormsdb.cursor()
        init_db(cursor)
        # generate_fake_students(sagedormsdb, cursor)

        # # update dorm
        if (option == 'u'):
            cursor.execute(f'''
                UPDATE Student
                SET
                    dormName = '{info['dormName']}',
                    dormRoom = '{info['dormRoom']}'
                WHERE sid = {info['sid']}
            ''')
            sagedormsdb.commit()
            cursor.close()
            return "success"

        # retrieve students
        elif (option == 'r'):
            result = cursor.execute("SELECT * FROM Students;")
            return cursor.fetchall()

        cursor.close()

    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")

        print(traceback.format_exc())

if __name__ == '__main__':
    main()
