import pandas as pd
from database.connection import conectar


def listar_veiculos():
    conn = conectar()

    if conn is None:
        return pd.DataFrame()

    try:
        query = """
            SELECT
                v.id,
                p.nome AS participante,
                v.participante_id,
                v.marca,
                v.modelo,
                v.ano,
                v.cor,
                v.placa,
                v.categoria,
                v.foto,
                v.descricao,
                v.created_at
            FROM veiculos v
            INNER JOIN participantes p ON p.id = v.participante_id
            ORDER BY v.id DESC
        """

        return pd.read_sql(query, conn)

    except Exception as erro:
        print("Erro ao listar veículos:", erro)
        return pd.DataFrame()

    finally:
        conn.close()


def cadastrar_veiculo(
    participante_id,
    marca,
    modelo,
    ano,
    cor,
    placa,
    categoria,
    foto,
    descricao
):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO veiculos (
                participante_id,
                marca,
                modelo,
                ano,
                cor,
                placa,
                categoria,
                foto,
                descricao
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            participante_id,
            marca,
            modelo,
            ano,
            cor,
            placa,
            categoria,
            foto,
            descricao
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao cadastrar veículo:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def atualizar_veiculo(
    veiculo_id,
    participante_id,
    marca,
    modelo,
    ano,
    cor,
    placa,
    categoria,
    foto,
    descricao
):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE veiculos
            SET
                participante_id = %s,
                marca = %s,
                modelo = %s,
                ano = %s,
                cor = %s,
                placa = %s,
                categoria = %s,
                foto = %s,
                descricao = %s
            WHERE id = %s
        """, (
            participante_id,
            marca,
            modelo,
            ano,
            cor,
            placa,
            categoria,
            foto,
            descricao,
            veiculo_id
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao atualizar veículo:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def excluir_veiculo(veiculo_id):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM veiculos
            WHERE id = %s
        """, (veiculo_id,))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao excluir veículo:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()