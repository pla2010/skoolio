import sqlite3
from fastapi import FastApi
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastApi()

Class User():
    id_user: int
    name: str | None = None
    pw: str

@app.get("/")
def root():
    return {"message": "Root"}
@app.get("/auth")
# A changer avant la prod !!!

def auth(user: User):
    con = sqlite3.connect("skooly.db")
    cur=con.cursor()
    id_user = cur.execute("""
    SELECT id_user FROM users
    WHERE id_user = ? OR name= ?
    """,(user.id_user, user.name))
    token = uuid4()
    cur.execute("""
    INSERT INTO tokens (id_user, token)
    VALUES (?, ?)
    """,(id_user, token))
    con.close()
    response = {"id_user": id_user,"auth_token": token}
    return response