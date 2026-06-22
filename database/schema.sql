-- ==========================================================
-- AUTOCLÁSSICOS
-- Schema v2.0
-- PostgreSQL
-- ==========================================================

-- ==========================================================
-- USUÁRIOS
-- ==========================================================

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- EVENTOS
-- ==========================================================

CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,

    nome VARCHAR(200) NOT NULL,

    cidade VARCHAR(100),

    estado CHAR(2),

    local_evento VARCHAR(200),

    data_inicio DATE,

    data_fim DATE,

    data_limite_inscricao DATE,

    descricao TEXT,

    banner TEXT,

    logo TEXT,

    status VARCHAR(20) DEFAULT 'ABERTO',

    ativo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================
-- CLUBES
-- ==========================================================

CREATE TABLE clubes (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(150) UNIQUE NOT NULL,

    cidade VARCHAR(100),

    estado CHAR(2),

    instagram VARCHAR(150),

    logo TEXT

);

-- ==========================================================
-- PROPRIETÁRIOS
-- ==========================================================

CREATE TABLE proprietarios (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(150) NOT NULL,

    telefone VARCHAR(30),

    email VARCHAR(150),

    cidade VARCHAR(100),

    estado CHAR(2),

    clube_id INTEGER,

    primeira_participacao BOOLEAN DEFAULT TRUE,

    autorizacao_imagem BOOLEAN DEFAULT TRUE,

    observacoes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_clube
        FOREIGN KEY (clube_id)
        REFERENCES clubes(id)

);

-- ==========================================================
-- VEÍCULOS
-- ==========================================================

CREATE TABLE veiculos (

    id SERIAL PRIMARY KEY,

    proprietario_id INTEGER NOT NULL,

    marca VARCHAR(100) NOT NULL,

    modelo VARCHAR(100) NOT NULL,

    ano INTEGER NOT NULL,

    cor VARCHAR(50),

    placa VARCHAR(20) UNIQUE NOT NULL,

    categoria VARCHAR(50),

    foto TEXT,

    descricao TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_proprietario
        FOREIGN KEY (proprietario_id)
        REFERENCES proprietarios(id)

);

-- ==========================================================
-- INSCRIÇÕES
-- ==========================================================

CREATE TABLE inscricoes (

    id SERIAL PRIMARY KEY,

    evento_id INTEGER NOT NULL,

    proprietario_id INTEGER NOT NULL,

    veiculo_id INTEGER NOT NULL,

    numero_inscricao INTEGER UNIQUE,

    quantidade_pessoas INTEGER DEFAULT 1,

    chegada_prevista DATE,

    saida_prevista DATE,

    status VARCHAR(30) DEFAULT 'INSCRITO',

    qrcode TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_evento
        FOREIGN KEY (evento_id)
        REFERENCES eventos(id),

    CONSTRAINT fk_prop
        FOREIGN KEY (proprietario_id)
        REFERENCES proprietarios(id),

    CONSTRAINT fk_veiculo
        FOREIGN KEY (veiculo_id)
        REFERENCES veiculos(id)

);

-- ==========================================================
-- CHECKIN
-- ==========================================================

CREATE TABLE checkin (

    id SERIAL PRIMARY KEY,

    inscricao_id INTEGER NOT NULL,

    usuario_id INTEGER,

    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    observacao TEXT,

    CONSTRAINT fk_checkin
        FOREIGN KEY (inscricao_id)
        REFERENCES inscricoes(id),

    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)

);

-- ==========================================================
-- KITS
-- ==========================================================

CREATE TABLE kits (

    id SERIAL PRIMARY KEY,

    inscricao_id INTEGER NOT NULL,

    kit_entregue BOOLEAN DEFAULT FALSE,

    brinde_entregue BOOLEAN DEFAULT FALSE,

    cafe BOOLEAN DEFAULT FALSE,

    data_entrega TIMESTAMP,

    usuario_id INTEGER,

    CONSTRAINT fk_inscricao_kit
        FOREIGN KEY (inscricao_id)
        REFERENCES inscricoes(id),

    CONSTRAINT fk_usuario_kit
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)

);

-- ==========================================================
-- PREMIAÇÕES
-- ==========================================================

CREATE TABLE premiacoes (

    id SERIAL PRIMARY KEY,

    inscricao_id INTEGER,

    categoria VARCHAR(100),

    colocacao INTEGER,

    observacao TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_premiacao
        FOREIGN KEY (inscricao_id)
        REFERENCES inscricoes(id)

);

-- ==========================================================
-- ÍNDICES
-- ==========================================================

CREATE INDEX idx_prop_nome
ON proprietarios(nome);

CREATE INDEX idx_placa
ON veiculos(placa);

CREATE INDEX idx_evento
ON inscricoes(evento_id);

CREATE INDEX idx_checkin
ON checkin(inscricao_id);

CREATE INDEX idx_clube
ON clubes(nome);