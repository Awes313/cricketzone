from flask import Flask, render_template, request

app = Flask(__name__)

users = []  # To store student data

@app.route('/')
def homePage():
    return render_template('eventPost.html')

@app.route('/StudentForm')
def studentForm():
    return render_template('view.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        student = []
        name = request.form['fname']
        email = request.form['mail']
        password = request.form['paswd']
        dob = request.form['dob']

        student.append(name)
        student.append(email)
        student.append(password)
        student.append(dob)

        users.append(student)
        return render_template('View.html', users=users)

@app.route('/ViewForm')
def view():
    return render_template('View.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
