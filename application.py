import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#from models import *

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
        if session["USERNAME"] is None:
            return render_template("login.html", message="")
        else:
            return redirect(url_for("home"))
        
    
    # Once user submits the login page, we want to get all the information and log the user in
    # take the user name and password from the form
    if request.method == "POST":
        #return render_template("error.html", message="its here now", users=users)

        # PROCESS USER INFORMATION
        # Gather our list of users    
        username = request.form.get("username")
        password = request.form.get("password")

        #find our user in our database
        current_user = db.execute("SELECT username, password FROM users WHERE username = :username AND password = :password",
                                    {"username": username, "password": password}).fetchone()

        # If the Username is not found, notify user and keep at login page
        if current_user is None:
            return render_template("login.html", message="Username or Password is incorrect, please try again")
        # else set current user to the username
        else:
            session["USERNAME"] = current_user.username    
            return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register(): 
    if request.method == "GET":
        if session["USERNAME"] is None:
            return render_template("registration.html")
        else:
            return redirect(url_for("home"))
    
    if request.method == "POST":
        # handle registering the user here
        # Gather our users info from registration sheet
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        #Insert into our database
        db.execute("INSERT INTO users (name, email, username, password) VALUES (:name, :email, :username, :password)",
                {"name": name, "email": email, "username": username, "password":password})
        db.commit()

        # Render the loading page
        return home()


@app.route("/home", methods=["GET", "POST"])
def home():
    # TODO: Handle users registration information here?
    #REGISTRATION HANDLING
    if request.method == "GET":
        if session["USERNAME"] is None:
            return redirect(url_for("login"))
        else:
            pass

    users = db.execute("SELECT username, password FROM users")


    return render_template("home.html", users=users)

# Here we will handle the user signing out
@app.route("/sign-out", methods=["GET"])
def signout():
    # delete the session
    session["USERNAME"] = None
    # redirect our user back to the login page\
    return redirect(url_for("login"))

# TODO: Allow the user to search through our books
# TODO: When a book is selected, print dialog with book's details
# TODO: display the average book ratings retrieved from GoodReads
# TODO: Allow the user to write a review for a book
# TODO: create data tables to store user reviews
# TODO: connect our books, users, and reviews tables somehow

@app.route("/books")
def books():
    # List all the books
    #books = Book.query.all()
    #return render_template
    pass

