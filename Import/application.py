import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine("postgres://yuvuibqookjtqw:d8408c98770f17233db882e8ccaf5d54146b31746f499f76123ce4815b1092a2@ec2-34-233-186-251.compute-1.amazonaws.com:5432/d5su2kprfclm6j")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
    return "hi"
