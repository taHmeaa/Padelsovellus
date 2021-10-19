#Tätä käytetään pelien tekemiseen games.html kanssa
from db import db
from flask import session
import random

def get_brackets(p:list, t:bool):
    #tarkastaa paljon valittuja pelaajia on ja sen mukaan valitaan§ kaavio tässä?
    if t == True:
        random.shuffle(p)
    #alla kaaviot
    if len(p) == 4:
        game1 = [p[0], p[1], p[2], p[3]]
        game2 = [p[1], p[3], p[0], p[2]]
        game3 = [p[0], p[3], p[1], p[2]]
        return [game1, game2, game3]

    if len(p) == 5:
        game1 = [p[0], p[1], p[2], p[3]]
        game2 = [p[1], p[3], p[2], p[4]]
        game3 = [p[0], p[4], p[1], p[2]]
        game4 = [p[0], p[2], p[3], p[4]]
        game5 = [p[0], p[3], p[1], p[4]]
        return [game1, game2, game3, game4, game5]
    if len(p) == 6:
        game1 = [p[0], p[5], p[1], p[3]]
        game2 = [p[3], p[4], p[0], p[2]]
        game3 = [p[2], p[4], p[1], p[5]]
        game4 = [p[2], p[5], p[0], p[1]]
        game5 = [p[0], p[4], p[3], p[5]]
        game6 = [p[0], p[3], p[1], p[2]]
        game7 = [p[3], p[4], p[1], p[5]]
        game8 = [p[2], p[3], p[4], p[5]]
        game9 = [p[1], p[4], p[0], p[2]]
        return [game1, game2, game3, game4, game5, game6, game7, game8, game9]

def americanobracket(p:list):
    random.shuffle(p)
    game1 = [p[0], p[1], p[2], p[3]]
    game2 = [p[4], p[5], p[6], p[7]]
    game3 = [p[0], p[2], p[4], p[6]]
    game4 = [p[1], p[3], p[5], p[7]]
    game5 = [p[1], p[2], p[5], p[6]]
    game6 = [p[0], p[3], p[4], p[7]]
    game7 = [p[0], p[4], p[1], p[5]]
    game8 = [p[2], p[6], p[3], p[7]]
    game9 = [p[1], p[4], p[3], p[6]]
    game10 = [p[0], p[5], p[2], p[7]]
    game11 = [p[1], p[7], p[2], p[4]]
    game12 = [p[0], p[6], p[3], p[5]]
    game13 = [p[2], p[5], p[3], p[4]]
    game14 = [p[0], p[7], p[1], p[6]]
    return [game1, game2, game3, game4, game5, game6, game7, game8, game9, game10, game11, game12, game13, game14]

def get_players():
    sql = "SELECT player FROM Players WHERE visible = TRUE ORDER BY player;"
    result = db.session.execute(sql)
    players = result.fetchall()
    return players

