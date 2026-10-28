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
    id_user = user_data[0]
    pw_hash_user = user_data[1]
    if pw_hash_user == user.pw_hash:
        
    # usage of ai to debug the above line
    print(user_data)
    token = str(uuid4())
    cur.execute("""
    DELETE FROM tokens
    WHERE id_user = ?
    """,(user_data[-1][0],))
    cur.execute("""
    INSERT INTO tokens (id_user, token)
    VALUES (?, ?)
    """,((user_data[-1]), (token)))
    con.commit()
    con.close()
    response = {"id_user": user_data,"auth_token": token}
    return response