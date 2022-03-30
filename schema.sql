CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player TEXT UNIQUE,
    scorewon INTEGER,
    scoreloss INTEGER,
    gamewon INTEGER,
    gameloss INTEGER,
    visible BOOLEAN
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
    tournament_id INT REFERENCES tournaments,
    game_time TIMESTAMP,
    seasonround INTEGER 
);

CREATE TABLE daystats (
    id SERIAL PRIMARY KEY,
    player TEXT,
    score INTEGER,
    game_time TIMESTAMP  
);

CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    tournament TEXT UNIQUE,
);