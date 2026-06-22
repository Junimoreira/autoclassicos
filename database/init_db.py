from database.connection import conectar


def criar_tabelas():

    conn = conectar()

    if conn is None:
        return

    cur = conn.cursor()

    # ==================================================
    # USUÁRIOS
    # ==================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (

            id SERIAL PRIMARY KEY,

            nome VARCHAR(100) NOT NULL,

            usuario VARCHAR(50) UNIQUE NOT NULL,

            senha TEXT NOT NULL,

            ativo BOOLEAN DEFAULT TRUE,

            perfil VARCHAR(50) DEFAULT 'usuario',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
    """)

    # garante coluna perfil em bancos antigos
    cur.execute("""
        ALTER TABLE usuarios
        ADD COLUMN IF NOT EXISTS perfil VARCHAR(50) DEFAULT 'usuario';
    """)

    # ==================================================
    # EVENTOS
    # ==================================================
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

    # ==================================================
    # CLUBES
    # ==================================================
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

    # garante colunas em bancos antigos
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

    print("Banco atualizado com sucesso!")