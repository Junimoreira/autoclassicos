import pandas as pd
from database.connection import conectar


def listar_eventos():
    conn = conectar()

    if conn is None:
        return pd.DataFrame()

    try:
        query = """
            SELECT
                id,
                nome,
                cidade,
                estado,
                local_evento,
                data_inicio,
                data_fim,
                descricao,
                ativo,
                created_at
            FROM eventos
            ORDER BY id DESC
        """

        return pd.read_sql(query, conn)

    except Exception as erro:
        print("Erro ao listar eventos:", erro)
        return pd.DataFrame()

    finally:
        conn.close()


def cadastrar_evento(
    nome,
    cidade,
    estado,
    local_evento,
    data_inicio,
    data_fim,
    descricao,
    ativo=True
):
    conn = conectar()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO eventos (
                nome,
                cidade,
                estado,
                local_evento,
                data_inicio,
                data_fim,
                descricao,
                ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nome,
            cidade,
            estado,
            local_evento,
            data_inicio,
            data_fim,
            descricao,
            ativo
        ))

        conn.commit()
        return True

    except Exception as erro:
        print("Erro ao cadastrar evento:", erro)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


def atualizar_evento(
    evento_id,
    nome,
    cidade,
    estado,
    local_evento,
    data_inicio,
    data_fim,
    descricao,
    ativo
):
    conn = conectar()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE eventos
            SET
                nome = %s,
                cidade = %s,
                estado = %s,
                local_evento = %s,
                data_inicio = %s,
                data_fim = %s,
                descricao = %s,
                ativo = %s
            WHERE id = %s
        """, (
            nome,
            cidade,
            estado,
            local_evento,
            data_inicio,
            data_fim,
            descricao,
            ativo,
            evento_id
        ))

        conn.commit()
        return True

    except Exception as erro:
        print("Erro ao atualizar evento:", erro)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


def excluir_evento(evento_id):
    conn = conectar()

    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM eventos
            WHERE id = %s
        """, (evento_id,))

        conn.commit()
        return True

    except Exception as erro:
        print("Erro ao excluir evento:", erro)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()