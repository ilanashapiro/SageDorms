import traceback
import mysql.connector
import sys
import names
import random
from datetime import datetime
from mysql.connector import Error

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

def selectDormRooms(cursor, info):
    queryString = '''SELECT *
        FROM DormRoom AS dr, Room AS r
        WHERE r.isReservedForSponsorGroup = FALSE'''
    for key, value in info.items():
        if info[value] is not None: # or "" or whatever means empty input
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
                        if key == "dormName" or key == "dormNum":
                            queryString += f' AND dr.{info[key]} = r.{info[key]}'
            else: # or "" or whatever means empty input
                queryString += f' AND r.{info[key]} = {info[value]}'
    queryString += ';'

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

    cursor.execute(queryString)
    cursor.fetchall()

# https://pynative.com/python-mysql-execute-stored-procedure/
def setStudentRoom(cursor, info):
    try:
        # actually, can we save the SID of the logged-in student in the session somewhere?? Idk how to get that data, this is just a template for now
        cursor.callproc('SetStudentRoom', [info["SID"], info["dormName"], info["dormNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def addToWishList(cursor, info):
    try:
        cursor.callproc('AddToWishlist', [info["SID"], info["dormName"], info["dormNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def deleteFromWishList(cursor, info):
    try:
        cursor.callproc('DeleteFromWishList', [info["SID"], info["dormName"], info["dormRoomNum"]])
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

def createProspectiveSuiteGroup(cursor, info):
    try:
        # query the students in the prospective suite group to calculate average draw num. (note: the emails entered is everyone ELSE in the list,
        # not including the student doing the entering -- that person is STUDENT_EMAIL_FROM_LOGIN which I need to get from Gabe's CAS login...)
        getAvgDrawNumQueryString = f'SELECT avg(s.drawNum) FROM Student AS s WHERE s.email = {STUDENT_EMAIL_FROM_LOGIN}''
        for key, value in info.items():
            if info[value] is not None: # or "" or whatever means empty input
                email = info[value]
                queryString += f' OR s.email = {email}''
                emailsToAdd.append(email)

        cursor.execute(getAvgDrawNumQueryString)
        avgDrawNum = cursor.fetchone()[0] # there's only one (single-value) result tuple that contains the average

        # now that we have the avg draw num, add all students to the ProspectiveSuiteGroup table with this avg draw num
        # the avg draw times will be calculated later, just before the draw, after all groups have been created (so it's null for now)
        # The student doing the entering becomes the suite representative
        # If a student is already in a different prospective suite group, that data will be overwritten and they will be part of the new group
        # If a group wants to add another student, they'll need to fill out the form again to register the group for everyone
        addStudentsQueryString = f'''REPLACE INTO ProspectiveSuiteGroup (email, avgDrawNum, avgDrawTime, isSuiteRepresentative, suiteID) VALUES
                                     ({STUDENT_EMAIL_FROM_LOGIN}, {avgDrawNum}, NULL, TRUE, NULL)'''
        for email in emailsToAdd:
            addStudentsQueryString += f', ({email}, {avgDrawNum}, NULL, FALSE, NULL)'
        # addStudentsQueryString += ' ON DUPLICATE KEY UPDATE avgDrawNum = VALUES(avgDrawNum), isSuiteRepresentative = VALUES(isSuiteRepresentative)'THIS LINE UPDATES EXISTING DATA
        # RATHER THAN REPLACING, COULD USE THIS IF WE WANT TO UPDATE RATHER THAN REPLACE

        addStudentsQueryString += ','
        cursor.execute(addStudentsQueryString)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

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
