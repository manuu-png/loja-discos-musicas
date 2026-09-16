import sqlite3

conexao = sqlite3.connect("discos.db") #funções do banco
cursor = conexao.cursor()