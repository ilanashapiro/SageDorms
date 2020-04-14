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

    loggedIn = False
    if 'cookies' in session and session['cookies']:
        print(session['cookies'])
        loggedIn = True
    return render_template('index.html', loggedIn=loggedIn)

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
        info = request.form

        # not used in CAS login form but rather for ourselves
        user_info = {}
        user_info['school'] = info['school']
        user_info['sid'] = info['sid']

        # used in login
        login_info = {}
        login_info['username'] = f"{info['dispname']}@{info['school']}.edu"
        login_info['dispname'] = info['dispname']
        login_info['password'] = info['password']

        # session is a built in vbl that persists as long as the app is running
        # login using an external python script. once we login, we save the
        # cookies of the login throughout the app
        session['cookies'] = cas_login.main(login_info)
        return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
