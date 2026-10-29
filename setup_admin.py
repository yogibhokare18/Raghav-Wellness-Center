"""Create or update the first admin account. Run: python setup_admin.py"""
import os
import getpass
import mysql.connector
from werkzeug.security import generate_password_hash

config = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "Yogi"),
    "database": os.environ.get("DB_NAME", "wellness_center"),
    "port": int(os.environ.get("DB_PORT", "3306")),
}
username = input("Admin username: ").strip()
password = getpass.getpass("Admin password (min 10 characters): ")
if not username or len(password) < 10:
    raise SystemExit("Username is required and password must be at least 10 characters.")
conn = mysql.connector.connect(**config)
cur = conn.cursor()
cur.execute("SELECT id FROM admins WHERE username=%s", (username,))
row = cur.fetchone()
password_hash = generate_password_hash(password)
if row:
    cur.execute("UPDATE admins SET password_hash=%s WHERE id=%s", (password_hash, row[0]))
else:
    cur.execute("INSERT INTO admins (username,password_hash) VALUES (%s,%s)", (username,password_hash))
conn.commit()
cur.close()
conn.close()
print("Admin account created/updated. Keep the password private.")
