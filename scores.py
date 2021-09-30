#Tätä käytetään pelien tekemiseen games.html kanssa
from db import db
from flask import session
import random

def get_players(p:list):
    #tarkastaa paljon valittuja pelaajia on ja sen mukaan valitaan§ kaavio tässä?
    random.shuffle(p)
    #alla kaavio jotta kaikki pelaa kaikkien kanssa kaikkia vastaan
    if len(p) == 4:
        game1 = p[0], p[1], p[2], p[3]
        game2 = p[1], p[3], p[0], p[2]
        game3 = p[0], p[3], p[1], p[2]
        return (game1, game2, game3)

    if len(p) == 5:
        game1 = p[0], p[1], p[2], p[3]
        game2 = p[1], p[3], p[2], p[4]
        game3 = p[0], p[4], p[1], p[2]
        game4 = p[0], p[2], p[3], p[4]
        game5 = p[0], p[3], p[1], p[4]
        return (game1, game2, game3, game4, game5)
    if len(p) == 6:
        game1 = p[0], p[5], p[1], p[3]
        game2 = p[3], p[4], p[0], p[2]
        game3 = p[2], p[4], p[1], p[5]
        game4 = p[2], p[5], p[0], p[1]
        game5 = p[0], p[4], p[3], p[5]
        game6 = p[0], p[3], p[1], p[2]
        game7 = p[3], p[4], p[1], p[5]
        game8 = p[2], p[3], p[4], p[5]
        game9 = p[1], p[4], p[0], p[2]
        return (game1, game2, game3, game4, game5, game6, game7, game8, game9)

        
def team_points():
    pass

