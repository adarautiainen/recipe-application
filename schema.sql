CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT, 
    admin BOOLEAN);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users
    );

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    review TEXT
    user_id INTEGER REFERENCES users,
    visible BOOLEAN);