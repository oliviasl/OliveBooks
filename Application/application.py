import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

class DataStore():
    login_error_message = ""
    register_error_message = ""

data = DataStore()

# Set up database
engine = create_engine("postgres://yuvuibqookjtqw:d8408c98770f17233db882e8ccaf5d54146b31746f499f76123ce4815b1092a2@ec2-34-233-186-251.compute-1.amazonaws.com:5432/d5su2kprfclm6j")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():

    # Reset login and register page
    data.login_error_message = ""
    data.register_error_message = ""

    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html", message=data.register_error_message)

@app.route("/tryregister", methods=["POST"])
def tryregister():

    username = request.form.get("username")
    password = request.form.get("password")
    password_again = request.form.get("password_again")

    # Check username isn't taken
    possible_username = db.execute("SELECT username FROM users WHERE username=:username",
                                    {"username": username}).fetchone()
    if possible_username != None:
        data.register_error_message = "Username is taken."
        return redirect(url_for('register'))

    # Check username and password are not empty
    if username == "" or password == "":
        data.register_error_message = "Must enter a username and password."
        return redirect(url_for('register'))

    # Check passwords are the same
    if password != password_again:
        data.register_error_message = "Passwords must match."
        return redirect(url_for('register'))

    # Create new user
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": username, "password": password})
    db.commit()

    return redirect(url_for('index'))

@app.route("/login")
def login():
    return render_template("login.html", message=data.login_error_message)


@app.route("/trylogin", methods=["POST"])
def trylogin():

    # Check if user exists
    username = request.form.get("username")
    user = db.execute("SELECT * FROM users WHERE username=:username",
                        {"username": username}).fetchone()
    if user is None:
        data.login_error_message = "Incorrect username or password."
        return redirect(url_for('login'))

    # Check if password is correct
    password = request.form.get("password")
    if user.password != password:
        data.login_error_message = "Incorrect username or password."
        return redirect(url_for('login'))

    return redirect(url_for('index'))
