from db import db
from flask import session

def addplayers(add_player):
    try:
        sql = """INSERT INTO players (player, scorewon, scoreloss, visible)
                VALUES (:player, 0, 0, TRUE);"""
        db.session.execute(sql, {"player":add_player})
        db.session.commit()
    except:
        return False

def delplayers(del_player):
    sql = "UPDATE players SET visible=FALSE WHERE player = :player"
    db.session.execute(sql, {"player":del_player})
    db.session.commit()
    return
