from database.connection import conectar


def criar_tabelas():

    conn = conectar()

    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (

            id SERIAL PRIMARY KEY,

            nome VARCHAR(100) NOT NULL,

            usuario VARCHAR(50) UNIQUE NOT NULL,

            senha VARCHAR(255) NOT NULL,

            ativo BOOLEAN DEFAULT TRUE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS eventos (

            id SERIAL PRIMARY KEY,

            nome VARCHAR(200) NOT NULL,

            cidade VARCHAR(100),

            estado CHAR(2),

            local_evento VARCHAR(200),

            data_inicio DATE,

            data_fim DATE,

            descricao TEXT,

            ativo BOOLEAN DEFAULT TRUE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clubes (

            id SERIAL PRIMARY KEY,

            nome VARCHAR(150) UNIQUE,

            cidade VARCHAR(100),

            estado CHAR(2)

        );
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Banco atualizado com sucesso!")