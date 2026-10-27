import sqlite3
con = sqlite3.connect("skooly.db")
cur = con.cursor()

cur.execute("""
SELECT * FROM users
""")
print(cur.fetchall())