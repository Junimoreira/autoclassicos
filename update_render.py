from database.connection import conectar

conn = conectar()

cur = conn.cursor()

cur.execute("""
    ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS perfil VARCHAR(50) DEFAULT 'usuario'
""")

conn.commit()

cur.close()
conn.close()

print("Coluna perfil criada com sucesso!")