from app import app
from flask import render_template, request, redirect
import users, recipes

@app.route("/")
def index():
    list = recipes.get_list()
    return render_template("index.html", count=len(list), recipes = list)

@app.route("/new")
def new():
    return render_template("writenew.html")

@app.route("/write", methods=["POST"])
def write():
    content = request.form["content"]
    if recipes.write(content):
        return redirect("/")
    else:
        return render_template("errormessage.html", message = "Julkaisu ei onnistunut")

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    if query.result(query):
        return render_template("result.html", recipes = recipes)
    else:
        return render_template("errormessage.html", message = "Annetulla sanalla ei löydy reseptejä")


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
            return render_template("errormessage.html", message="Väärä tunnus tai salasana")

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
            return render_template("errormessage.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("errormessage.html", message="Rekisteröinti ei onnistunut")