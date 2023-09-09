
-- install pgcrypto module used for storing passwords
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- create tables

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TYPE Publicity AS ENUM ('listed', 'private');

CREATE TABLE Pastes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    modification_date TIMESTAMP NOT NULL DEFAULT current_timestamp,
    owner INTEGER REFERENCES Users,
    publicity Publicity NOT NULL
);
