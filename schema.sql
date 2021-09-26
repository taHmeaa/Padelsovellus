CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player TEXT UNIQUE,
    score INTEGER
);

CREATE TABLE stats (
    id SERIAL PRIMARY KEY,
    player TEXT,
    score INTEGER,
    game_at TIMESTAMP  
);
