#Tätä käytetään pelien tekemiseen games.html kanssa
from db import db
from flask import session
import random

def get_players(p:list):
    #tarkastaa paljon valittuja pelaajia on ja sen mukaan valitaan§ kaavio tässä?
    random.shuffle(p)
    #alla kaavio jotta kaikki pelaa kaikkien kanssa kaikkia vastaan
    #viimeinen on pelin/joukkue tunniste, joka siirretään html
    game1 = p[0], p[1], p[2], p[3], "T1", "T2"
    game2 = p[1], p[3], p[2], p[4], "T3", "T4"
    game3 = p[0], p[4], p[1], p[2], "T5", "T6"
    game4 = p[0], p[2], p[3], p[4], "T7", "T8"
    game5 = p[0], p[3], p[1], p[4], "T9", "T10"
    return (game1, game2, game3, game4, game5)

        
def team_points():
    pass

