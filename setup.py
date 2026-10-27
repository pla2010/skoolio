import sqlite3
con = sqlite3.connect("skooly.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
id_user INTEGER PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
pw_hash text NOT NULL,
type int NOT NULL,
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS classes (
id_class INTEGER PRIMARY KEY AUTOINCREMENT,
id_teacher INTEGER,
name_class text NOT NULL,
FOREIGN KEY (id_teacher) REFERENCES users(id_user)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS students_in_classes (
id_user INTEGER PRIMARY KEY,
id_class INTEGER PRIMARY KEY,
FOREIGN KEY (id_user) references users (id_user)
FOREIGN KEY (id_class) references class (id_class)
);
""")