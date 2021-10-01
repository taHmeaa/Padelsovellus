from app import app
from flask import render_template, request, redirect
import users, statistic, scores

@app.route("/")
def index():
    podium = statistic.season_stats()
    return render_template("index.html", podium = podium)

@app.route("/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        players = request.form.getlist("player")
        #tarkastetaan, että pelaaja valinnat ovat oikein
        if len(players) > 3:
            playerchart = scores.get_players(players)
            return render_template("games.html", playerchart=playerchart)
        else:
            return redirect("/")

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "POST":
        game_results = request.form.getlist("gamescore")
        game_players = request.form.getlist("gamedata")
        statistic.results(game_players, game_results)
        statistic.playerstats(game_players, game_results)
        day_podium = statistic.gameday_stats()
        return render_template("dayscores.html", day_podium = day_podium)                   
        
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


#tällä  hetkellä vain yksi tunnus sivustolle.
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