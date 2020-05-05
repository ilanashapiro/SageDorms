from flask import Flask, render_template, request, redirect, session, \
        jsonify, url_for
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
    if 'dispname' in session:
        global_vars.emailID = session['dispname']
    return render_template('index.html')

@app.route('/dorms')
def dorms():
    if 'dispname' not in session:
        return redirectFromLoginTo('dorms')

    return render_template('generic.html')

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if 'dispname' not in session:
        return redirectFromLoginTo('wishlist')

    if request.method == 'POST':
        deleteInfo = request.form['removeRoom'].split()
        info = {}
        info['dormName'] = deleteInfo[0]
        info['number'] = deleteInfo[1]
        wish_list_queries.deleteFromWishList(info)

    data = wish_list_queries.getMyWishList()
    return render_template('wishlist.html', data = data)

def addToWishListHelper(data, redirectPageIfNotLoggedIn):
    ''' Adds room to wishlist; called by each room in their POST requests '''

    # if not logged in
    if 'dispname' not in session:
        return redirectFromLoginTo(redirectPageIfNotLoggedIn)

    global_vars.emailID = session['dispname']
    info = {}
    info['dormName'] = data[0]
    info['number'] = data[1]
    print("INFO", info)
    wish_list_queries.addToWishList(info)
    return jsonify(user=session['dispname'])

