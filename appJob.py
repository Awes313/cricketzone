from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

applicants = []

@app.route('/')
def home():
    return render_template('jobApplication.html', msg=None)

@app.route('/apply', methods=['POST'])
def apply():
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    institution = request.form['institution']
    degree = request.form['degree']
    skills = request.form['skills']

    applicants.append([fullname, email, phone, institution, degree, skills])
    msg = "✅ Application submitted successfully!"
    return render_template('jobApplication.html', msg=msg)

@app.route('/viewApplicants')
def viewApplicants():
    return render_template('viewApplicants.html', applicants=applicants)

if __name__ == '__main__':
    app.run(debug=True)
