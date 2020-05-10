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

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
# Our start of the Website
# We will have the user log in with an option to signup
# This page will only have two buttons:
#   one to sign up and one to register
# Users will then be sent to respective pages
def welcome():
    return render_template("welcome.html")

@app.route("/login")
def login():
    # # take the user name and password from the form
    # if request.method == "POST":
        
    #     req = request.form

    #     username = req.get("username")
    #     password = req.get("password")

    #     if not username in User:
    #         #TODO
    #         return render_template("error.html", message="Invalid Username or Password, go back and try again")
    #         pass
    #     elif not password in User:
    #         # TODO: send error message incorrect password
    #         return render_template("error.html", message="Incorrect Username or Password, go back and try again")


    # Return the Log in page    
    return render_template("login.html")



@app.route("/register")
def register(): 
    return render_template("registration.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    # TODO: Handle users registration information here?
    #REGISTRATION HANDLING
    users = db.execute("SELECT username, password FROM users")

    return render_template("error.html", message="shit", users=users)

    """ if request.method == "GET":
        return login()
    else:    
        return render_template("error.html", message="SIGNED IN BUT USER N PASS HAVE NOT BEEN SAVED INTO DATABASE")
    pass """

@app.route("/books")
def books():
    # List all the books
    #books = Book.query.all()
    #return render_template
    pass

