from re import S
from sqlalchemy.orm import query
from werkzeug.wrappers import request
from db import db
from flask import session


def results(game_player:list,game_result:list):
    #lisätään peli pelitaulukkoon
    sql = """INSERT INTO games (p1, p1score, p2, p2score, p3, p3score, p4, p4score) 
               VALUES (:p1, :p1score, :p2, :p2score, :p3, :p3score, :p4, :p4score);"""
    s = 0 #tuloksen kerroin
    for i in range(0, len(game_player), 4): #4 stepeissä   
        db.session.execute(sql, {"p1": game_player[0+i], "p1score": int(game_result[0+s]),
                                "p2": game_player[1+i], "p2score": int(game_result[0+s]),
                                "p3": game_player[2+i], "p3score": int(game_result[1+s]),
                                "p4": game_player[3+i], "p4score": int(game_result[1+s])})
        s += 2
        db.session.commit()    
    return 

def playerstats(players:list, points:list):
    #päivitetään pelaajan tilastot

    sql = """ UPDATE players SET scorewon = scorewon + :w, scoreloss = scoreloss + :l 
                WHERE player = :player """
    #kaaviossa vaseamman puolen joukkueen pisteet
    l = 0 
    for i in range(0, len(players), 4) :
        db.session.execute(sql, {"w":int(points[l]), "l":int(points[1+l]), "player":players[i],})
        db.session.execute(sql, {"w":int(points[l]), "l":int(points[1+l]), "player":players[i+1],})
        db.session.commit()
        l += 2
    #kaavion oikean puolen joukkueen pisteet
    r = 0 
    for i in range(2, len(players), 4) :
        db.session.execute(sql, {"w":int(points[r+1]), "l":int(points[r]), "player":players[i],})
        db.session.execute(sql, {"w":int(points[r+1]), "l":int(points[r]), "player":players[i+1],})
        db.session.commit()
        r += 2
    return

def gameday_stats():
    sql = "SELECT player, SUM(score) FROM stats GROUP BY player ORDER BY sum DESC;"
    result = db.session.execute(sql)
    gameday_podium = result.fetchall()
    return gameday_podium

def season_stats():
    sql = "SELECT player, scorewon FROM players ORDER BY scorewon DESC;"
    result = db.session.execute(sql)
    podium = result.fetchall()
    return podium