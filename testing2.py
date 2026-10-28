import sqlite3
con = sqlite3.connect("skooly.db")
cur = con.cursor()
user_name = cur.execute("""
SELECT name FROM users
WHERE id_user = 0;
""").fetchone()
print(user_name[0])
token_verify = cur.execute("""
SELECT token FROM tokens WHERE id_user = 0
""").fetchone()
print(token_verify[0])