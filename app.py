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

        # initialize mysql server and database
        sagedorm_db.main('u', studInfo)
        return redirect('/students')

    return render_template('index.html')

@app.route('/students')
def students():
    students = sagedorm_db.main('r')
    return render_template('students.html', students=students)

@app.route('/dorms')
def view_dorms():
    return render_template('generic.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)

