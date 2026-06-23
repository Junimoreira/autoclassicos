import pandas as pd
from database.connection import conectar


def listar_inscricoes():
    conn = conectar()

    if conn is None:
        return pd.DataFrame()

    try:
        query = """
            SELECT
                i.id,
                i.numero_inscricao,
                e.nome AS evento,
                p.nome AS participante,
                v.marca || ' ' || v.modelo AS veiculo,
                v.placa,
                i.quantidade_pessoas,
                i.chegada_prevista,
                i.saida_prevista,
                i.status,
                i.observacoes,
                i.created_at
            FROM inscricoes i
            INNER JOIN eventos e ON e.id = i.evento_id
            INNER JOIN participantes p ON p.id = i.participante_id
            INNER JOIN veiculos v ON v.id = i.veiculo_id
            ORDER BY i.id DESC
        """

        df = pd.read_sql(query, conn)

        if not df.empty:
            df["chegada_prevista"] = pd.to_datetime(df["chegada_prevista"]).dt.strftime("%d-%m-%Y")
            df["saida_prevista"] = pd.to_datetime(df["saida_prevista"]).dt.strftime("%d-%m-%Y")
            df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%d-%m-%Y %H:%M")

        return df

    except Exception as erro:
        print("Erro ao listar inscrições:", erro)
        return pd.DataFrame()

    finally:
        conn.close()


def cadastrar_inscricao(
    evento_id,
    participante_id,
    veiculo_id,
    quantidade_pessoas,
    chegada_prevista,
    saida_prevista,
    observacoes
):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(MAX(numero_inscricao), 0) + 1
            FROM inscricoes
        """)

        numero_inscricao = cursor.fetchone()[0]

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
                observacoes
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
            observacoes
        ))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao cadastrar inscrição:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()


def excluir_inscricao(inscricao_id):
    conn = conectar()

    if conn is None:
        return "Erro de conexão com o banco."

    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM inscricoes
            WHERE id = %s
        """, (inscricao_id,))

        conn.commit()
        return True

    except Exception as erro:
        conn.rollback()
        print("Erro ao excluir inscrição:", erro)
        return str(erro)

    finally:
        cursor.close()
        conn.close()