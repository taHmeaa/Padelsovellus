from operator import methodcaller
from app import app
from flask import render_template, request, redirect
import users, statistic, gamebracket


@app.route("/")
def index():
    players = gamebracket.get_players()
    return render_template("index.html", players = players)

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

@app.route("/playerapp", methods=["GET", "POST"])
def playerapp():
    if request.method == "POST":
        users.csrf()
        add_player = request.form["add_player"]
        #tarkastetaan, että syöte on oikea
        if 3 < len(add_player) < 9:
            if users.players(add_player):
                return redirect("/playerapp")
            else:
                return redirect("/playerapp")
        else:
            return redirect("/playerapp") 
    players = gamebracket.get_players()
    return render_template("players.html", players = players)

@app.route("/playerdel", methods=["GET", "POST"])
def playerdel():
    if request.method == "POST":
        users.csrf()
        if users.is_admin():
            del_player = request.form["del_player"]

    pass

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "POST":
        users.csrf()
        game_results = request.form.getlist("gamescore")
        game_players = request.form.getlist("gamedata")
        statistic.results(game_players, game_results)
        statistic.playerstats(game_players, game_results)
        day_podium = statistic.gameday_stats()
        return render_template("dayscores.html", day_podium = day_podium)                   
    podium =statistic.season_stats()
    return render_template("seasonstats.html", podium = podium)  

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
            return render_template("index.html", message="Kirjautuminen ei onnistunut")

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
            return render_template("register.html", message="Rekisteröinti ei onnistunut")