from db import db
import users

def get_list():
    sql = "SELECT R.content, U.username FROM recipes R, users U WHERE R.user_id=U.id ORDER BY R.id"
    result = db.session.execute(sql)
    return result.fetchall()

def write(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO recipes (content, user_id) VALUES (:content, :user_id)"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True
