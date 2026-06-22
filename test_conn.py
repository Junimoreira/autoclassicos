from database.connection import conectar

conn = conectar()

print("CONN:", conn)

if conn:
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print(cur.fetchone())