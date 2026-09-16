from login import login
from conexao_db import conexao
from funcoes_menu import (
    ver_discos,
    ver_artistas,
    ver_generos,
    comprar_discos,
    meus_pedidos,
)


def menu_principal():
    print("\n==============================")
    print("       MENU PRINCIPAL")
    print("==============================")
    print("1 - Comprar discos")
    print("2 - Ver artistas")
    print("3 - Ver gêneros")
    print("4 - Meus pedidos")
    print("0 - Sair")


def main():
    usuario = login()
    if not usuario:
        print("\nEncerrando...")
        return

    usuario_id = usuario[0]   # ID do usuário logado

    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            comprar_discos(usuario_id)
        elif opcao == "2":
            ver_artistas()
        elif opcao == "3":
            ver_generos()
        elif opcao == "4":
            meus_pedidos(usuario_id)
        elif opcao == "0":
            print("\nSaindo da loja...")
            break
        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    try:
        main()
    finally:
        conexao.close()