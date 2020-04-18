from flask import Flask, render_template, request, redirect, session
import sagedorm_db
import random
import cas_login

app = Flask(__name__)
app.secret_key = "shhhhh keep it a secret"

@app.route('/', methods=['GET', 'POST'])
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
        # prospectiveSuiteGroupInfo = {}
        # prospectiveSuiteGroupInfo['sid2'] = .....
        # prospectiveSuiteGroupInfo['sid3'] = ...
        # prospectiveSuiteGroupInfo['sid4'] = ...
        # prospectiveSuiteGroupInfo['sid5'] = ...
        # prospectiveSuiteGroupInfo['sid6'] = ...

        # initialize mysql server and database
        sagedorm_db.main('u', studInfo)
    loggedIn = False
    if 'cookies' in session:
        print(session['cookies'])
        loggedIn = True
    return render_template('index.html', loggedIn=loggedIn)
>>>>>>> 0ca78c1c9e87b7d5e0457c13b786c800f378840f

@app.route('/students')
def students():
    students = sagedorm_db.main('r')
    return render_template('students.html', students=students)

@app.route('/dorms')
def dorms():
    return render_template('generic.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # submitted login form
    if request.method == 'POST':

        # the login form data
        info = request.form

        # used in login request body
        login_info = {}
        login_info['username'] = f"{info['dispname']}@{info['school']}.edu"
        login_info['dispname'] = info['dispname']
        login_info['password'] = info['password']

        # session is a built in vbl that persists as long as the app is running.
        # we login using an external python script. once we login, we save the
        # cookies of the login throughout the app
        cookies = cas_login.main(login_info)
        if cookies:
            session['cookies'] = cookies
            session['school'] = info['school']
            session['sid'] = info['sid']
            return redirect('/')

        # no cookies means login failed, so we open the login page again
        return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
