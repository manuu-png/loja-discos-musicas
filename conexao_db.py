import psycopg2
from psycopg2 import Error


def obter_conexao():
    try:
        # Substitua a URL abaixo pela URL inteira que você copiou do painel do Neon
        url_neon = "postgresql://neondb_owner:npg_NSpLBKD0w9qh@ep-damp-unit-be1a0tqt-pooler.c-9.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

        conexao = psycopg2.connect(url_neon)
        return conexao
    except Error as error:
        print('Erro ao conectar ao PostgreSQL no Neon:', error)
        return None