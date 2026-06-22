    cur.execute("""
        CREATE TABLE IF NOT EXISTS clubes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(150) UNIQUE,
            cidade VARCHAR(100),
            estado CHAR(2),
            instagram VARCHAR(150),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        ALTER TABLE clubes
        ADD COLUMN IF NOT EXISTS instagram VARCHAR(150);
    """)

    cur.execute("""
        ALTER TABLE clubes
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    """)