from db import db
import users, recipes

def get_recipes():
    sql = "SELECT id, name FROM recipes ORDER BY name"
    return db.session.execute(sql).fetchall()

def get_shown_recipes(user_id):
    sql = "SELECT id, name FROM recipes WHERE user_id=:user_id AND visible = 1 ORDER BY name"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def result(query):
    sql = "SELECT id, name, content FROM recipes WHERE name LIKE :query OR content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def order():
    sql = "SELECT R.name, W.scores FROM recipes R, reviews W ORDER BY W.scores"
    return db.session.execute(sql).fetchall()

def write(name, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO recipes (name, content, user_id) VALUES (:name, :content, :user_id)"
    db.session.execute(sql, {"name":name, "content":content, "user_id":user_id})
    db.session.commit()
    return True

def get_info(recipe_id):
    sql = "SELECT R.name, R.content, U.username FROM recipes R, users U WHERE R.id=:recipe_id AND R.user_id=U.id"
    return db.session.execute(sql, {"recipe_id": recipe_id}).fetchone()

def get_reviews(recipe_id):
    sql = "SELECT U.username, R.scores, R.review FROM users U, reviews R WHERE R.user_id=U.id AND R.recipe_id=:recipe_id ORDER BY R.id"
    return db.session.execute(sql, {"recipe_id":recipe_id}).fetchall()

def add_reviews(recipe_id, user_id, scores, review):
    sql = "INSERT INTO reviews (recipe_id, user_id, scores, review) VALUES (:recipe_id, :user_id, :scores, :review)"
    db.session.execute(sql, {"recipe_id":recipe_id, "user_id":user_id, "scores":scores, "review":review})
    db.session.commit()

def get_shown_reviews(user_id):
    sql = "SELECT id, review FROM reviews WHERE user_id=:user_id AND visible = 1 ORDER BY name"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def delete_recipe(recipe_id, user_id):
    sql = "UPDATE recipes SET visible = 0 WHERE recipe_id=:user_id AND user_id=:user_id"
    db.session.execute(sql, {"recipe_id":recipe_id, "user_id":user_id})
    db.session.commit()

def delete_comment(review_id, user_id):
    sql = sql = "UPDATE reviews SET visible = 0 WHERE review_id=:user_id AND user_id=:user_id"
    db.session.execute(sql, {"review_id":review_id, "user_id":user_id})
    db.session.commit()
