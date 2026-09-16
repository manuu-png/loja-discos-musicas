from conexao_db import cursor, conexao

# Preço padrão de cada disco
PRECO_DISCO = 180.00


# ============================================================
#   MOSTRAR DISCOS
# ============================================================
def ver_discos():
    print("\n===== DISCOS DISPONÍVEIS =====")

    # rowid é um ID automático que o SQLite cria em toda tabela
    cursor.execute("""
        SELECT rowid, genero, artistas, ano, nome_musica
        FROM discos
        ORDER BY genero, artistas, ano
    """)
    discos = cursor.fetchall()

    if not discos:
        print("Nenhum disco cadastrado.")
        return []

    print(f"{'Nº':<4}{'GÊNERO':<16}{'ARTISTA':<22}{'ANO':<6}{'MÚSICA'}")
    print("-" * 95)
    for d in discos:
        print(f"{d[0]:<4}{d[1]:<16}{d[2]:<22}{d[3]:<6}{d[4]}")

    return discos   # ← devolve a lista para podermos usar depois


# ============================================================
#   COMPRAR DISCOS (carrinho + finalizar)
# ============================================================
def comprar_discos(usuario_id):
    discos = ver_discos()
    if not discos:
        return

    # Transforma a lista em dicionário {rowid: disco}
    # Assim fica fácil achar um disco pelo número digitado
    mapa_discos = {d[0]: d for d in discos}

    carrinho = {}   # {rowid: quantidade}

    while True:
        try:
            num = int(input("\nDigite o Nº do disco (ou 0 para cancelar): "))
        except ValueError:
            print("⚠️  Digite apenas números.")
            continue

        if num == 0:
            print("\n Compra cancelada.")
            return

        if num not in mapa_discos:
            print("⚠️  Número inválido.")
            continue

        # Adiciona ou incrementa no carrinho
        carrinho[num] = carrinho.get(num, 0) + 1
        disco = mapa_discos[num]
        print(f" '{disco[4]}' adicionado ao carrinho!")

        # Pergunta se finaliza
        while True:
            opc = input("Deseja finalizar a compra? (s/n): ").strip().lower()
            if opc in ("s", "n"):
                break
            print("Digite 's' ou 'n'.")

        if opc == "s":
            break

    # =========================
    #   RESUMO DO CARRINHO
    # =========================
    print("\n===== RESUMO DO CARRINHO =====")
    total = 0
    for rowid, qtd in carrinho.items():
        disco = mapa_discos[rowid]
        subtotal = qtd * PRECO_DISCO
        total += subtotal
        print(f"{qtd}x {disco[4]} — {disco[2]}  →  R$ {subtotal:.2f}")

    print("-" * 45)
    print(f"TOTAL: R$ {total:.2f}")

    # =========================
    #   CONFIRMAR RESERVA
    # =========================
    confirmar = input("\nDeseja mesmo reservar esse(s) disco(s)? (s/n): ").strip().lower()

    if confirmar != "s":
        print("\n Reserva cancelada.")
        return

    endereco = input("Digite seu endereço de entrega: ")

    # =========================
    #   SALVAR NO BANCO
    # =========================
    for rowid, qtd in carrinho.items():
        subtotal = qtd * PRECO_DISCO
        cursor.execute("""
            INSERT INTO pedidos (quantidade, endereco, preco, id_usuario)
            VALUES (?, ?, ?, ?)
        """, (qtd, endereco, subtotal, usuario_id))

    conexao.commit()

    print("\n🎵 Reservado com sucesso! Estamos aguardando você! 🎵")


# ============================================================
#   VER ARTISTAS
# ============================================================
def ver_artistas():
    print("\n===== ARTISTAS CADASTRADOS =====")
    cursor.execute("SELECT nome, idade FROM artistas ORDER BY nome")
    artistas = cursor.fetchall()

    if not artistas:
        print("Nenhum artista cadastrado.")
        return

    print(f"{'ARTISTA':<25}{'IDADE'}")
    print("-" * 40)
    for a in artistas:
        print(f"{a[0]:<25}{a[1]}")


# ============================================================
#   VER GÊNEROS
# ============================================================
def ver_generos():
    print("\n===== GÊNEROS MUSICAIS =====")
    cursor.execute("SELECT nome, qtde_discos FROM generos ORDER BY nome")
    generos = cursor.fetchall()

    if not generos:
        print("Nenhum gênero cadastrado.")
        return

    print(f"{'GÊNERO':<20}{'QTD. DISCOS'}")
    print("-" * 40)
    for g in generos:
        print(f"{g[0]:<20}{g[1]}")


# ============================================================
#   MEUS PEDIDOS
# ============================================================
def meus_pedidos(usuario_id):
    print("\n===== MEUS PEDIDOS =====")
    cursor.execute("""
        SELECT quantidade, endereco, preco
        FROM pedidos
        WHERE id_usuario = ?
    """, (usuario_id,))
    pedidos = cursor.fetchall()

    if not pedidos:
        print("Você ainda não fez nenhum pedido.")
        return

    print(f"{'QTD':<6}{'PREÇO':<14}{'ENDEREÇO'}")
    print("-" * 80)
    total = 0
    for p in pedidos:
        total += p[2]
        print(f"{p[0]:<6}R$ {p[2]:<10.2f}{p[1]}")

    print("-" * 80)
    print(f"TOTAL GASTO: R$ {total:.2f}")