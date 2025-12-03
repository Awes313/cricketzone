from flask import Flask, render_template, request

app = Flask(__name__)

registrations = []

@app.route('/')
def index():
    return render_template('event.html', registrations=registrations)

@app.route('/register', methods=['GET'])
def register():
    fullname = request.args.get('fullname')
    email = request.args.get('email')
    phone = request.args.get('phone')
    event_type = request.args.get('event_type')
    comments = request.args.get('comments')

    if fullname and email and phone and event_type:
        data = [fullname, email, phone, event_type, comments]
        registrations.append(data)

    return render_template('event.html', registrations=registrations)

if __name__ == "__main__":
    app.run(debug=True)
