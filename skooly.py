import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

class User(BaseModel):
    id_user: int | None = None
    name: str | None = None
    pw_hash: str | None = None

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Root"}
@app.post("/auth")
# A changer avant la prod !!!
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
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    token_verify = cur.execute("""
    SELECT token FROM tokens WHERE id_user = ?
    """,(user.id_user,)).fetchone()
    try:
        if token == token_verify[0]:
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
                return {"message": "Account Deleted"}
            else:
                return {"error": "Account not deleted"}
        else:
            return {"error": "Unauthorized"}
    except TypeError as e:
        return {"error": f"Type error, full error : {e}"}
@app.post("/retrieve/user_data")
def retrieve_user_data(user: User, token: str):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    token_verify = cur.execute("""
    SELECT token FROM tokens WHERE id_user = ?
    """,(user.id_user,)).fetchone()
    if not token_verify:
        return {"error": "Unauthorized"}
    if token == token_verify[0]:
        user_name = cur.execute("""
        SELECT name FROM users
        WHERE id_user = ?;
        """,(user.id_user,)).fetchone()
        con.close()
        return {"user_name": user_name}
    else:
        return {"error": "Unauthorized"}
@app.post("/change_user_type/")
def change_user_type(user:User, token: str, user_change_id: int):
        con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    token_verify = cur.execute("""
    SELECT token FROM tokens WHERE id_user = ?
    """,(user.id_user,)).fetchone()
    if not token_verify:
        return {"error": "Unauthorized"}
    if token == token_verify[0]:
        user_type = cur.execute("""
        SELECT type FROM users
        WHERE id_user = ?;
        """,(user.id_user,)).fetchone()
        if user_type[0] == 0:
            cur.execute("""
            UPDATE users
            SET type = 0
            WHERE id_user = ?;
            """,(user_change_id,))
            con.commit()
            con.close()
            return {"mesasge": "User Type changed"}
        return {"error": "Unauthorized"}
    return {"error": "Unauthorized"}