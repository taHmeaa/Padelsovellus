from app import app
from flask import render_template, request, redirect
import users, statistic, scores

@app.route("/")
def index():
    podium = statistic.season_stats()
    return render_template("index.html", podium = podium)

@app.route("/games", methods=["GET", "POST"])
def games():
    #tähän pitäisi saada testi, että on valittu vähintään 5 pelaajaa
    if request.method == "POST":
        players = request.form.getlist("player")
        #number_players = len(players)
        rand_players = scores.get_players(players)
        #if number_players == 5: tähän tulee ehdot eri kaavioihin
        return render_template("games.html",    P1 = rand_players[0],
                                                P2 = rand_players[1],
                                                P3 = rand_players[2],
                                                P4 = rand_players[3],
                                                P5 = rand_players[4])

#jollain pitäisi ratkaista, että saisi päivän kaavion näkyviin ilman, että
#pelaajat arvotaan uudestaa......
#@app.route("/gameday", methods=["GET", "POST"])
#def gameday():
#    if request.method == "POST":
#        #joukkueen pisteet
#        T1_points = request.form["T1"]
#        T2_points = request.form["T2"]
#        1. joukkueen pelaajat
#        T1_P1 = request.form["P1"]
#        T1_P2 = request.form["P2"]
#        2. joukkuuen pisteet
#        T2_P1 = request.form["P3"]
#        T2_P2 = request.form["P4"]
#        if statistic.results(T1_points, T2_points, T1_P1, T1_P2, T2_P1, T2_P2):
#           return render_template("games.html") 

@app.route("/stats", methods=["GET", "POST"])
def stats():
    if request.method == "POST":
        #joukkueen pisteet
        T1_points = request.form["T1"]
        T2_points = request.form["T2"]
        #1. joukkueen pelaajat
        T1_P1 = request.form["P1"]
        T1_P2 = request.form["P2"]
        #2. joukkuuen pisteet
        T2_P1 = request.form["P3"]
        T2_P2 = request.form["P4"]
        if statistic.results(T1_points, T2_points, T1_P1, T1_P2, T2_P1, T2_P2):
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