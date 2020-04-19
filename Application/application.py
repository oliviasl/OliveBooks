import os
import requests

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
    user = None;

data = DataStore()


# Set up database
engine = create_engine("postgres://yuvuibqookjtqw:d8408c98770f17233db882e8ccaf5d54146b31746f499f76123ce4815b1092a2@ec2-34-233-186-251.compute-1.amazonaws.com:5432/d5su2kprfclm6j")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():

    # Reset login and register page
    data.login_error_message = ""
    data.register_error_message = ""
    session.pop('username', None)

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

    data.user = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username}).fetchone()
    session['username'] = username
    return redirect(url_for('search'))

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

    data.user = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username}).fetchone()
    session['username'] = username
    return redirect(url_for('search'))

@app.route("/search", methods=["GET", "POST"])
def search():

    if request.method == 'POST':
        searchinfo = request.form.get("searchinfo")
        newsearch = '%' + searchinfo + '%'
        searchby = request.form.get("searchby")

        if searchby == "ISBN":
            booksfound = db.execute("SELECT * FROM books WHERE ISBN LIKE :searchinfo",
                                    {"searchinfo": newsearch}).fetchall()
        elif searchby == "title":
            booksfound = db.execute("SELECT * FROM books WHERE title LIKE :searchinfo",
                                    {"searchinfo": newsearch}).fetchall()
        elif searchby == "author":
            booksfound = db.execute("SELECT * FROM books WHERE author LIKE :searchinfo",
                                    {"searchinfo": newsearch}).fetchall()
        else:
            booksfound = []

        return render_template("search.html", searchinfo=searchinfo, searchby=searchby, booksfound=booksfound, username=session['username'])

    return render_template("search.html", searchinfo="", searchby="", booksfound=[], username=session['username'])


@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):

    book = db.execute("SELECT * FROM books WHERE id = :id",
                        {"id": book_id}).fetchone()

    # Check book exists
    if book is None:
        return render_template("error.html", message="No such book exists.")

    # Get API book information
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "CP5fhQDJPfEjhox0sGg", "isbns": book.isbn})
    if res.status_code != 200:
        raise Exception("API request unsuccessful.")
    book_data = res.json()
    total_ratings = book_data["books"][0]["work_ratings_count"]
    average_rating = book_data["books"][0]["average_rating"]

    # List of reviews
    reviewslist = db.execute("SELECT * FROM reviews WHERE book_id = :id",
                        {"id": book_id}).fetchall()
    usernameslist = []
    for post in reviewslist:
        user = db.execute("SELECT username FROM users WHERE id = :id",
                        {"id": post.user_id}).fetchone()
        usernameslist.append(user)

    # Check if review exists
    review = db.execute("SELECT * FROM reviews WHERE user_id = :user_id and book_id = :book_id",
                        {"user_id": data.user.id, "book_id": book_id}).fetchone()
    if review == None:
        return render_template("book.html", book=book, total_ratings=total_ratings, average_rating=average_rating, rating=None, review=None, username=session['username'], reviewslist=reviewslist, usernameslist=usernameslist)

    return render_template("book.html", book=book, total_ratings=total_ratings, average_rating=average_rating, rating=review.rating, review=review.review, username=session['username'], reviewslist=reviewslist, usernameslist=usernameslist)


@app.route("/processreview", methods=["POST"])
def processreview():

    # Get rating and review
    rating = request.form.get("rating")
    review = request.form.get("review")
    book_id = request.form.get("book_id")

    print(book_id)

    # Add review to reviews database
    db.execute("INSERT INTO reviews (rating, review, user_id, book_id) VALUES (:rating, :review, :user_id, :book_id)",
                {"rating": rating, "review": review, "user_id": data.user.id, "book_id": book_id})
    db.commit()

    return redirect(url_for('book', book_id=book_id))
