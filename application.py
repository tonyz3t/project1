import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from models import *

app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = db.execute("SELECT username, password FROM users")
API_KEY = "cps1I4JFH7gAxOfBtP46tQ"

@app.route("/")
# Our start of the Website
# We will have the user log in with an option to signup
# This page will only have two buttons:
#   one to sign up and one to register
# Users will then be sent to respective pages
def welcome():
    return render_template("welcome.html")

# Website Login Page
# User must submit a valid username and password
@app.route("/login", methods=["GET", "POST"])
def login():    
    # on get method we return the login page if the website does not remember the user
    
    if request.method == "GET":
        try:   
            if session["USERNAME"] is None:
                return render_template("login.html")
            else:
                return redirect(url_for("home"))
        except:
            return render_template("login.html")
    
    # Once user submits the login page, we want to get all the information and log the user in
    # take the user name and password from the form
    if request.method == "POST":
        #return render_template("error.html", message="its here now", users=users)

        # PROCESS USER INFORMATION
        # Gather our list of users    
        username = request.form.get("username")
        password = request.form.get("password")

        #find our user in our database
        current_user = db.execute("SELECT id, username, password FROM users WHERE LOWER(username) = LOWER(:username)  AND password = :password",
                                    {"username": username, "password": password}).fetchone()

        # If the Username is not found, notify user and keep at login page
        if current_user is None:
            return render_template("login.html", message="Username or Password is incorrect, please try again")
        # else set current user to the username
        else:
            session["USERNAME"] = current_user.username
            session["USER_ID"] = current_user.id    
            return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register(): 
    if request.method == "GET":
        try:   
            if session["USERNAME"] is None:
                return render_template("registration.html")
            else:
                return redirect(url_for("home"))
        except:
            return render_template("registration.html")
    
    if request.method == "POST":
        # handle registering the user here
        # Gather our users info from registration sheet
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        #Insert into our database
        # TODO: handle error exception when an username that exists in the datatable is added to a new user
        db.execute("INSERT INTO users (name, email, username, password) VALUES (:name, LOWER(:email), :username, :password)",
                {"name": name, "email": email, "username": username, "password":password})
        db.commit()

        session["USERNAME"] = username

        # Send user to the home page
        return redirect(url_for('home'))


@app.route("/home", methods=["GET", "POST"])
def home():
    
    if session["USERNAME"] is None:
        return redirect(url_for("login"))

    # If method is POST, indicates user is searching for a book
    if request.method == "POST":

        # Retrieve our search query from our form
        search = request.form.get("search")
        # We add % to the front and back of our search to query through our database for items containing part of the users search
        my_search = "%" + search + "%"
        # Retrieve a list of all the books with making query
        # ILIKE is a case insensitive conditional
        books = db.execute("SELECT * FROM books WHERE isbn ILIKE :search OR title ILIKE :search OR author ILIKE :search LIMIT 50",
                                    {"search": my_search})

        # Return the home page with our list of books relating to user search
        return render_template("home.html", books=books)

    return render_template("home.html")

# Here we will handle the user signing out
@app.route("/sign-out", methods=["GET"])
def signout():
    # delete the session
    session["USERNAME"] = None
    session["USER_ID"] = None
    # redirect our user back to the login page\
    return redirect(url_for("login"))

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):

    # Get our book from our book database
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    # throw an error if the book doesnt exist
    if book is None:
        return render_template("error.html", message="book DNE")
    
    # Show reviews
    reviews = db.execute("SELECT score, review From reviews WHERE book_id = :book_id", {"book_id": book.id}).fetchall()

    # Gather review statistics from goodreads
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": API_KEY, "isbns": isbn})
    if res.status_code != 200:
        return render_template("error.html", message="api request unsuccessful")
    data = res.json()
    average_score = data["books"][0]["average_rating"]
    review_count = data["books"][0]["reviews_count"]

    # Submit user review
    if request.method == "POST":
        user_review = request.form.get("user_review")
        user_score = request.form.get("user_score")
        user_id = session["USER_ID"]

        #insert the review into the databse
        db.execute("INSERT INTO reviews (score, review, book_id, user_id) VALUES(:score, :review, :book_id, :user_id)",
                    {"score": user_score, "review": user_review, "book_id": book.id, "user_id": user_id})
        db.commit()

    return render_template("book.html", book=book, reviews=reviews, data=data, average_score=average_score, review_count=review_count)

@app.route("/books")
def books():
    # List all the books

    books = db.execute("SELECT * FROM books")
    
    return render_template("books.html", books=books)
    #books = Book.query.all()
    #return render_template
    pass

@app.route("/about")
def about():
    # return the about page
    return render_template("about.html")

# TODO: API ACCESS  
@app.route("/api/<string:isbn>")
def book_api(isbn):
    # gather book data from database
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    # Gather review statistics from goodreads
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": API_KEY, "isbns": isbn})
    if res.status_code != 200:
        return render_template("error.html", message="api request unsuccessful")
    data = res.json()
    average_score = data["books"][0]["average_rating"]
    review_count = data["books"][0]["reviews_count"]

    # JSONify the information
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": review_count,
        "average_score": average_score
    })

