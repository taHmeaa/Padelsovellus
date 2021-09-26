#Tätä käytetään pelien tekemiseen games.html kanssa
from db import db
from flask import session
import random

def get_players(players:list):
    random.shuffle(players)
    return players

        

