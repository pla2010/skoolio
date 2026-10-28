import sqlite3
con = sqlite3.connect("skooly.db")
cur = con.cursor()

#cur.execute("INSERT INTO users (id_user, name, pw_hash, type)VALUES (0, 'adm', '0', 0);")
cur.execute("""
SELECT * FROM users
""")
print(cur.fetchall())
cur.execute("""
SELECT * FROM tokens
""")
print(cur.fetchall())

user_data = cur.execute("""
SELECT id_user, pw_hash FROM users
WHERE id_user = 0;
""").fetchone()
id_user = user_data[0]
pw_hash_user = user_data[1]
print(f"id user : {id_user}, pw hash : {pw_hash_user}")
token_verify = cur.execute("""
SELECT token FROM tokens WHERE id_user = 1
""").fetchone()
print(token_verify[0])
