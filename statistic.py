from sqlalchemy.orm import query
from werkzeug.wrappers import request
from db import db
from flask import session


def results(T1:int, T2:int, T1_P1:str, T1_P2:str, T2_P1:str, T2_P2:str):
    sql_t1 = "INSERT INTO stats (player, score) VALUES (:player, :score)"
    sql_t2 = "INSERT INTO stats (player, score) VALUES (:player, :score)"
    sql_t3 = "INSERT INTO stats (player, score) VALUES (:player, :score)"
    sql_t4 = "INSERT INTO stats (player, score) VALUES (:player, :score)"
    db.session.execute(sql_t1, {"player": T1_P1, "score": T1})
    db.session.execute(sql_t2, {"player": T1_P2, "score": T1})
    db.session.execute(sql_t3, {"player": T2_P1, "score": T2})
    db.session.execute(sql_t4, {"player": T2_P2, "score": T2})
    db.session.commit()    
    return True


def gameday_stats():
    sql = "SELECT player, SUM(score) FROM stats GROUP BY player ORDER BY sum DESC;"
    result = db.session.execute(sql)
    gameday_podium = result.fetchall()
    return gameday_podium

def season_stats():
    sql = "SELECT player, SUM(score) FROM stats GROUP BY player ORDER BY sum DESC;"
    result = db.session.execute(sql)
    podium = result.fetchall()
    return podium