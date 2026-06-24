import uuid

from database.connection import conectar


def cadastrar_inscricao_publica(
    evento_id,
    nome,
    telefone,
    email,
    cidade,
    estado,
    clube_id,
    primeira_participacao,
    autorizacao_imagem,
    observacoes_participante,
    marca,
    modelo,
    ano,
    cor,
    placa,
    categoria,
    quantidade_pessoas,
    chegada_prevista,
    saida_prevista
):

    conn = conectar()

    if conn is None:
        return False, "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO participantes (
                nome,
                telefone,
                email,
                cidade,
                estado,
                clube_id,
                primeira_participacao,
                autorizacao_imagem,
                observacoes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            nome,
            telefone,
            email,
            cidade,
            estado,
            clube_id,
            primeira_participacao,
            autorizacao_imagem,
            observacoes_participante
        ))

        participante_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO veiculos (
                participante_id,
                marca,
                modelo,
                ano,
                cor,
                placa,
                categoria
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            participante_id,
            marca,
            modelo,
            ano,
            cor,
            placa,
            categoria
        ))

        veiculo_id = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(MAX(numero_inscricao), 0) + 1
            FROM inscricoes
        """)

        numero_inscricao = cursor.fetchone()[0]

        uuid_qrcode = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO inscricoes (
                evento_id,
                participante_id,
                veiculo_id,
                numero_inscricao,
                quantidade_pessoas,
                chegada_prevista,
                saida_prevista,
                status,
                uuid_qrcode
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            evento_id,
            participante_id,
            veiculo_id,
            numero_inscricao,
            quantidade_pessoas,
            chegada_prevista,
            saida_prevista,
            "INSCRITO",
            uuid_qrcode
        ))

        conn.commit()

        return True, {
            "numero_inscricao": numero_inscricao,
            "uuid_qrcode": uuid_qrcode
        }

    except Exception as erro:
        conn.rollback()
        print("Erro inscrição pública:", erro)
        return False, str(erro)

    finally:
        cursor.close()
        conn.close()