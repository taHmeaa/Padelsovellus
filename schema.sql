""" Tällä hetkellä luotu vain yksi käyttäjä, jolla päästään sivulle sisään"""

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);


""" Pelaajat löytyy täältä ja valinnat tehdään tämän tietokannan kautta"""
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    player TEXT UNIQUE,
    score INTEGER
);

"""Tänne kerätään pisteet ja peli pvm """
CREATE TABLE stats (
    id SERIAL PRIMARY KEY,
    player TEXT UNIQUE,
    score INTEGER
    game_at TIMESTAMP  
);

"""
tällä saadaan tulokset
SELECT player, SUM(score) FROM stats GROUP BY player ORDER BY sum DESC;

"""