CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT, 
    role INTEGER);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    visible INTEGER
    );

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    scores INTEGER,
    review TEXT,
    visible INTEGER
    );