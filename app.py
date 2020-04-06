from flask import Flask, render_template, request, redirect
import sagedorm_db
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # student selected housing
    if request.method == 'POST':

        # save all inputted data
        student = request.form
        name = student['name'].split(" ") #TODO: name does nothing for us rn
        studInfo = {}
        studInfo['fname'] = name[0]
        studInfo['lname'] = name[1]
        studInfo['sid'] = int(student['sid'])
        studInfo['dormName'] = student['dormName']
        studInfo['dormRoom'] = random.randint(1, 999)

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
        # roomInfo['connectingRoomNum'] = .....
        # roomInfo['floorNum'] = .....
        # roomInfo['squareFeet'] = .....
        # roomInfo['isSubFree'] = .....
        # roomInfo['isReservedForSponsorGroup'] = .....
        # roomInfo['windowType'] = .....
        # roomInfo['isSuite'] = .....

        # initialize mysql server and database
        sagedorm_db.main('u', studInfo)
        return redirect('/students')

    return render_template('index.html')

@app.route('/students')
def students():
    students = sagedorm_db.main('r')
    return render_template('students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
