-- =========================================================
-- AUTOCLÁSSICOS
-- Schema Inicial
-- PostgreSQL
-- =========================================================

-- ==========================================
-- USUÁRIOS
-- ==========================================

CREATE TABLE usuarios (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(100) NOT NULL,

    usuario VARCHAR(50) UNIQUE NOT NULL,

    senha VARCHAR(255) NOT NULL,

    ativo BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================================
-- EVENTOS
-- ==========================================

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

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================================
-- CLUBES
-- ==========================================

CREATE TABLE clubes (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(150) UNIQUE NOT NULL,

    cidade VARCHAR(100),

    estado CHAR(2),

    instagram VARCHAR(150),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================================
-- PARTICIPANTES
-- ==========================================

CREATE TABLE participantes (

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

    CONSTRAINT fk_participante_clube
        FOREIGN KEY (clube_id)
        REFERENCES clubes(id)

);

-- ==========================================
-- VEÍCULOS
-- ==========================================

CREATE TABLE veiculos (

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

);

-- ==========================================
-- INSCRIÇÕES
-- ==========================================

CREATE TABLE inscricoes (

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

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_evento
        FOREIGN KEY (evento_id)
        REFERENCES eventos(id),

    CONSTRAINT fk_participante
        FOREIGN KEY (participante_id)
        REFERENCES participantes(id),

    CONSTRAINT fk_veiculo
        FOREIGN KEY (veiculo_id)
        REFERENCES veiculos(id)

);

-- ==========================================
-- CHECKIN
-- ==========================================

CREATE TABLE checkin (

    id SERIAL PRIMARY KEY,

    inscricao_id INTEGER NOT NULL,

    usuario_id INTEGER,

    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    observacao TEXT,

    CONSTRAINT fk_checkin_inscricao
        FOREIGN KEY (inscricao_id)
        REFERENCES inscricoes(id),

    CONSTRAINT fk_checkin_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)

);

-- ==========================================
-- ENTREGA DE KITS
-- ==========================================

CREATE TABLE kits (

    id SERIAL PRIMARY KEY,

    inscricao_id INTEGER NOT NULL,

    kit_entregue BOOLEAN DEFAULT FALSE,

    brinde_entregue BOOLEAN DEFAULT FALSE,

    data_entrega TIMESTAMP,

    usuario_id INTEGER,

    CONSTRAINT fk_kit_inscricao
        FOREIGN KEY (inscricao_id)
        REFERENCES inscricoes(id),

    CONSTRAINT fk_kit_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)

);

-- ==========================================
-- PREMIAÇÕES
-- ==========================================

CREATE TABLE premiacoes (

    id SERIAL PRIMARY KEY,

    inscricao_id INTEGER NOT NULL,

    categoria VARCHAR(100),

    colocacao INTEGER,

    observacao TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_premiacao
        FOREIGN KEY (inscricao_id)
        REFERENCES inscricoes(id)

);

-- ==========================================
-- ÍNDICES
-- ==========================================

CREATE INDEX idx_participante_nome
ON participantes(nome);

CREATE INDEX idx_veiculo_placa
ON veiculos(placa);

CREATE INDEX idx_inscricao_evento
ON inscricoes(evento_id);

CREATE INDEX idx_inscricao_status
ON inscricoes(status);

CREATE INDEX idx_checkin
ON checkin(inscricao_id);

CREATE INDEX idx_clube
ON clubes(nome);