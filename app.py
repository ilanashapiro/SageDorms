from flask import Flask, render_template, request, redirect, session, jsonify
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
    data = wish_list_queries.getMyWishList()
    print(data)
    return render_template('wishlist.html', data = data)

def addToWishListHelper(data):
    ''' Adds room to wishlist; called by each room in their POST requests
    '''
    if (session['username']):
        global_vars.emailID = session['username']
        info = {}
        info['dormName'] = data[0]
        info['dormRoomNum'] = data[1]
        wish_list_queries.addToWishList(info)
        return jsonify(user=session['username'])
    else:
        return redirect('login')

@app.route('/smiley', methods=['GET', 'POST'])
def smiley():

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Smiley'}
    data = room_queries.searchForDormRooms(info)
    sdata = suite_queries.searchForSuites(info)
    return render_template('smiley.html', data=data, sdata=sdata)

@app.route('/clark1', methods=['GET', 'POST'])
def clark1():

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Clark-I'}
    data = room_queries.searchForDormRooms(info)
    sdata = suite_queries.searchForSuites(info)
    return render_template('clark1.html', data=data, sdata=sdata)

@app.route('/clark5', methods=['GET', 'POST'])
def clark5():

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Clark-V'}
    data = room_queries.searchForDormRooms(info)
    sdata = suite_queries.searchForSuites(info)
    return render_template('clark5.html', data=data, sdata=sdata)

@app.route('/norton', methods=['GET', 'POST'])
def norton():

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Norton-Clark'}
    data = room_queries.searchForDormRooms(info)
    sdata = suite_queries.searchForSuites(info)
    return render_template('norton.html', data=data, sdata=sdata)

@app.route('/walker', methods=['GET', 'POST'])
def walker():

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Walker'}
    data = room_queries.searchForDormRooms(info)
    sdata = suite_queries.searchForSuites(info)
    return render_template('walker.html', data=data, sdata=sdata)

@app.route('/lawry', methods=['GET', 'POST'])
def lawry():

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Lawry'}
    data = room_queries.searchForDormRooms(info)
    sdata = suite_queries.searchForSuites(info)
    return render_template('lawry.html', data=data, sdata=sdata)

@app.route('/displayRoomSelectionInfo', methods=['POST'])
def displayRoomSelectionInfo():
    # student selected housing
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form

        # add to wishlist
        if len(rawinfo) == 1:
            # get email if logged in
                return addToWishListHelper(rawinfo['room'].split())

        else:
            info = rawinfo.to_dict(flat=False)
            #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
            for key, value in info.items():
                info[key] = value[0]

            data = None
            data = room_queries.searchForDormRooms(info)
            hasNotChosen = len(room_queries.getMyRoomDetails()[0]) == 0
            myWishList = wish_list_queries.getMyWishList()[0]
            print("WISHLIST", myWishList)
            return render_template('displayRoomSelectionInfo.html', data=data, hasNotChosen = hasNotChosen, myWishList = myWishList)

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
        result = filter(lambda suite: len(suite[0]) > 0, data)
        hasNotChosen = len(suite_queries.getMySuiteDetails()[0]) == 0
        return render_template('displaySuiteSelectionInfo.html', data=result, hasNotChosen = hasNotChosen)
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

@app.route('/viewMyRoom', methods=['GET', 'POST'])
def viewMyRoom():
    if request.method == 'POST':
        print(request.form)
        info = {}

        #select room
        if 'room' in request.form:
            roomSelectInfo = request.form['room'].split()
            info['dormName'] = roomSelectInfo[0]
            info['dormRoomNum'] = roomSelectInfo[1]
            info['roommateEID'] = None
            room_queries.setStudentRoom(info)

        #select suite
        else:
            suiteSelectInfo = request.form['suite'].split()
            info['suiteID'] = suiteSelectInfo[0]
            info['emailIDSuiteRep'] = global_vars.emailID
            suite_queries.setSuite(info)

        roomData = room_queries.getMyRoomDetails()
        suiteData = suite_queries.getMySuiteDetails()
        dataDict = {'roomData' : roomData, 'suiteData' : suiteData}
        print(dataDict)
        return render_template('viewMyRoom.html', data = dataDict)

    print("ID", global_vars.emailID)
    # info = {'suiteID' : 'oxeoqmej', 'emailIDSuiteRep' : 'hpaa2018'}
    # suite_queries.setSuite(info)
    roomData = room_queries.getMyRoomDetails()
    suiteData = suite_queries.getMySuiteDetails()
    dataDict = {'roomData' : roomData, 'suiteData' : suiteData}
    print("DATADICT", dataDict)
    return render_template('viewMyRoom.html', data = dataDict)

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
