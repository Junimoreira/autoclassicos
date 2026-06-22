import pandas as pd
from database.connection import conectar


def listar_clubes():
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
                COALESCE(instagram, '') AS instagram,
                created_at
            FROM clubes
            ORDER BY nome
        """

        return pd.read_sql(query, conn)

    except Exception as erro:
        print("Erro ao listar clubes:", erro)
        return pd.DataFrame()

    finally:
        conn.close()


def cadastrar_clube(nome, cidade, estado, instagram):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO clubes (
                nome,
                cidade,
                estado,
                instagram
            )
            VALUES (%s, %s, %s, %s)
        """, (
            nome,
            cidade,
            estado,
            instagram
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao cadastrar clube:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def atualizar_clube(clube_id, nome, cidade, estado, instagram):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE clubes
            SET
                nome = %s,
                cidade = %s,
                estado = %s,
                instagram = %s
            WHERE id = %s
        """, (
            nome,
            cidade,
            estado,
            instagram,
            clube_id
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao atualizar clube:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def excluir_clube(clube_id):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM clubes
            WHERE id = %s
        """, (clube_id,))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao excluir clube:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()