#from re import S
from sqlalchemy.orm import query
from werkzeug.wrappers import request
from db import db
from flask import session
import datetime


def results(game_player:list,game_result:list, t_id:int, s_round:int):
    #lisätään peli games-taulukkoon
    sql = """INSERT INTO games (p1, p1score, p2, p2score, p3, p3score, p4, p4score, tournament_id, game_time, seasonround) 
               VALUES (:p1, :p1score, :p2, :p2score, :p3, :p3score, :p4, :p4score, :tournament_id, NOW(), :seasonround);"""
    s = 0 #tuloksen kerroin
    for i in range(0, len(game_player), 4): #4 stepeissä   
        db.session.execute(sql, {"p1": game_player[0+i], "p1score": int(game_result[0+s]),
                                "p2": game_player[1+i], "p2score": int(game_result[0+s]),
                                "p3": game_player[2+i], "p3score": int(game_result[1+s]),
                                "p4": game_player[3+i], "p4score": int(game_result[1+s]),
                                "tournament_id": t_id, "seasonround": s_round})
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

#def newseason():
#    db.session.execute("""SELECT * INTO players22 FROM players;""")
#    db.session.commit
#    db.session.execute(""" UPDATE players22 SET scorewon = 0, scoreloss = 0, gamewon = 0, gameloss = 0;""")
#    db.session.commit
#    return


def playerstats(players:list, points:list):
    #päivitetään pelaajan kausitilastot
    sql = """ UPDATE players22 SET scorewon = scorewon + :w, scoreloss = scoreloss + :l 
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
    sql2 = """ UPDATE players22 SET gamewon = gamewon + :gw, gameloss = gameloss +:gl
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

#Tästä tulee talvikauden kausi tilastot, tähän pitää saada kausivalinta? players22 taulukko 2022-2023
#Tähän voisi tehdä laskenna voitto% yms ja palauttaa tiedot -> html eikä laskea siellä.
def season_stats():
    sql = "SELECT player, scorewon, scoreloss, gamewon, gameloss FROM players22 ORDER BY gamewon DESC;"
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
    sql = "SELECT * FROM tournaments WHERE id !=1;" #1 on talvikausi 2021-22, pitäisi muuttaa toimivammaksi
    result = db.session.execute(sql)
    tournaments = result.fetchall()
    return tournaments

def get_rounds():
    sql = "SELECT DISTINCT seasonround FROM games WHERE tournament_id = 1 ORDER BY seasonround DESC;" #1 on talvikausi 2021-22, pitäisi muuttaa toimivammaksi
    result = db.session.execute(sql)
    rounds = result.fetchall()
    return rounds

def get_roundstats(round):
    try:
        sql = """SELECT p1, p1score, p2, p2score, p3, p3score, p4, p4score, seasonround, game_time, id FROM games 
            WHERE seasonround=:round ORDER BY id ASC;"""
        result = db.session.execute(sql, {"round":round,})
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

def prevgameday():
    try:
        sql = "SELECT seasonround FROM games WHERE tournament_id = 1 ORDER BY seasonround DESC;"
        prev = db.session.execute(sql)
        round = prev.fetchone()
        lastround = round[0]
    except:
        return False
    return lastround

#haetaan pelin tulokset ja pelaajat muokkausta varten
def gameresult(id):
    sql = """SELECT p1, p2, p3, p4 FROM games WHERE id=:id"""
    result = db.session.execute(sql, {"id":id,})
    game = result.fetchone()
    return game

#muokkaa pelatun pelin tuolokset    
def modify(g1:int, g2:int, id:int):
    sql ="""UPDATE games SET p1score = :p1, p2score = :p2, p3score = :p3, p4score = :p4 WHERE id = :id; """ 
    db.session.execute(sql, {"p1":g1, "p2":g1, "p3":g2, "p4":g2, "id":id,})
    db.session.commit()
    return
    
    
    
    #try:
    #    sql = "SELECT game_time FROM games ORDER BY game_time DESC;"
    #    prev = db.session.execute(sql)
    #    gameday = prev.fetchone()
    #    day = gameday[0].strftime("%Y-%m-%d")
    #except:
    #    return False
    #return day