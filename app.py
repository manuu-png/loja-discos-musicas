from flask import Flask, render_template, request, redirect, url_for, session
from conexao_db import obter_conexao
import random

app = Flask(__name__)
app.secret_key = 'opera_records_secret_key'

# Carrinho global temporário por ID de usuário
carrinhos = {}

CAPAS_DISCOS = {
    # Rock Clássico
    'There Is a Light That Never Goes Out': 'https://e.snmc.io/i/600/w/d3844354372312f6e84e75dad1380cc4/14780388/The%20Smiths%20-%20The%20Queen%20Is%20Dead%2C%20Cover%20art.webp',
    "Don't Let Me Down": 'https://e.snmc.io/i/600/w/8bb7f1adb1dd815246336a9d460693d8/11462750/The%20Beatles%20-%20Let%20It%20Be___%20Naked%2C%20Cover%20art.webp',
    'Wonderwall': 'https://e.snmc.io/i/600/w/b50cc50216ed09a729cc0cdf730f37b6/13246079/Oasis%20-%20(Whats%20the%20Story)%20Morning%20Glory%3F%2C%20Cover%20art.webp',
    'Under Pressure': 'https://upload.wikimedia.org/wikipedia/en/3/3c/Queen_Hot_Space.png',  # Corrigido (.space.jpg -> .png)
    'I Thought I Saw Your Face Today': 'https://upload.wikimedia.org/wikipedia/en/8/82/She_%26_Him_-_Volume_One.png',
    'Forget Her': 'https://upload.wikimedia.org/wikipedia/en/b/b5/JeffBuckleyGrace.jpg',
    'Every Breath You Take': 'https://upload.wikimedia.org/wikipedia/en/3/39/The_Police_-_Synchronicity_%28album_cover%29.png',
    'Half a Person': 'https://upload.wikimedia.org/wikipedia/en/2/25/The_Queen_Is_Dead_cover.png',
    'Oh! Darling': 'https://upload.wikimedia.org/wikipedia/en/4/42/Beatles_-_Abbey_Road.jpg',
    'Hey Jude': 'https://upload.wikimedia.org/wikipedia/en/f/f9/The_Beatles_1_cover.svg',  # Substituído por SVG oficial válido do álbum 1

    # Rock Metal
    'Kickstart My Heart': 'https://upload.wikimedia.org/wikipedia/en/f/f8/Motley_crue_dr_feelgood.jpg',
    'Paradise City': 'https://upload.wikimedia.org/wikipedia/en/a/a3/GunsnRosesAppetiteforDestructionalbumcover.jpg',
    'Lithium': 'https://upload.wikimedia.org/wikipedia/en/b/b7/NirvanaNevermindalbumcover.jpg',
    'Master of Puppets': 'https://upload.wikimedia.org/wikipedia/en/b/b2/Metallica_-_Master_of_Puppets_cover.jpg',
    'Back in Black': 'https://upload.wikimedia.org/wikipedia/commons/3/3e/ACDC_Back_in_Black_cover.svg',
    'Change (In the House of Flies)': 'https://upload.wikimedia.org/wikipedia/en/f/fb/Deftones_-_White_Pony_%28album_cover%29.png',
    "Sweet Child O' Mine": 'https://upload.wikimedia.org/wikipedia/en/a/a3/GunsnRosesAppetiteforDestructionalbumcover.jpg',
    'Enter Sandman': 'https://upload.wikimedia.org/wikipedia/en/2/2c/Metallica_Metallica_cover.jpg',
    'Heart-Shaped Box': 'https://upload.wikimedia.org/wikipedia/en/7/76/Nirvana-In_Utero_album_cover.jpg',
    'Highway to Hell': 'https://upload.wikimedia.org/wikipedia/en/a/ad/ACDC_Highway_to_Hell.JPG',

    # MPB
    'Ainda Bem': 'https://upload.wikimedia.org/wikipedia/pt/c/c9/O_Que_Voc%C3%AA_Quer_Saber_de_Verdade.jpg',
    'Baby': 'https://upload.wikimedia.org/wikipedia/pt/f/f6/Gal_Costa_1969.jpg',
    'Lança Perfume': 'https://upload.wikimedia.org/wikipedia/pt/4/4d/Rita_Lee_1980.jpg',
    'Oceano': 'https://upload.wikimedia.org/wikipedia/pt/3/33/Djavan_DJAVAN_1989.jpg',
    'Mas Que Nada': 'https://upload.wikimedia.org/wikipedia/en/b/b6/Jorge_Ben_-_Samba_Esquema_Novo.jpg',
    'Velha Infância': 'https://upload.wikimedia.org/wikipedia/pt/a/a2/Tribalistas_-_Tribalistas_%282002%29.jpg',
    'Beija Eu': 'https://e.snmc.io/i/600/w/e20b58f090bc64b66b9a05a7e1549041/2739771/Marisa%20Monte%20-%20Mais%2C%20Cover%20art.webp',
    'Lanterna dos Afogados': 'https://upload.wikimedia.org/wikipedia/pt/5/52/Gal_Costa_-_Ac%C3%BAstico_MTV_%28Capa%29.jpg',
    'Mania de Você': 'https://upload.wikimedia.org/wikipedia/pt/6/6f/Rita_Lee_-_Rita_Lee_%281979%29.jpg',
    'Taj Mahal': 'https://upload.wikimedia.org/wikipedia/en/5/5e/Jorge_Ben_-_A_Tabua_de_Esmeralda.jpg',

    # Pop
    'The Way I Loved You': 'https://upload.wikimedia.org/wikipedia/en/8/86/Taylor_Swift_-_Fearless.png',
    'Red': 'https://upload.wikimedia.org/wikipedia/en/e/e8/Taylor_Swift_-_Red.png',
    'Champagne Problems': 'https://upload.wikimedia.org/wikipedia/en/3/39/Taylor_Swift_-_Evermore.png',
    'New Romantics': 'https://upload.wikimedia.org/wikipedia/en/f/f6/Taylor_Swift_-_1989.png',
    'Drivers License': 'https://upload.wikimedia.org/wikipedia/en/b/b2/Olivia_Rodrigo_-_Sour.png',
    'Thank U, Next': 'https://upload.wikimedia.org/wikipedia/en/d/dd/Ariana_Grande_-_Thank_U_Next_album_cover.png',
    'As It Was': 'https://upload.wikimedia.org/wikipedia/en/e/e1/Harry_Styles_-_Harry%27s_House.png',
    'What Makes You Beautiful': 'https://upload.wikimedia.org/wikipedia/en/1/1c/One_Direction_-_Up_All_Night_%28US_Album_Cover%29.png',
    'Baby': 'https://upload.wikimedia.org/wikipedia/en/d/da/Justin_Bieber_-_My_World_2.0.png',
    'Good 4 U': 'https://upload.wikimedia.org/wikipedia/en/b/b2/Olivia_Rodrigo_-_Sour.png',

    # K-Pop
    'Dynamite': 'https://upload.wikimedia.org/wikipedia/en/d/d7/BTS_-_Dynamite.png',
    'DDU-DU DDU-DU': 'https://upload.wikimedia.org/wikipedia/en/7/7b/Blackpink_-_Square_Up.png',
    'Hype Boy': 'https://upload.wikimedia.org/wikipedia/en/d/d0/NewJeans_1st_EP.png',
    'Fancy': 'https://upload.wikimedia.org/wikipedia/en/b/b5/Twice_-_Fancy_You.png',
    'Fever': 'https://upload.wikimedia.org/wikipedia/en/4/42/Enhypen_-_Border_Carnival.png',
    'Butter': 'https://upload.wikimedia.org/wikipedia/en/b/bb/BTS_-_Butter.png',
    'How You Like That': 'https://upload.wikimedia.org/wikipedia/en/a/a2/Blackpink_-_The_Album.png',
    'Ditto': 'https://upload.wikimedia.org/wikipedia/en/f/f6/NewJeans_-_Ditto.png',
    'What Is Love?': 'https://upload.wikimedia.org/wikipedia/en/0/02/Twice_-_What_Is_Love_%28EP%29.png',
    'Bite Me': 'https://upload.wikimedia.org/wikipedia/en/3/36/Enhypen_-_Dark_Blood.png'
}

