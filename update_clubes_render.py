from database.connection import conectar

conn = conectar()
cur = conn.cursor()

cur.execute("""
    ALTER TABLE clubes
    ADD COLUMN IF NOT EXISTS instagram VARCHAR(150);
""")

cur.execute("""
    ALTER TABLE clubes
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
""")

conn.commit()
cur.close()
conn.close()

print("Tabela clubes atualizada com sucesso!")