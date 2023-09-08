
CREATE TABLE Pastes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    modification_date TIMESTAMP NOT NULL DEFAULT current_timestamp
);

INSERT INTO pastes (title, content) VALUES ('My first paste!', 'This is my first paste.');
INSERT INTO pastes (title, content) VALUES ('Most useful tool', 'I found this mindblowing tool: console.log');
INSERT INTO pastes (title, content) VALUES ('Instructions', 'Initialize your database with ./docs/database.sh');
