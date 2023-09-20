
-- install pgcrypto module used for storing passwords
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- create tables

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    totpSecret TEXT DEFAULT NULL
);

CREATE TYPE Publicity AS ENUM ('listed', 'unlisted', 'private');

CREATE TABLE Pastes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    modification_date TIMESTAMP NOT NULL DEFAULT current_timestamp,
    owner INTEGER REFERENCES Users,
    publicity Publicity NOT NULL,
    is_encrypted BOOLEAN NOT NULL
);

CREATE TYPE TokenLevel AS ENUM ('view', 'modify');

CREATE TABLE Tokens (
    id SERIAL PRIMARY KEY,
    token TEXT UNIQUE NOT NULL,
    paste INTEGER REFERENCES Pastes NOT NULL,
    level TokenLevel NOT NULL
);

CREATE TABLE ChatMessages (
    id SERIAL PRIMARY KEY,
    paste INTEGER REFERENCES Pastes NOT NULL,
    creator INTEGER REFERENCES Users,
    content TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE Votes (
    id SERIAL PRIMARY KEY,
    paste INTEGER REFERENCES Pastes NOT NULL,
    voter INTEGER REFERENCES Users NOT NULL,
    is_upvote BOOLEAN NOT NULL
);
