from flask import Flask, render_template, request, redirect, session, \
        jsonify, url_for
import populate_database
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
    '''
    Rendering the home screen
    '''
    if 'dispname' in session:
        global_vars.emailID = session['dispname']
        session['hasNotChosen'] = (len(room_queries.getMyRoomDetails()[0]) == 0 and len(suite_queries.getMySuiteDetails()[0]) == 0)
        numPeopleInSuite = len(suite_queries.getMySuiteGroup()[0])
        session['isInSuiteGroup'] = (numPeopleInSuite > 0)
        return render_template('index.html')
    else:
        session['hasNotChosen'] = True
        return render_template('index.html')

@app.route('/dorms')
def dorms():
    '''
    View all dorms page
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('dorms')
    return render_template('generic.html')

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    '''
    Display wish list info
    '''
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
    '''
    Adds room to wishlist; called by each room in their POST requests
    '''

    # if not logged in
    if 'dispname' not in session:
        return redirectFromLoginTo(redirectPageIfNotLoggedIn)

    global_vars.emailID = session['dispname']
    session['hasNotChosen'] = (len(room_queries.getMyRoomDetails()[0]) == 0 and len(suite_queries.getMySuiteDetails()[0]) == 0)
    numPeopleInSuite = len(suite_queries.getMySuiteGroup()[0])
    session['isInSuiteGroup'] = (numPeopleInSuite > 0)

    info = {}
    info['dormName'] = data[0]
    info['number'] = data[1]
    wish_list_queries.addToWishList(info)
    return jsonify(user=session['dispname'])

@app.route('/smiley', methods=['GET', 'POST'])
def smiley():
    '''
    Info for Smiley dorm
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('smiley')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'smiley')

    info = {'dormName': 'Smiley'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)

    return render_template('smiley.html', data=data, sdata=sdata)

