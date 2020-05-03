from flask import Flask, render_template, request, redirect, session
import sagedorm_db
import mysql.connector
import random
import cas_login
import global_vars
import room_queries
import suite_queries
import wish_list_queries
import sys
app = Flask(__name__)
app.secret_key = "shhhhh keep it a secret"

@app.route('/', methods=['GET', 'POST'])
# called when you go to localhost 5000
def index():
    # # student selected housing
    # if request.method == 'POST':
        # # save all inputted data
        # student = request.form
        # name = student['name'].split(" ")
        # studInfo = {}
        # studInfo['fname'] = name[0]
        # studInfo['lname'] = name[1]
        # studInfo['sid'] = int(student['sid'])
        # studInfo['dormName'] = student['dormName']
        # studInfo['dormRoom'] = random.randint(1, 999)

        # table to be properly created later when parsing room request data (i.e. user-selected filters)
        # for now, this is psuedocode that will be referenced in the dynamically built SQL query in sagedorm_db.property
        # info = request.form
        # roomInfo = {}
        # roomInfo['dormNum'] = .....
        # roomInfo['dormName'] = .....
        # roomInfo['numOccupants'] = .....
        # roomInfo['hasPrivateBathroom'] = .....
        # roomInfo['numDoors'] = .....
        # roomInfo['closetType'] = .....
        # roomInfo['hasConnectingRoom'] = .....
        # roomInfo['floorNum'] = .....
        # roomInfo['squareFeet'] = .....
        # roomInfo['isSubFree'] = .....
        # roomInfo['windowType'] = .....
        # roomInfo['isSuite'] = .....
        # sagedorm_db.selectRooms(....)

        # table to be properly created later when parsing student chooses room data
        # is there a way to remember which student is logged in, and get the SID from there without the student inputting it directly into a form???
        # info = request.form
        # roomChoiceInfo = {}
        # roomChoiceInfo['dormRoomNum'] = .....
        # roomChoiceInfo['dormName'] = .....
        # roomChoiceInfo['SID'] = somehow get the sid of the logged in student directly???

        # table to be properly created later when parsing create prospective suite group data
        # Idea is the student creating the group puts all OTHER members' SIDs in the form (So up to 5 for 6 total), and the student filling out the form becomes the suite group
        #       representative that will register the suite later on
        # some fields will be null since a suite can have up to 6 people. However an error should get displayed if the user inputs in less than 2 names (for 3 total)
        # is there a way to remember which student is logged in, and get the SID from there without the student inputting it directly into a form???
        # info = request.form
        # SuiteGroupInfo = {}
        # SuiteGroupInfo['sid2'] = .....
        # SuiteGroupInfo['sid3'] = ...
        # SuiteGroupInfo['sid4'] = ...
        # SuiteGroupInfo['sid5'] = ...
        # SuiteGroupInfo['sid6'] = ...

        # initialize mysql server and database
        # sagedorm_db.main('u', studInfo)
    loggedIn = False
    if 'cookies' in session:
        loggedIn = True
        global_vars.emailID = session['username']
    return render_template('index.html', loggedIn=loggedIn)

@app.route('/test')
def test():
    students = sagedorm_db.main(session['username'])
    return render_template('students.html', students=students)

@app.route('/dorms')
def dorms():
    return render_template('generic.html')

@app.route('/wishlist')
def wishlist():
    data = wish_list_queries.getMyWishList(global_vars.cursor)
    return render_template('wishlist.html', data = data)

@app.route('/smiley', methods=['GET', 'POST'])
def smiley():
    if request.method == 'POST':

        # get email if logged in
        if session['username']:
            global_vars.emailID = session['username']

            # data is in the form of {"room" : "name num"}
            room = request.form['room'].split()
            info = {}
            info['dormName'] = room[0]
            info['dormRoomNum'] = room[1]
            wish_list_queries.addToWishList(global_vars.cursor, info)
        else:
            return redirect('login')
    return render_template('smiley.html')

