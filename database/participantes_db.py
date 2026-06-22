import pandas as pd
from database.connection import conectar


def listar_participantes():
    conn = conectar()

    if conn is None:
        return pd.DataFrame()

    try:
        query = """
            SELECT
                p.id,
                p.nome,
                p.telefone,
                p.email,
                p.cidade,
                p.estado,
                c.nome AS clube,
                p.clube_id,
                p.primeira_participacao,
                p.autorizacao_imagem,
                p.observacoes,
                p.created_at
            FROM participantes p
            LEFT JOIN clubes c ON c.id = p.clube_id
            ORDER BY p.nome
        """

        return pd.read_sql(query, conn)

    except Exception as erro:
        print("Erro ao listar participantes:", erro)
        return pd.DataFrame()

    finally:
        conn.close()


def cadastrar_participante(
    nome,
    telefone,
    email,
    cidade,
    estado,
    clube_id,
    primeira_participacao,
    autorizacao_imagem,
    observacoes
):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

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
        """, (
            nome,
            telefone,
            email,
            cidade,
            estado,
            clube_id,
            primeira_participacao,
            autorizacao_imagem,
            observacoes
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao cadastrar participante:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def atualizar_participante(
    participante_id,
    nome,
    telefone,
    email,
    cidade,
    estado,
    clube_id,
    primeira_participacao,
    autorizacao_imagem,
    observacoes
):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE participantes
            SET
                nome = %s,
                telefone = %s,
                email = %s,
                cidade = %s,
                estado = %s,
                clube_id = %s,
                primeira_participacao = %s,
                autorizacao_imagem = %s,
                observacoes = %s
            WHERE id = %s
        """, (
            nome,
            telefone,
            email,
            cidade,
            estado,
            clube_id,
            primeira_participacao,
            autorizacao_imagem,
            observacoes,
            participante_id
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao atualizar participante:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def excluir_participante(participante_id):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM participantes
            WHERE id = %s
        """, (participante_id,))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao excluir participante:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()