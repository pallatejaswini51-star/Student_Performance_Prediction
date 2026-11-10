
from database import create_table, get_connection

create_table()

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, name, username FROM users")
users = cursor.fetchall()

print("Registered users:", users)

conn.close()
