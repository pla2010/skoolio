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