CAPA_PADRAO = 'https://upload.wikimedia.org/wikipedia/commons/b/b6/12in-Vinyl-LP-Record-Angle.jpg'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT id_usuario, nome, email FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
        usuario = cursor.fetchone()
        cursor.close()
        conexao.close()

        if usuario:
            session['id_usuario'] = usuario[0]
            session['nome'] = usuario[1]
            return redirect(url_for('catalogo'))
        else:
            return render_template('login.html', erro='E-mail ou senha incorretos.')

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        conexao.commit()
        cursor.close()
        conexao.close()

        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/catalogo')
def catalogo():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_discos, genero, artistas, ano, nome_musica FROM discos ORDER BY id_discos")
    discos_raw = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Criamos uma versão do dicionário com as chaves em minúsculas e sem espaços nas pontas para facilitar a busca
    capas_normalizadas = {k.strip().lower(): v for k, v in CAPAS_DISCOS.items()}

    random.seed(42)
    discos = []
    for d in discos_raw:
        preco = round(random.uniform(180.00, 200.00), 2)

        # Pega o nome da música do banco e normaliza para comparar com segurança
        nome_musica_db = str(d[4]).strip().lower() if d[4] else ""
        imagem_url = capas_normalizadas.get(nome_musica_db, CAPA_PADRAO)

        discos.append({
            'id': d[0],
            'genero': d[1],
            'artista': d[2],
            'ano': d[3],
            'musica': d[4],
            'preco': preco,
            'imagem': imagem_url
        })

    return render_template('catalogo.html', discos=discos, nome=session['nome'])


