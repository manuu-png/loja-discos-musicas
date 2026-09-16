from conexao_db import conexao, cursor


def criar_conta():
    print("\n===== CRIAR CONTA =====")

    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha)
        VALUES (?, ?, ?)
    """, (nome, email, senha))

    conexao.commit()
    print("\nConta criada com sucesso!")
    return True   # 👈 importante retornar algo


def login():
    print("\n===== LOGIN =====")

    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE nome = ? AND email = ? AND senha = ?
    """, (nome, email, senha))

    usuario = cursor.fetchone()

    if usuario:
        print(f"\nBem-vindo(a), {usuario[1]}!")
        return usuario          # 👈 retorna a linha toda
    else:
        print("\nUsuário não encontrado.")
        opcao = input("Deseja criar uma conta? (s/n): ")
        if opcao.lower() == "s":
            criar_conta()
            return login()      # tenta logar de novo
        return None