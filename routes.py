from app import app
from flask import render_template, request, redirect
import users, recipes

@app.route("/")
def index():
    return render_template("index.html", recipes = recipes.get_recipes())

@app.route("/new")
def new():
    return render_template("writenew.html")

@app.route("/write", methods=["POST"])
def write():
    users.check_csrf()
    name = request.form["name"]
    content = request.form["content"]

    if recipes.write(name, content):
        return redirect("/")
    else:
        return render_template("errormessage.html", message = "Julkaisu ei onnistunut")

@app.route("/order")
def order():
    return render_template("ordered.html", recipes = recipes.order())

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    info = recipes.get_info(recipe_id)
    reviews = recipes.get_reviews(recipe_id)
    return render_template("recipe.html", id = recipe_id, name = info[0], content = info[1], user = info[2], reviews = reviews)

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    if recipes.result(query):
        return render_template("searchresult.html", recipes = recipes.result(query))
    else:
        return render_template("errormessage.html", message = "Annetulla sanalla ei löydy reseptejä")
    
@app.route("/review", methods=["POST"])
def review():
    users.check_csrf()
    recipe_id = request.form["recipe_id"]
    scores = int(request.form["scores"])
    if scores < 1 or scores > 5:
        return render_template("errormessage.html", message = "Arvosana puuttui")

    review = request.form["review"]
    if len(review) > 1000:
        return render_template("errormessage.html", message = "Ei näin pitkiä kommentteja")
    if review == "":
        return render_template("errormessage.html", message = "Teksti puuttui")

    recipes.add_reviews(recipe_id, users.user_id(), scores, review)
    return redirect("/recipe/"+str(recipe_id))

#delete recipe
@app.route("/delete", methods=["GET", "POST"])
def delete_recipe():
    users.require_role(2)

    if request.method == "GET":
        shown_recipes = recipes.get_shown_recipes()
        return render_template("remove.html", list=shown_recipes)

    if request.method == "POST":
        users.check_csrf()
        if "recipe" in request.form:
            recipe = request.form["recipe"]
            recipes.delete_recipe(recipe)

    return redirect("/")

#delete comment
@app.route("/deletecom", methods=["GET", "POST"])
def delete_comment():
    users.require_role(2)

    if request.method == "GET":
        shown_comments = recipes.get_shown_reviews()
        return render_template("removecom.html", list=shown_comments)

    if request.method == "POST":
        users.check_csrf()
        if "review" in request.form:
            review = request.form["review"]
            recipes.delete_comment(review)

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
        role = request.form["role"]
        if password1 != password2:
            return render_template("errormessage.html", message="Salasanat eivät täsmää")
        if users.register(username, password1, role):
            return redirect("/")
        else:
            return render_template("errormessage.html", message="Jotain meni vikaan rekisteröinnissä")
        
@app.route("/favorite", methods=["GET", "POST"])
def favorite():
    if request.method == "GET":
        return render_template("favorites.html", list = recipes.getfavorites(users.user_id()))
    if request.method == "POST":
        users.check_csrf()
        recipe_id = request.form["recipe_id"]
        recipe_name = request.form["recipe_name"]
        recipes.favorite(users.user_id(), recipe_id, recipe_name)
        return redirect("/recipe/"+str(recipe_id))
