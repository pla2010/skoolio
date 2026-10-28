import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

class User(BaseModel):
    id_user: int
    name: str | None = None
    pw_hash: str

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
    id_user_db = user_data[0]
    pw_hash_user = user_data[1]
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
@app.post("/retrieve/user_data")
def retrieve_user_data(user: User, token: str):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    token_verify = cur.execute("""
    SELECT token FROM tokens WHERE id_user = ?
    """,(user.id_user,)).fetchone()
    if token == token_verify:
        user_name = cur.execute("""
        SELECT name FROM users
        WHERE id_user = ?;
        """,(user.id_user,)).fetchone()
        return {"user_name": user_name}
    else:
        return {"error": "Unauthorized"}