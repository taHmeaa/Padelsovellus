from re import S
from sqlalchemy.orm import query
from werkzeug.wrappers import request
from db import db
from flask import session
import datetime


def results(game_player:list,game_result:list):
    #lisätään peli games-taulukkoon
    sql = """INSERT INTO games (p1, p1score, p2, p2score, p3, p3score, p4, p4score, game_time ) 
               VALUES (:p1, :p1score, :p2, :p2score, :p3, :p3score, :p4, :p4score, NOW());"""
    s = 0 #tuloksen kerroin
    for i in range(0, len(game_player), 4): #4 stepeissä   
        db.session.execute(sql, {"p1": game_player[0+i], "p1score": int(game_result[0+s]),
                                "p2": game_player[1+i], "p2score": int(game_result[0+s]),
                                "p3": game_player[2+i], "p3score": int(game_result[1+s]),
                                "p4": game_player[3+i], "p4score": int(game_result[1+s])})
        s += 2
        db.session.commit()
    #lisätään päivän tulokset daystats-tauluun ja nollataan taulu. Tähän joku fiksumpi ratkaisu...
    db.session.execute("DROP TABLE daystats;")
    db.session.execute("""CREATE TABLE daystats (id SERIAL PRIMARY KEY, player TEXT,
                         score INTEGER, game_time TIMESTAMP);""")
    db.session.commit()

    sql2 = "INSERT INTO daystats (player, score, game_time) VALUES (:player, :score, NOW())"
    g = 0 #tuloksen kerroin
    for p in range(0, len(game_player), 2):
        db.session.execute(sql2, {"player":game_player[0+p], "score":int(game_result[0+g])})
        db.session.execute(sql2, {"player":game_player[1+p], "score":int(game_result[0+g])})
        g +=1
        db.session.commit()        
    return 

def playerstats(players:list, points:list):
    #päivitetään pelaajan tilastot
    sql = """ UPDATE players SET scorewon = scorewon + :w, scoreloss = scoreloss + :l 
                WHERE player = :player """
    #kaaviossa vaseamman puolen joukkueen pisteet
    l = 0 
    for i in range(0, len(players), 4):
        db.session.execute(sql, {"w":int(points[l]), "l":int(points[1+l]), "player":players[i],})
        db.session.execute(sql, {"w":int(points[l]), "l":int(points[1+l]), "player":players[i+1],})
        db.session.commit()
        l += 2
    #kaavion oikean puolen joukkueen pisteet
    r = 0 
    for i in range(2, len(players), 4):
        db.session.execute(sql, {"w":int(points[r+1]), "l":int(points[r]), "player":players[i],})
        db.session.execute(sql, {"w":int(points[r+1]), "l":int(points[r]), "player":players[i+1],})
        db.session.commit()
        r += 2
    #Pelivoitot / Pelihäviöt
    sql2 = """ UPDATE players SET gamewon = gamewon + :gw, gameloss = gameloss +:gl
            Where player = :player """
    l = 0
    for i in range(0, len(players), 4):
        if int(points[l]) > int(points[1+l]):
            db.session.execute(sql2, {"gw":1, "gl":0, "player": players[i],})
            db.session.execute(sql2, {"gw":1, "gl":0, "player": players[i+1],})
            db.session.commit()
        if int(points[l]) < int(points[1+l]):
            db.session.execute(sql2, {"gw":0, "gl":1, "player": players[i],})
            db.session.execute(sql2, {"gw":0, "gl":1,"player": players[i+1],})
            db.session.commit()
        l +=2
    r = 0 
    for i in range(2, len(players), 4):
        if int(points[r]) > int(points[r+1]):
            db.session.execute(sql2, {"gw":0, "gl":1, "player": players[i],})
            db.session.execute(sql2, {"gw":0, "gl":1, "player": players[i+1],})
            db.session.commit()
        if int(points[r]) < int(points[r+1]):
            db.session.execute(sql2, {"gw":1, "gl":0, "player": players[i],})
            db.session.execute(sql2, {"gw":1, "gl":0,"player": players[i+1],})
            db.session.commit()
        r += 2
    return

def gameday_stats():
    sql = "SELECT player, SUM(score) FROM daystats GROUP BY player ORDER BY sum DESC;"
    result = db.session.execute(sql)
    gameday_podium = result.fetchall()
    return gameday_podium

def season_stats():
    sql = "SELECT player, scorewon, scoreloss, gamewon, gameloss FROM players ORDER BY scorewon DESC;"
    result = db.session.execute(sql)
    podium = result.fetchall()
    return podium

def getgames(date):
    try:
        sql = """SELECT game_time, p1 , p2, p1score, p3, p4, p3score FROM games 
                WHERE game_time::date=:gameday ORDER BY game_time DESC;"""
        result = db.session.execute(sql, {"gameday":date,})
        games = result.fetchall()
    except:
        return False
    return games

def prevgameday():
    sql = "SELECT game_time FROM games ORDER BY game_time DESC;"
    prev = db.session.execute(sql)
    gameday = prev.fetchone()
    day = gameday[0].strftime("%Y-%m-%d")
    return day