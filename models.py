import os

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
    
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Our Book object class used to represent a book contains:
#   id = a serialized integer given to each book to represent its id
#   isbn, title, author, year of book
class Book(db.Model):
    db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL);")

    # Same table as above using sqlalchemy orm
    """ __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False) """

# Our User object class used to represent a user of the website
class User(db.Model):
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, email VARCHAR NOT NULL, username VARCHAR NOT NULL, password VARCHAR NOT NULL);")
    db.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Our Review object class used to represent a review of a given book
class Review(db.Model):
    pass