#Tätä käytetään pelien tekemiseen games.html kanssa
from db import db
from flask import session
import random

def get_players(players:list):
    #tarkastaa paljon valittuja pelaajia on ja sen mukaan valita kaavio tässä?
    random.shuffle(players)
    return players

        
def team_points():
    pass