@app.route('/smiley', methods=['GET', 'POST'])
def smiley():
    if 'dispname' not in session:
        return redirectFromLoginTo('smiley')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'smiley')

    info = {'': '', 'dormName': 'Smiley'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    print(data)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('smiley.html', data=data, sdata=sdata)

@app.route('/clark1', methods=['GET', 'POST'])
def clark1():
    if 'dispname' not in session:
        return redirectFromLoginTo('clark1')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Clark-I'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('clark1.html', data=data, sdata=sdata)

@app.route('/clark5', methods=['GET', 'POST'])
def clark5():
    if 'dispname' not in session:
        return redirectFromLoginTo('clark5')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Clark-V'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('clark5.html', data=data, sdata=sdata)

@app.route('/norton', methods=['GET', 'POST'])
def norton():
    if 'dispname' not in session:
        return redirectFromLoginTo('norton')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Norton-Clark'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('norton.html', data=data, sdata=sdata)

@app.route('/walker', methods=['GET', 'POST'])
def walker():
    if 'dispname' not in session:
        return redirectFromLoginTo('walker')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Walker'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('walker.html', data=data, sdata=sdata)

@app.route('/lawry', methods=['GET', 'POST'])
def lawry():
    if 'dispname' not in session:
        return redirectFromLoginTo('lawry')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split())

    info = {'': '', 'dormName': 'Lawry'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('lawry.html', data=data, sdata=sdata)

@app.route('/displayRoomSelectionInfo', methods=['POST'])
def displayRoomSelectionInfo():
    if 'dispname' not in session:
        return redirectFromLoginTo('displayRoomSelectionInfo')

    # student selected housing
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form

        # add to wishlist
        if 'wishlist_item' in rawinfo:
            # get email if logged in
            return addToWishListHelper(rawinfo['wishlist_item'].split(), 'displayRoomSelectionInfo')

        else:
            info = rawinfo.to_dict(flat=False)
            #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
            for key, value in info.items():
                info[key] = value[0]

            data = None
            data = room_queries.searchForDormRooms(info)
            hasNotChosen = (len(room_queries.getMyRoomDetails()[0]) == 0 and len(suite_queries.getMySuiteDetails()[0]) == 0)
            print(f"*************************************{hasNotChosen}")
            myWishList = wish_list_queries.getMyWishList()
            if len(myWishList) > 0:
                myWishList = myWishList[0]
            print("myWishList", myWishList)
            return render_template('displayRoomSelectionInfo.html', data=data, hasNotChosen = hasNotChosen, myWishList = myWishList)

@app.route('/displaySuiteSelectionInfo', methods=['GET', 'POST'])
def displaySuiteSelectionInfo():
    if 'dispname' not in session:
        return redirectFromLoginTo('displaySuiteSelectionInfo')

    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form
        info = rawinfo.to_dict(flat=False)

        #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
        for key, value in info.items():
            info[key] = value[0]
        data = suite_queries.searchForSuites(info)
        result = filter(lambda suite: len(suite[0]) > 0, data)
        hasNotChosen = (len(suite_queries.getMySuiteDetails()[0]) == 0 and len(room_queries.getMyRoomDetails()[0]) == 0)
        isSuiteRep = suite_queries.isCurrentUserSuiteRepresentative()
        return render_template('displaySuiteSelectionInfo.html', data=result, hasNotChosen = hasNotChosen, isSuiteRep = isSuiteRep)
    return render_template('displaySuiteSelectionInfo.html')

@app.route('/viewMyRoom', methods=['GET', 'POST'])
def viewMyRoom():
    if 'dispname' not in session:
        return redirectFromLoginTo('viewMyRoom')

    if request.method == 'POST':
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

            suiteGroupSize = len(suite_queries.getMySuiteGroup()[0])
            numPeopleInSuite = suite_queries.getNumPeopleInSuite(info)
            # print("SUITE SIZE", numPeopleInSuite, "GROUP SIZE", suiteGroupSize)
            if numPeopleInSuite != suiteGroupSize:
                dataDict = {'roomData' : [], 'suiteData' : []}
                return render_template('viewMyRoom.html', data = dataDict)
            suite_queries.setSuite(info)

    roomData = room_queries.getMyRoomDetails()
    suiteData = suite_queries.getMySuiteDetails()
    dataDict = {'roomData' : roomData, 'suiteData' : suiteData}
    return render_template('viewMyRoom.html', data = dataDict)

@app.route('/viewSuiteMembers', methods=['GET', 'POST'])
def viewSuiteMembers():
    if 'dispname' not in session:
        return redirectFromLoginTo('viewSuiteMembers')

    if request.method == 'POST':
        if 'newSuiteRepID' in request.form:
            print("NEW SUITE REP")
            info = {}
            info['emailID'] = request.form['newSuiteRepID']
            print(request.form)
            suite_queries.setSuiteRepresentative(info)
        elif 'remove' in request.form:
            print("REMOVE")
            rawinfo = request.form
            info = rawinfo.to_dict(flat=False)
            #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
            for key, value in info.items():
                info[key] = value[0]
            suite_queries.removeMyselfFromSuiteGroup()
            return redirect('/')
    # print("ID", global_vars.emailID)
    data = suite_queries.getMySuiteGroup()
    # print("DATA", data)
    numPeopleInSuite = suiteGroupSize = len(suite_queries.getMySuiteGroup()[0])
    isLastPerson = False
    isInSuiteGroup = False
    if numPeopleInSuite == 1:
        isLastPerson = True
    if numPeopleInSuite > 0:
        isInSuiteGroup = True
    return render_template('viewSuiteMembers.html', data = data, isSuiteRep = suite_queries.isCurrentUserSuiteRepresentative(), isLastPerson = isLastPerson, isInSuiteGroup = isInSuiteGroup)

@app.route('/suiteFormation', methods=['GET', 'POST'])
def suiteFormation():
    if 'dispname' not in session:
        return redirectFromLoginTo('suiteFormation')

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

    if 'dispname' not in session:
        return redirectFromLoginTo('selectionpage')

    return render_template('selectionpage.html')

def redirectFromLoginTo(url):
    ''' Helper method to save the url from which we are asked to login.

    If we decide to click a link that requires login, we save the link, login to
    the website, and go back to the url we once were
    '''
    session['prevURL'] = url
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # submitted login form
    if request.method == 'POST':

        # the login form data
        info = request.form

        # tell the user to complete all the fields
        if not (info['dispname'] and info['password']):
            return render_template('login.html',error="Please complete all fields")

        # used in login request body
        login_info = {}
        login_info['username'] = f"{info['dispname']}@pomona.edu"
        login_info['dispname'] = info['dispname']
        login_info['password'] = info['password']

        # global variable for display name
        global_vars.emailID = info['dispname']

        # session is a built in vbl that persists as long as the app is running.
        # we login using an external python script. once we login, we save the
        # cookies of the login throughout the app
        response = cas_login.main(login_info)
        if response:

            # save the username in persistent storage
            session['dispname'] = login_info['dispname']

            # redirect from the page we were previously on
            return redirect(url_for(session['prevURL']))

        # no cookies means login failed, so we open the login page again
        return render_template('login.html',error="Invalid credentials")

    # if we came from the home page, we will redirect to home page after login
    if 'prevURL' not in session:
        session['prevURL'] = 'index'
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
            buffered=True,
            auth_plugin='mysql_native_password',
            autocommit=True)

    # global_vars.cursor executes SQL commands
    global_vars.cursor = sagedormsdb.cursor()
    sagedorm_db.init_db()
    app.run(debug=True)
