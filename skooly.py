import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

class User(BaseModel):
    id_user: int | None = None
    name: str | None = None
    pw_hash: str | None = None
class Course(BaseModel):
    id_course: int | None = None
    id_class: int | None = None
    name_class: str | None = None
    id_course: int | None = None
    name_course: str | None = None
    content_course: str | None = None
class Class(BaseModel):
    id_class: int | None = None
    id_teacher: int | None = 0
    name_class: str | None = "Example"
def verify_token(id_user: int, token: str):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    token_verify = cur.execute("""
    SELECT token FROM tokens WHERE id_user = ?
    """,(id_user,)).fetchone()
    con.close()
    if not token_verify:
        return False
    if token == token_verify[0]:
        return True
    return False
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Root"}
@app.post("/template")
def template(user: User, token: str):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    token_verify = cur.execute("""
    SELECT token FROM tokens WHERE id_user = ?
    """,(user.id_user,)).fetchone()
    if not token_verify:
        return {"error": "Unauthorized"}
    if token == token_verify[0]:
        return {"code": "200"}
    else:
        return {"error": "Unauthorized"}
@app.post("/auth")
# A changer avant la prod (hash supplémentaire mot de passe)!!!
def auth(user: User):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    user_data = cur.execute("""
    SELECT id_user, pw_hash FROM users
    WHERE id_user = ?;
    """,(user.id_user,)).fetchone()
    # usage of ai to debug the above line
    if not user_data:
        return {"error": "no such data in database"}

    id_user_db = user_data[0]
    pw_hash_user = user_data[1]
    # / ! \ !!! Méthode non secure, possible voler et copier le hash, a changer absolument !
    if pw_hash_user == user.pw_hash:
        token = str(uuid4())
        cur.execute("""
        DELETE FROM tokens
        WHERE id_user = ?
        """,(id_user_db,))
        cur.execute("""
        INSERT INTO tokens (id_user, token)
        VALUES (?, ?)
        """,((id_user_db), (token)))
        con.commit()
        con.close()
        response = {"id_user": id_user_db,"auth_token": token}
        return response
    else:
        return {"error": "password incorrect"}
@app.post("/create_user")
def create_user(user: User):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    cur.execute("""
    INSERT INTO users (name, pw_hash, type)
    VALUES (?, ?, 1)
    """, (user.name, user.pw_hash))
    con.commit()
    id_newuser = cur.execute("""
    SELECT id_user FROM users
    WHERE name = ?
    """,(user.name,)).fetchone()
    con.close()
    if id_newuser:
        return {"id_user": id_newuser}
    else:
        return {"error": "account not created."}
@app.post("/delete_user")
def delete_user(user: User, token: str):
    if verify_token(user.id_user, token) == True:
        con = sqlite3.connect("skooly.db")
        cur=con.cursor()
        cur.execute("""
        DELETE FROM users
        WHERE id_user = ?
        """,(user.id_user,))
        cur.execute("""
        DELETE FROM tokens
        WHERE id_user = ?
        """,(user.id_user,))
        checking = cur.execute("""
        SELECT * FROM users
        WHERE id_user = ?
        """,(user.id_user,)).fetchone()
        con.commit()
        con.close()
        if not checking:
            return {"code": "200"}
        return {"error": "Account not deleted"}
    return {"error": "Unauthorized"}
@app.post("/retrieve/user_data")
def retrieve_user_data(user: User, token: str):
    if verify_token(user.id_user, token) == True:
        con = sqlite3.connect("skooly.db")
        cur=con.cursor()
        user_data = cur.execute("""
        SELECT name, type FROM users
        WHERE id_user = ?;
        """,(user.id_user,)).fetchone()
        con.close()
        return {"user_name": user_name}
    else:
        return {"error": "Unauthorized"}
@app.post("/change_user_type/")
def change_user_type(user:User, token: str, user_change_id: int, user_new_id: int):
    if verify_token(user.id_user, token) == True:
        con = sqlite3.connect("skooly.db")
        cur=con.cursor()
        user_type = cur.execute("""
        SELECT type FROM users
        WHERE id_user = ?;
        """,(user.id_user,)).fetchone()
        if user_type[0] == 0:
            cur.execute("""
            UPDATE users
            SET type = ?
            WHERE id_user = ?;
            """,(user_new_id, user_change_id))
            con.commit()
            con.close()
            return {"code": "200"}
        return {"error": "Unauthorized"}
    return {"error": "Unauthorized"}
@app.post("/create_class")
def template(user: User, token: str, class_data: Class):
    if verify_token(user.id_user, token) == True:
        con = sqlite3.connect("skooly.db")
        cur=con.cursor()
        user_type = cur.execute("""
        SELECT type FROM users
        WHERE id_user = ?;
        """,(user.id_user,)).fetchone()
        if user_type[0] == 0:
            cur.execute("""
            INSERT INTO classes(name_class, id_teacher)
            VALUES (?,?);
            """,(class_data.name_class, class_data.id_teacher))
            class_id = cur.execute("""
            SELECT id_class FROM classes
            WHERE name_class = ? AND id_teacher = ?;
            """, (class_data.name_class, class_data.id_teacher)).fetchone()
            return {"id_class": class_id}
    else:
        return {"error": "Unauthorized"}
