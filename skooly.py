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
    id_user1 = cur.execute("""
    SELECT id_user FROM users
    WHERE id_user = ?;
    """,(user.id_user,)).fetchone()
    # usage of ai to debug the above line
    print(id_user1)
    token = str(uuid4())
    cur.execute("""
    DELETE FROM tokens
    WHERE id_user = ?
    """,(id_user1[-1],))
    cur.execute("""
    INSERT INTO tokens (id_user, token)
    VALUES (?, ?)
    """,((id_user1[-1]), (token)))
    con.commit()
    con.close()
    response = {"id_user": id_user1,"auth_token": token}
    return response