/* Datatables:
    - Books:
    - Users
    - Reviews

    Each book has reviews. Each user has a review for any book. A review can only be for one book.
     */

-- CREATE TABLE books (
--     id SERIAL PRIMARY KEY,
--     isbn VARCHAR NOT NULL,
--     title VARCHAR NOT NULL,
--     author VARCHAR NOT NULL,
--     year INTEGER NOT NULL
--     -- each book has a review
-- );

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    username VARCHAR NOT NULL,  -- Each username can only belong to one user no matter how the letters 
    password VARCHAR NOT NULL,
    UNIQUE(username) 
    -- a user has a list of reviews
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    score INTEGER NOT NULL,
    review VARCHAR NOT NULL,
    book_id INTEGER NOT NULL REFERENCES books,
    -- a single review belongs to a single user
    user_id INTEGER REFERENCES users
);


/* Connect data tables to each other
each userr should have a list of reviews
each review belongs to a book and a user */

