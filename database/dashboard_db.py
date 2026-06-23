from database.connection import conectar


def buscar_resumo_dashboard():
    conn = conectar()

    if conn is None:
        return {
            "eventos": 0,
            "clubes": 0,
            "participantes": 0,
            "veiculos": 0
        }

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM eventos")
        eventos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM clubes")
        clubes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM participantes")
        participantes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM veiculos")
        veiculos = cursor.fetchone()[0]

        return {
            "eventos": eventos,
            "clubes": clubes,
            "participantes": participantes,
            "veiculos": veiculos
        }

    except Exception as erro:
        print("Erro ao buscar resumo dashboard:", erro)

        return {
            "eventos": 0,
            "clubes": 0,
            "participantes": 0,
            "veiculos": 0
        }

    finally:
        cursor.close()
        conn.close()