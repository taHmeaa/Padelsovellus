from sqlalchemy.orm import query
from werkzeug.wrappers import request
from db import db
from flask import session


def results(T1:int, T2:int):
    sql_t1 = "INSERT INTO stats (player, score) VALUES ('Pelaaja1', :score)"
    sql_t2 = "INSERT INTO stats (player, score) VALUES ('Pelaaja2', :score)"
    db.session.execute(sql_t1, {"score": T1})
    db.session.execute(sql_t2, {"score": T2})
    db.session.commit()    
    return True

def season_stats():
    sql = "SELECT player, SUM(score) FROM stats GROUP BY player ORDER BY sum DESC;"
    result = db.session.execute(sql)
    podium = result.fetchall()
    return podium