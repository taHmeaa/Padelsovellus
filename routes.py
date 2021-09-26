from app import app
from flask import render_template, request, redirect
import users, statistic, scores

@app.route("/")
def index():
    podium = statistic.season_stats()
    return render_template("index.html", podium = podium)

@app.route("/games", methods=["GET", "POST"])
def games():
    #tähän pitäisi saada testi, että on valittu vähintään 4 pelaajaa
    if request.method == "POST":
        players = request.form.getlist("player")
        rand_players = scores.get_players(players)
        return render_template("games.html", P1 = rand_players[0],
                                             P2 = rand_players[1],
                                             P3 = rand_players[2],
                                             P4 = rand_players[3])

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "POST":
        T1 = request.form["T1"]
        T2 = request.form["T2"]
        if statistic.results(T1, T2):
            return redirect("/")                   
        
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
            return render_template("error.html", message="Väärä tunnus tai salasana")

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
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")