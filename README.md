# OliveBooks
A book review website.

PSQL database on Heroku tracks books, users, and reviews.
<br>
Uses Goodreads API for information on number of ratings and average rating.


Acts as an api that can be accessed with the url /api/<isbn>
<br>
Follows the JSON format:
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}

Software Used:
* PSQL database on Heroku
* Flask and flask sessions
* SQLAlchemy
* Bootstrap 4
* SASS and CSS
* HTML
* Python

Features:
* Front Page
* Register, Login, Logout
* Search Page
* Individual Book Pages
* Post reviews and display reviews from other users

Must run these commands in termimal:
export FLASK_APP=application.py
<br>
export FLASK_ENV=development

Application folder holds the actual website.
<br>
Import folder holds code for importing book information into PSQL database from a csv file.

Project 1 of CS50 Web Development
