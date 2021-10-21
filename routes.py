import datetime
from operator import methodcaller
from app import app
from flask import render_template, request, redirect
import users, statistic, gamebracket, playerconfig


@app.route("/")
def index():
    players = gamebracket.get_players()
    return render_template("indexseason.html", players = players)

@app.route("/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        users.csrf()
        players = request.form.getlist("player")
        rounds = int(request.form["roundvalue"])
        #tarkastetaan, että pelaajavalinnat ovat oikein 
        if len(players) > 3:
            playerchart = gamebracket.get_brackets(players, True)
            return render_template("games.html", playerchart=playerchart, rounds=rounds)
        else:
            return redirect("/")

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
        if users.is_admin():
            del_player = request.form["del_player"]
            playerconfig.delplayers(del_player)
            return redirect("/playerapp")
        else:
            return redirect("/")

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "POST":
        users.csrf()
        game_results = request.form.getlist("gamescore")
        game_players = request.form.getlist("gamedata")
        tournament_id = request.form["tournament_id"]
        statistic.results(game_players, game_results, int(tournament_id))
        #Koska käytetään samaa stats turnauksille ja kaudelle
        #tällä estetään kausitilastojen muokkaus.
        if int(tournament_id) == 1:
            statistic.playerstats(game_players, game_results)
        day_podium = statistic.gameday_stats()
        return render_template("dayscores.html", day_podium = day_podium)                   
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

#tästä haetaan pelihistoria tilastoihin
@app.route("/allgames", methods=["GET", "POST"])
def allgames():
    if request.method == "POST":
        users.csrf()
        date = request.form["gameday"]
        if statistic.getgames(date):
            games = statistic.getgames(date)
            return render_template("gamestats.html", games = games)
        else:
            last_gameday = statistic.prevgameday()
            games = statistic.getgames(last_gameday)
            return render_template("gamestats.html", games = games, message = "Ei pelejä kyseisenä päivänä")
    #tämä generoi alkuun edellisen pelipäivän pelit esille
    if statistic.prevgameday():
        last_gameday = statistic.prevgameday()
        games = statistic.getgames(last_gameday)
        return render_template("gamestats.html", games = games)
    else:
        return render_template("gamestats.html", message = "Ei vielä pelattuja pelejä")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
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
            return redirect("/")
        else:
            return render_template("register.html", message="Tunnus jo käytössä")