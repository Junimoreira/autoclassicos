from database.connection import conectar

conn = conectar()
cur = conn.cursor()

cur.execute("""
    SELECT id, nome, usuario, perfil
    FROM usuarios
""")

for usuario in cur.fetchall():
    print(usuario)

cur.close()
conn.close()