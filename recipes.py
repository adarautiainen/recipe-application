from db import db
import users
from flask import session

def get_recipes():
    sql = "SELECT id, name FROM recipes WHERE visible = 1 ORDER BY name"
    return db.session.execute(sql).fetchall()

def result(query):
    sql = "SELECT id, name, content FROM recipes WHERE visible = 1 AND name LIKE :query OR content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def order():
    sql = "SELECT R.id, R.name, SUM(W.scores) FROM reviews W, recipes R WHERE R.visible = 1 GROUP BY R.id ORDER BY SUM(W.scores)"
    return db.session.execute(sql).fetchall()

def write(name, content):
    user_id = users.user_id()
    visible = 1
    if user_id == 0:
        return False
    sql = "INSERT INTO recipes (name, content, user_id, visible) VALUES (:name, :content, :user_id, :visible)"
    db.session.execute(sql, {"name":name, "content":content, "user_id":user_id, "visible":visible})
    db.session.commit()
    return True

def get_info(recipe_id):
    sql = "SELECT R.name, R.content, U.username FROM recipes R, users U WHERE R.id=:recipe_id AND R.user_id=U.id"
    return db.session.execute(sql, {"recipe_id": recipe_id}).fetchone()

def get_reviews(recipe_id):
    sql = "SELECT U.username, R.scores, R.review FROM users U, reviews R WHERE R.user_id=U.id \
        AND R.recipe_id=:recipe_id AND visible = 1 ORDER BY R.id"
    return db.session.execute(sql, {"recipe_id":recipe_id}).fetchall()

def get_shown_reviews():
    sql = "SELECT id, review FROM reviews WHERE visible = 1"
    return db.session.execute(sql).fetchall()

def get_shown_recipes():
    sql = "SELECT id, name FROM recipes WHERE visible = 1"
    return db.session.execute(sql).fetchall()

def add_reviews(recipe_id, user_id, scores, review):
    visible = 1
    sql = "INSERT INTO reviews (recipe_id, user_id, scores, review, visible) \
        VALUES (:recipe_id, :user_id, :scores, :review, :visible)"
    db.session.execute(sql, {"recipe_id":recipe_id, "user_id":user_id, "scores":scores, "review":review, "visible":visible})
    db.session.commit()

def delete_recipe(recipe_id):
    sql = "UPDATE recipes SET visible = 0 WHERE id=:id"
    db.session.execute(sql, {"id":recipe_id})
    db.session.commit()

def delete_comment(review_id):
    sql = "UPDATE reviews SET visible = 0 WHERE id=:id"
    db.session.execute(sql, {"id":review_id})
    db.session.commit()

def get_recipeid():
    return session.get("recipe_id", 0)

def favorite(user_id, recipe_id, recipe_name):
    sql = "INSERT INTO favorites (user_id, recipe_id, recipe_name) VALUES (:user_id, :recipe_id, :recipe_name)"
    db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id, "recipe_name":recipe_name})
    db.session.commit()

def getfavorites(user_id):
    sql = "SELECT id, recipe_id, recipe_name FROM favorites WHERE user_id=:user_id ORDER BY recipe_name"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()