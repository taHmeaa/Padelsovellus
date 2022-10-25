import datetime
from operator import methodcaller
#from unicodedata import name
from app import app
from flask import render_template, request, redirect
import users, statistic, gamebracket, playerconfig


@app.route("/")
def index():
    return redirect("/login")

@app.route("/gameindex")
def gameindex():
    players = gamebracket.get_players()
    return render_template("indexseason.html", players = players)

#@app.route("/newseason")
#def newseason():
#    if request.method == "POST":
#        users.csrf()
#        add_season = request.form["add_season"]


@app.route("/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        users.csrf()
        players = request.form.getlist("player")
        rounds = int(request.form["roundvalue"])
        #tarkastetaan, että pelaajavalinnat ovat oikein 
        if len(players) > 3:
            playerchart = gamebracket.get_brackets(players, True)
            #tähän fault handling, jos ei ole pelejä tulee error.
            nextround = statistic.prevgameday() + 1  #+1 luodaan seuraava kierros
            return render_template("games.html", playerchart=playerchart, rounds=rounds, sr = nextround)
        else:
            return redirect("/gameindex")

@app.route("/americano", methods=["GET", "POST"])
def americano():
    if request.method == "POST":
        users.csrf()
        players = request.form.getlist("player")
        tournament_name = request.form["tournament_name"]
        #tarkastetaan, että nimi ei ole jo käytössä ja syötetään se taulukkoon
        if statistic.tournament(tournament_name): 
            #tarkastetaan, että pelaajavalinnat ovat oikein 
            if len(players) == 8:
                playerchart = gamebracket.americanobracket(players)
                t_id = statistic.tournament_id(tournament_name)
                return render_template("americano.html", tournament_name=tournament_name, playerchart=playerchart, t_id = t_id[0])
            else:
                return redirect("/americano")
        else:
            return redirect("/americano")
    playerlist = gamebracket.get_players()
    return render_template("indexamericano.html", players = playerlist)

@app.route("/playerapp", methods=["GET", "POST"])
def playerapp():
    players = gamebracket.get_players()
    if request.method == "POST":
        users.csrf()
        add_player = request.form["add_player"]
        #tarkastetaan, että syöte on oikea
        if 3 < len(add_player) < 9:
            if playerconfig.addplayers(add_player):
                return redirect("/playerapp")
            else:
                return render_template("players.html", name_error = "Nimi jo käytössä tai jäädytetty", players = players)
        else:
            return redirect("/playerapp") 
    return render_template("players.html", players = players)

@app.route("/playerdel", methods=["GET", "POST"])
def playerdel():
    if request.method == "POST":
        users.csrf()
        del_player = request.form.getlist("del_player")
        if len(del_player) == 1:
            if users.is_admin():
                del_player = request.form["del_player"]
                playerconfig.delplayers(del_player)
                return redirect("/playerapp")
            else:
                players = gamebracket.get_players()
                return render_template("players.html", players =players, error = "Vain ADMIN voi poistaa pelaajan")

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "POST":
        users.csrf()
        game_results = request.form.getlist("gamescore")
        game_players = request.form.getlist("gamedata")
        tournament_id = request.form["tournament_id"]
        seasonround = request.form["seasonround"]
        statistic.results(game_players, game_results, int(tournament_id), int(seasonround))
        #Koska käytetään samaa stats turnauksille ja kaudelle
        #tällä estetään kausitilastojen muokkaus.
        if int(tournament_id) == 1:
            statistic.playerstats(game_players, game_results)
        day_podium = statistic.gameday_stats()
        games = statistic.get_roundstats(seasonround)
        return render_template("dayscores.html", day_podium = day_podium, games = games)                   
    podium =statistic.season_stats()
    return render_template("scorestats.html", podium = podium)

@app.route("/americanostats", methods=["GET", "POST"])
def americanostats():
    tournament_name = statistic.get_tournaments()
    if request.method == "POST":
        users.csrf()
        tournament_id = request.form["tournament_id"]
        if statistic.americano_stats(tournament_id):
            games = statistic.americano_stats(tournament_id)
            day_podium = statistic.gameday_stats()
            return render_template("americanostats.html", day_podium = day_podium, names = tournament_name, name = games[0][8], games = games)
        else:
            return render_template("americanostats.html",names = tournament_name, error = "Ei pelejä, valitse toinen turnaus")
    return render_template("americanostats.html", names = tournament_name)                   

#tästä haetaan pelihistoria kausipeleistä kaikki missä round > 0, 0 on vakio käytetään Americanossa
@app.route("/allgames", methods=["GET", "POST"])
def allgames():
    #haetaan kaikki kierrokset
    rounds = statistic.get_rounds()
    if request.method == "POST":
        users.csrf()
        round = request.form["round"]
        if statistic.get_roundstats(round):
            games = statistic.get_roundstats(round)
            date = games[0][9].strftime("%d-%m-%y") 
            day_podium = statistic.gameday_stats()
            return render_template("gamestats.html", day_podium = day_podium, games = games, rounds = rounds, name = games[0][8], date = date)
        else:
            #last_gameday = statistic.prevgameday()
            return render_template("gamestats.html", message = "Ei pelejä kyseisenä päivänä")
    #tämä generoi alkuun edellisen pelipäivän pelit esille
    if statistic.prevgameday():
        last_gameday = statistic.prevgameday()
        games = statistic.get_roundstats(last_gameday)
        date = games[0][9].strftime("%d-%m-%y")
        day_podium = statistic.gameday_stats()
        return render_template("gamestats.html", day_podium = day_podium, games = games, rounds = rounds, name = games[0][8], date = date)
    else:
        return render_template("gamestats.html", message = "Ei vielä pelattuja pelejä")

#haetaam peli pelihistoriasivun kautta muokkausta varten
@app.route("/getgame", methods=["GET", "POST"])
def getgame():
    if request.method == "POST":
        users.csrf()
        if users.is_admin():
            game = request.form["get_game"]
            gameplayers = statistic.gameresult(game)
            return render_template("modifygame.html", game = game, P = gameplayers)
        else:
            return redirect("/allgames")
            
#muokataan tuloksia
@app.route("/modify", methods=["GET", "POST"])
def modify():
    if request.method == "POST":
        users.csrf()
        if users.is_admin():
            r = request.form.getlist("gamescore")
            game = request.form["get_game"]
            statistic.modify(r[0], r[1], game)
            return redirect("/allgames")
        else:
            return redirect("/allgames")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/gameindex")
        else:
            return render_template("login.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/gameindex")
        else:
            return render_template("register.html", message="Tunnus jo käytössä")