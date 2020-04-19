# OliveBooks
A book review website that allows users to view book reviews and post their own reviews. Uses the Goodreads API for information on a wider range of users.

### API Usage
Acts as an api that can be accessed with the url: /api/<isbn>
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

### Software Used:
* PSQL database on Heroku
* Flask and flask sessions
* SQLAlchemy
* Bootstrap 4
* SASS and CSS
* HTML
* Python

### Features:
* Front Page
* Register, Login, Logout
* Search Page
* Individual Book Pages
* Post reviews and display reviews from other users

### Must run these commands in termimal:
export FLASK_APP=application.py
<br>
export FLASK_ENV=development

### Note
Application folder holds the actual website.
<br>
Import folder holds code for importing book information into PSQL database from a csv file.

Project 1 of CS50 Web Development
