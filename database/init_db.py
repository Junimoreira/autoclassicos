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

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS cidade VARCHAR(100);
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS estado CHAR(2);
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS local_evento VARCHAR(200);
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS data_inicio DATE;
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS data_fim DATE;
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS descricao TEXT;
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS ativo BOOLEAN DEFAULT TRUE;
    """)

    cur.execute("""
        ALTER TABLE eventos
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
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

    cur.execute("""
        ALTER TABLE clubes
        ADD COLUMN IF NOT EXISTS instagram VARCHAR(150);
    """)

    cur.execute("""
        ALTER TABLE clubes
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    """)

    # ==================================================
    # PARTICIPANTES
    # ==================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            telefone VARCHAR(50),
            email VARCHAR(150),
            cidade VARCHAR(100),
            estado CHAR(2),
            clube_id INTEGER,
            primeira_participacao BOOLEAN DEFAULT TRUE,
            autorizacao_imagem BOOLEAN DEFAULT TRUE,
            observacoes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_participante_clube
                FOREIGN KEY (clube_id)
                REFERENCES clubes(id)
                ON DELETE SET NULL
        );
    """)

    # ==================================================
    # VEÍCULOS
    # ==================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id SERIAL PRIMARY KEY,
            participante_id INTEGER NOT NULL,
            marca VARCHAR(100) NOT NULL,
            modelo VARCHAR(100) NOT NULL,
            ano INTEGER,
            cor VARCHAR(50),
            placa VARCHAR(20) UNIQUE,
            categoria VARCHAR(50),
            foto TEXT,
            descricao TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_veiculo_participante
                FOREIGN KEY (participante_id)
                REFERENCES participantes(id)
                ON DELETE CASCADE
        );
    """)

    # ==================================================
    # INSCRIÇÕES
    # ==================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inscricoes (
            id SERIAL PRIMARY KEY,
            evento_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            veiculo_id INTEGER NOT NULL,
            numero_inscricao INTEGER,
            quantidade_pessoas INTEGER DEFAULT 1,
            chegada_prevista DATE,
            saida_prevista DATE,
            status VARCHAR(30) DEFAULT 'INSCRITO',
            uuid_qrcode VARCHAR(100),
            observacoes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_inscricao_evento
                FOREIGN KEY (evento_id)
                REFERENCES eventos(id)
                ON DELETE CASCADE,
            CONSTRAINT fk_inscricao_participante
                FOREIGN KEY (participante_id)
                REFERENCES participantes(id)
                ON DELETE CASCADE,
            CONSTRAINT fk_inscricao_veiculo
                FOREIGN KEY (veiculo_id)
                REFERENCES veiculos(id)
                ON DELETE CASCADE
        );
    """)

    cur.execute("""
        ALTER TABLE inscricoes
        ADD COLUMN IF NOT EXISTS observacoes TEXT;
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Banco atualizado com sucesso!")