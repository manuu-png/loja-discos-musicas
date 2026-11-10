import psycopg2
from psycopg2 import Error

def obter_conexao():
    try:
        conexao = psycopg2.connect(
            host='localhost',
            database='discos',
            user='postgres',
            password='1234',
            port=5432
        )
        return conexao
    except Error as error:
        print('Erro ao conectar ao PostgreSQL:', error)
        return None
