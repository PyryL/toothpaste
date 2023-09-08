
-- install pgcrypto module used for storing passwords
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- create tables

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE Pastes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    modification_date TIMESTAMP NOT NULL DEFAULT current_timestamp,
    owner INTEGER REFERENCES Users
);


-- test data

INSERT INTO pastes (title, content) VALUES ('My first paste!', 'This is my first paste.');
INSERT INTO pastes (title, content) VALUES ('Most useful tool', 'I found this mindblowing tool: console.log');
INSERT INTO pastes (title, content) VALUES ('Instructions', 'Initialize your database with ./docs/database.sh');

INSERT INTO users (username, password_hash) VALUES ('johndoe', crypt('secret', gen_salt('bf')));
INSERT INTO users (username, password_hash) VALUES ('janedoe', crypt('password', gen_salt('bf')));
