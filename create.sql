/* Datatables:
    - Books:
    - Users
    - Reviews

    Each book has reviews. Each user has a review for any book. A review can only be for one book.
     */

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    duration INTEGER NOT NULL
    -- each book has a review
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    score INTEGER NOT NULL,
    review VARCHAR NOT NULL,
    book_id INTEGER REFERENCES books,
    -- a single review belongs to a single user
    user_id VARCHAR REFERENCES users
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    username VARCHAR NOT NULL,  -- Each username can only belong to one user no matter how the letters 
    password VARCHAR NOT NULL,
    review_id INTEGER REFERENCES reviews,
    UNIQUE(username) 
    -- a user has a list of reviews
);
