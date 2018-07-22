from flask import Flask, render_template, request, session

# __name__ is a private variable in python. If we're running an app directly (from terminal) or not ???
from src.common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = "simon"


@app.route('/')
def home_template():
    return register_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')  # www.mysite.com/api/register
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])


if __name__ == '__main__':
    app.run()
