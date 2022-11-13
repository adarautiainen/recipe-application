import recipes
from db import db


def result(query):
    sql = "SELECT id, content FROM recipes WHERE content LIKE :query"
    result = db.session.execute(sql, {"query" : "%" +query+"%"})
    return result.fetchall()
    