@app.route('/artistas')
def artistas():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_artistas, nome, idade FROM artistas ORDER BY nome")
    lista_artistas = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('artistas.html', artistas=lista_artistas, nome=session['nome'])


@app.route('/generos')
def generos():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_generos, nome, qtde_discos FROM generos ORDER BY nome")
    lista_generos = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('generos.html', generos=lista_generos, nome=session['nome'])


@app.route('/adicionar_carrinho/<int:id_disco>', methods=['POST'])
def adicionar_carrinho(id_disco):
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['id_usuario']
    if usuario_id not in carrinhos:
        carrinhos[usuario_id] = {}

    carrinhos[usuario_id][id_disco] = carrinhos[usuario_id].get(id_disco, 0) + 1
    return redirect(url_for('ver_carrinho'))


@app.route('/carrinho')
def ver_carrinho():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['id_usuario']
    itens_carrinho = carrinhos.get(usuario_id, {})

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_discos, genero, artistas, ano, nome_musica FROM discos")
    todos_discos = {d[0]: {'genero': d[1], 'artista': d[2], 'ano': d[3], 'musica': d[4]} for d in cursor.fetchall()}
    cursor.close()
    conexao.close()

    random.seed(42)
    carrinho_detalhado = []
    total_discos = 0

    for id_disco, qtd in itens_carrinho.items():
        if id_disco in todos_discos:
            d = todos_discos[id_disco]
            preco_unitario = round(random.uniform(180.00, 200.00), 2)
            subtotal = qtd * preco_unitario
            total_discos += subtotal

            carrinho_detalhado.append({
                'id': id_disco,
                'musica': d['musica'],
                'artista': d['artista'],
                'quantidade': qtd,
                'preco': preco_unitario,
                'subtotal': subtotal
            })

    total_com_taxa = total_discos + (5.00 if carrinho_detalhado else 0.00)

    return render_template(
        'carrinho.html',
        carrinho=carrinho_detalhado,
        total=total_discos,
        total_com_taxa=total_com_taxa,
        nome=session['nome']
    )


@app.route('/finalizar_carrinho', methods=['POST'])
def finalizar_carrinho():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    usuario_id = session['id_usuario']
    itens_carrinho = carrinhos.get(usuario_id, {})

    if not itens_carrinho:
        return redirect(url_for('catalogo'))

    endereco = request.form['endereco']
    pagamento = request.form['pagamento']

    total_geral = 0
    total_qtd = 0
    random.seed(42)

    for id_disco, qtd in itens_carrinho.items():
        preco_unitario = round(random.uniform(180.00, 200.00), 2)
        total_geral += qtd * preco_unitario
        total_qtd += qtd

    total_com_taxa = total_geral + 5.00

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO pedidos (id_usuario, quantidade, endereco, preco) VALUES (%s, %s, %s, %s)",
        (usuario_id, total_qtd, f"{endereco} | Pagto: {pagamento} (Taxa entrega R$ 5,00)", total_com_taxa)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    carrinhos[usuario_id] = {}
    return render_template('confirmado.html', nome=session['nome'])


@app.route('/pedidos')
def pedidos():
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT quantidade, endereco, preco FROM pedidos WHERE id_usuario = %s", (session['id_usuario'],))
    meus_pedidos = cursor.fetchall()
    cursor.close()
    conexao.close()

    total_gasto = sum(p[2] for p in meus_pedidos)
    return render_template('pedidos.html', pedidos=meus_pedidos, total_gasto=total_gasto, nome=session['nome'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)