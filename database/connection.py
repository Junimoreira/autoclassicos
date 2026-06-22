import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def conectar():

    try:

        database_url = os.getenv("DATABASE_URL")

        if database_url:

            print("Conectando ao banco do Render...")
            return psycopg2.connect(database_url)

        print("Conectando ao banco local...")

        return psycopg2.connect(
            host="localhost",
            database="autoclassicos_db",
            user="postgres",
            password="123456",
            port=5432
        )

    except Exception as e:

        print("ERRO CONEXÃO:", e)
        return None