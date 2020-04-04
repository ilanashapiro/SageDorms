import traceback
import mysql.connector

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

def main(option = 'i', info = None):
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
                passwd="databases133")

        # cursor executes SQL commands
        cursor = sagedormsdb.cursor()
        init_db(cursor)

        # update dorm
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
            result = cursor.execute("SELECT * FROM Student;")
            return cursor.fetchall()

    except mysql.connector.Error as e:
        if (e.errno == 1045):
            print("Wrong password; did you enter databases133 ???")

        print(traceback.format_exc())

if __name__ == '__main__':
    main()
