from database.connection import conectar

conn = conectar()
cur = conn.cursor()

cur.execute("""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
""")

print(cur.fetchall())

conn.close()