@app.route('/clark1', methods=['GET', 'POST'])
def clark1():
    '''
    Info for Clark 1 dorm
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('clark1')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'clark1')

    info = {'dormName': 'Clark-I'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('clark1.html', data=data, sdata=sdata)

@app.route('/clark5', methods=['GET', 'POST'])
def clark5():
    '''
    Info for Clark 5 dorm
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('clark5')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'clark5')

    info = {'dormName': 'Clark-V'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('clark5.html', data=data, sdata=sdata)

@app.route('/norton', methods=['GET', 'POST'])
def norton():
    '''
    Info for Norton dorm
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('norton')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'norton')

    info = {'dormName': 'Norton-Clark'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('norton.html', data=data, sdata=sdata)

@app.route('/walker', methods=['GET', 'POST'])
def walker():
    '''
    Info for Walker dorm
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('walker')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'walker')

    info = {'dormName': 'Walker'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('walker.html', data=data, sdata=sdata)

@app.route('/lawry', methods=['GET', 'POST'])
def lawry():
    '''
    Info for Lawry dorm
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('lawry')

    if request.method == 'POST':
        return addToWishListHelper(request.form['room'].split(), 'lawry')

    info = {'dormName': 'Lawry'}
    data = room_queries.getDormRoomSummaryForDorm(info)
    sdata = suite_queries.getSuiteSummaryForDorm(info)
    return render_template('lawry.html', data=data, sdata=sdata)

@app.route('/displayRoomSelectionInfo', methods=['POST'])
def displayRoomSelectionInfo():
    '''
    Display the details of the room you selected, including roommate if applicable. Gives all this
    information to the relevant jinja template
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('displayRoomSelectionInfo')

    # student selected housing
    if request.method == 'POST':
        # save all inputted data
        rawinfo = request.form

        # add to wishlist
        if 'wishlist_item' in rawinfo:
            return addToWishListHelper(rawinfo['wishlist_item'].split(), 'displayRoomSelectionInfo')

        else:
            info = rawinfo.to_dict(flat=False)
            #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
            for key, value in info.items():
                info[key] = value[0]

            data = None
            data = room_queries.searchForDormRooms(info)

            myWishList = wish_list_queries.getMyWishList()
            myWishList = [item[0] for item in myWishList]
            return render_template('displayRoomSelectionInfo.html', data=data, myWishList = myWishList)

@app.route('/displaySuiteSelectionInfo', methods=['GET', 'POST'])
def displaySuiteSelectionInfo():
    '''
    Display the details of the suite you selected. Determine whether you're the suite rep, gives all this
    information to the relevant jinja template
    '''
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
        isSuiteRep = suite_queries.isCurrentUserSuiteRepresentative()
        return render_template('displaySuiteSelectionInfo.html', data=result, isSuiteRep = isSuiteRep)
    return render_template('displaySuiteSelectionInfo.html')


@app.route('/drawUp', methods=['GET', 'POST'])
def drawUp():
    '''
    Set your roommate for selecting a double
    '''
    if request.method == 'POST':
        # the login form data
        info = request.form
        roomSelectInfo = request.form['double'].split()
        dormName = roomSelectInfo[0]
        number = roomSelectInfo[1]
        return render_template('drawUp.html', dormName = dormName, number = number)

@app.route('/viewMyRoom', methods=['GET', 'POST'])
def viewMyRoom():
    '''
    View the details of my room. If incoming POST request (from room selection page), then
    set the single/double/suite in the database for the student(s), and then render the jinja template
    with this info, or go to an error page if there's an error
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('viewMyRoom')
    if request.method == 'POST':
        info = {}

        # select single room
        if 'single' in request.form:
            roomSelectInfo = request.form['single'].split()
            info['dormName'] = roomSelectInfo[0]
            info['dormRoomNum'] = roomSelectInfo[1]
            info['roommateEID'] = None

            errorMessage = room_queries.setStudentRoom(info)
            if errorMessage != "": # i.e. there's an error message
                return render_template('errorMessage.html', errorMessage=errorMessage)
            session['hasNotChosen'] = False

        # select double room (includes 2-room doubles)
        elif 'double' in request.form:
            roomSelectInfo = request.form['double'].split()
            info['dormName'] = roomSelectInfo[0]
            info['dormRoomNum'] = roomSelectInfo[1]
            info['roommateEID'] = request.form['roommateEID']

            errorMessage = room_queries.setStudentRoom(info)
            if errorMessage != "": # i.e. there's an error message
                return render_template('errorMessage.html', errorMessage=errorMessage)
            session['hasNotChosen'] = False

        #select suite
        elif 'suite' in request.form:
            suiteSelectInfo = request.form['suite'].split()
            info['suiteID'] = suiteSelectInfo[0]
            info['emailIDSuiteRep'] = global_vars.emailID

            suiteGroupSize = len(suite_queries.getMySuiteGroup()[0])
            numPeopleInSuite = suite_queries.getNumPeopleInSuite(info)
            if numPeopleInSuite != suiteGroupSize:
                return render_template('errorMessage.html', errorMessage="ERROR: You must select a suite that has the same number of people as your suite group does!")
            session['hasNotChosen'] = False
            suite_queries.setSuite(info)

    roommateData = room_queries.getMyRoommateInfo()
    hasRoommate = False
    if len(roommateData[0]) > 0:
        hasRoommate = True
    roomData = room_queries.getMyRoomDetails()
    suiteData = suite_queries.getMySuiteDetails()
    dataDict = {'roomData' : roomData, 'suiteData' : suiteData, 'roommateData' : roommateData}

    return render_template('viewMyRoom.html', data = dataDict, hasRoommate = hasRoommate)

@app.route('/viewSuiteMembers', methods=['GET', 'POST'])
def viewSuiteMembers():
    '''
    Handles getting your suite memebers' data and injectinting it into the jinja template
    If POST request, executes the appropriate action (sets a new suite rep, or removes someone from the group)
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('viewSuiteMembers')

    if request.method == 'POST':
        if 'newSuiteRepID' in request.form:
            info = {}
            info['emailID'] = request.form['newSuiteRepID']
            errorMessage = suite_queries.setSuiteRepresentative(info)
            if errorMessage != "": # i.e. there's an error message
                return render_template('errorMessage.html', errorMessage=errorMessage)
        elif 'remove' in request.form:
            rawinfo = request.form
            info = rawinfo.to_dict(flat=False)
            #preprocess data. currently the data is a key and a list of vals. What we want is the first (and only) elem of each list
            for key, value in info.items():
                info[key] = value[0]
            suite_queries.removeMyselfFromSuiteGroup()
            session['isInSuiteGroup'] = False
            return redirect('/')

    data = suite_queries.getMySuiteGroup()
    numPeopleInSuite = len(data[0])
    isLastPerson = False
    if numPeopleInSuite == 1:
        isLastPerson = True
    isSuiteRep = suite_queries.isCurrentUserSuiteRepresentative()
    return render_template('viewSuiteMembers.html', data = data, isSuiteRep = isSuiteRep, isLastPerson = isLastPerson)

@app.route('/suiteFormation', methods=['GET', 'POST'])
def suiteFormation():
    '''
    Form a suite group and render the HTML template to view your suite group,
    or redirect to an error page if there is an error.
    '''
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
            errorMessage = suite_queries.createSuiteGroup(info)
            if errorMessage != "": # i.e. there's an error message
                return render_template('errorMessage.html', errorMessage=errorMessage)
            session['isInSuiteGroup'] = True
        elif info['inputType'] == 'existing':
            errorMessage = suite_queries.addMyselfToSuiteGroup(info)
            if errorMessage != "": # i.e. there's an error message
                return render_template('errorMessage.html', errorMessage=errorMessage)
            session['isInSuiteGroup'] = True
        return redirect('/viewSuiteMembers')
    return render_template('suiteFormation.html')

@app.route('/selectionpage', methods=['GET', 'POST'])
def selectionpage():
    '''
    Load the selection page
    '''
    if 'dispname' not in session:
        return redirectFromLoginTo('selectionpage')
    return render_template('selectionpage.html',)

def redirectFromLoginTo(url):
    ''' Helper method to save the url from which we are asked to login.

    If we decide to click a link that requires login, we save the link, login to
    the website, and go back to the url we once were
    '''
    session['prevURL'] = url
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    # if already logged in do nothing
    if 'dispname' in session:
        return redirect(url_for('index'))

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
        session['hasNotChosen'] = (len(room_queries.getMyRoomDetails()[0]) == 0 and len(suite_queries.getMySuiteDetails()[0]) == 0)
        numPeopleInSuite = len(suite_queries.getMySuiteGroup()[0])
        session['isInSuiteGroup'] = (numPeopleInSuite > 0)

        response = cas_login.main(login_info)
        if response:
            # session is a built in vbl that persists as long as the app is running.
            # we login using an external python script. once we login, we save the
            # cookies of the login throughout the app

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
    populate_database.init_db()
    app.run(debug=True)