@app.route('/displayRoomSelectionInfo', methods=['GET', 'POST'])
def displayRoomSelectionInfo():
    # student selected housing
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form
        info = rawinfo.to_dict(flat=False)
        #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
        for key, value in info.items():
            info[key] = value[0]

        data = None
        data = room_queries.searchForDormRooms(info)
        # print("DATA", type(data[0][0]), data[0][0][0][0])
        return render_template('displayRoomSelectionInfo.html', data=data)
    return render_template('displayRoomSelectionInfo.html')

@app.route('/displaySuiteSelectionInfo', methods=['GET', 'POST'])
def displaySuiteSelectionInfo():
    # student selected housing
    # if request.method == 'POST':
    # info = {'number': 'issa2018', 'Helen': 'hpaa2018', 'Gabe': 'gpaa2018', 'Alan': 'ayza2018', 'Yurie': 'ymac2018'}
    # info = [['suite1', 'room1'], ['suite1', 'room2'], ['suite1', 'room3']]
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form
        info = rawinfo.to_dict(flat=False)
        #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
        for key, value in info.items():
            info[key] = value[0]
        data = suite_queries.searchForSuites(info)
        return render_template('displaySuiteSelectionInfo.html', data=data)
    return render_template('displaySuiteSelectionInfo.html')

# @app.route('/viewRoomDetails', methods=['GET'])
# def viewRoomDetails():
#     rawinfo = request.form
#     info = rawinfo.to_dict(flat=False)
#     #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
#     for key, value in info.items():
#         info[key] = value[0]
#     print(info)
#     # data = room_queries.getRoomDetails(info)
#     # print(data)
#     return render_template('viewRoomDetails.html')#, data = data)

@app.route('/viewSuiteMembers', methods=['GET', 'POST'])
def viewSuiteMembers():
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form
        info = rawinfo.to_dict(flat=False)
        #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
        for key, value in info.items():
            info[key] = value[0]
        print("INFO", info)
        suite_queries.removeMyselfFromSuiteGroup(info)
        return redirect('/')
    print("ID", global_vars.emailID)
    data = suite_queries.getMySuiteGroup()
    print("DATA", data)
    return render_template('viewSuiteMembers.html', data = data)

@app.route('/suiteFormation', methods=['GET', 'POST'])
def suiteFormation():
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form
        info = rawinfo.to_dict(flat=False)
        #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
        for key, value in info.items():
            info[key] = value[0]
        if info['inputType'] == 'new':
            suite_queries.createSuiteGroup(info)
        elif info['inputType'] == 'existing':
            suite_queries.addMyselfToSuiteGroup(info)
        return redirect('/')
    return render_template('suiteFormation.html')

# get is when you load, post is when you submit
@app.route('/selectionpage', methods=['GET', 'POST'])
def selectionpage():
    return render_template('selectionpage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # submitted login form
    if request.method == 'POST':

        # the login form data
        info = request.form

        if not (info['dispname'] and info['password'] and 'school' in info):
            return render_template('login.html',error="Please complete all fields")

        # used in login request body
        login_info = {}
        login_info['username'] = f"{info['dispname']}@{info['school']}.edu"
        login_info['dispname'] = info['dispname']
        global_vars.emailID = info['dispname']
        login_info['password'] = info['password']

        # session is a built in vbl that persists as long as the app is running.
        # we login using an external python script. once we login, we save the
        # cookies of the login throughout the app
        cookies = cas_login.main(login_info)
        if cookies:
            session['cookies'] = cookies
            session['username'] = login_info['dispname']
            return redirect('/')

        # no cookies means login failed, so we open the login page again
        return render_template('login.html',error="Invalid credentials")

    return render_template('login.html',error=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    sagedormsdb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="databases133",
            auth_plugin='mysql_native_password',
            autocommit=True)

    # global_vars.cursor executes SQL commands
    global_vars.cursor = sagedormsdb.cursor()
    print(global_vars.cursor)
    sagedorm_db.init_db()
    app.run(debug=True)
