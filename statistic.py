from re import S
from sqlalchemy.orm import query
from werkzeug.wrappers import request
from db import db
from flask import session
import datetime


def results(game_player:list,game_result:list, t_id:int):
    #lisätään peli games-taulukkoon
    sql = """INSERT INTO games (p1, p1score, p2, p2score, p3, p3score, p4, p4score, tournament_id, game_time ) 
               VALUES (:p1, :p1score, :p2, :p2score, :p3, :p3score, :p4, :p4score, :tournament_id, NOW());"""
    s = 0 #tuloksen kerroin
    for i in range(0, len(game_player), 4): #4 stepeissä   
        db.session.execute(sql, {"p1": game_player[0+i], "p1score": int(game_result[0+s]),
                                "p2": game_player[1+i], "p2score": int(game_result[0+s]),
                                "p3": game_player[2+i], "p3score": int(game_result[1+s]),
                                "p4": game_player[3+i], "p4score": int(game_result[1+s]),
                                "tournament_id": t_id})
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
    #päivitetään pelaajan kausitilastot
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

def americano_stats(t_id):
    try:
        sql = """SELECT p1, p1score, p2, p2score, p3, p3score, p4, p4score, tournament FROM games, tournaments 
            WHERE tournament_id = tournaments.id AND tournaments.id=:t_id"""
        result = db.session.execute(sql, {"t_id":t_id,})
        games = result.fetchall()
        #lisätään päivän tulokset daystats-tauluun ja nollataan taulu. Tähän joku fiksumpi ratkaisu...
        db.session.execute("DROP TABLE daystats;")
        db.session.execute("""CREATE TABLE daystats (id SERIAL PRIMARY KEY, player TEXT,
                            score INTEGER, game_time TIMESTAMP);""")
        db.session.commit()

        sql2 = "INSERT INTO daystats (player, score, game_time) VALUES (:player, :score, NOW())"
        for g in games:
            db.session.execute(sql2, {"player":g[0], "score":g[1]})
            db.session.execute(sql2, {"player":g[2], "score":g[3]})
            db.session.execute(sql2, {"player":g[4], "score":g[5]})
            db.session.execute(sql2, {"player":g[6], "score":g[7]})
            db.session.commit()        
    except:
        return False
    return games

def tournament(name):
    try:
        sql = "INSERT INTO tournaments (tournament) VALUES (:name);"
        db.session.execute(sql, {"name":name,})
        db.session.commit()
    except:
        return False
    return True
    
def tournament_id(name):
    sql = "SELECT id FROM tournaments WHERE tournament =:name;"
    result = db.session.execute(sql, {"name":name,})
    id = result.fetchone()
    return id

def get_tournaments():
    sql = "SELECT * FROM tournaments WHERE id !=1;"
    result = db.session.execute(sql)
    tournaments = result.fetchall()
    return tournaments

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
    try:
        sql = "SELECT game_time FROM games ORDER BY game_time DESC;"
        prev = db.session.execute(sql)
        gameday = prev.fetchone()
        day = gameday[0].strftime("%Y-%m-%d")
    except:
        return False
    return day