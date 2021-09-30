CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player TEXT UNIQUE,
    scorewon INTEGER,
    scoreloss INTEGER
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    p1 TEXT,
    p1score INTEGER,
    p2 TEXT,
    p2score INTEGER,
    p3 TEXT,
    p3score INTEGER,
    p4 TEXT,
    p4score INTEGER,
    game_time TIMESTAMP  
);

CREATE TABLE stats (
    id SERIAL PRIMARY KEY,
    player TEXT,
    score INTEGER,
    game_time TIMESTAMP  
);
