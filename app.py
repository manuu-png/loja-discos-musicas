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
    'I Thought I Saw Your Face Today': ' https://e.snmc.io/i/600/w/a633633bbe6ded3bbec6e5ab7728318b/11361882/She%20%26%20Him%20-%20Volume%20One%2C%20Cover%20art.webp ',
    'Forget Her': ' https://cdn.sonemic.net/i/600/w/7409d01a8c0cdf51e8b22fd5d055196a/7027387/jeff-buckley-grace-cover-art.jpg ',
    'Every Breath You Take': ' https://e.snmc.io/i/600/w/b9094b1e9af09bbd4589232d1afd0338/6576413/The%20Police%20-%20Synchronicity%2C%20Cover%20art.webp ',
    'Half a Person': ' https://e.snmc.io/i/600/w/c9c371eaa8d9d50f78c77261fccaeab2/10758251/The%20Smiths%20-%20Louder%20Than%20Bombs%2C%20Cover%20art.webp ',
    'Oh! Darling': ' https://e.snmc.io/i/600/w/5bb35099a69ff9f43e389a683b568a64/10910535/The%20Beatles%20-%201%2C%20Cover%20art.webp ',
    'Hey Jude': ' https://e.snmc.io/i/600/w/5bb35099a69ff9f43e389a683b568a64/10910535/The%20Beatles%20-%201%2C%20Cover%20art.webp ',  # Substituído por SVG oficial válido do álbum 1

    # Rock Metal
    'Kickstart My Heart': ' https://e.snmc.io/i/600/w/d5f5b285e3d522841da3448c8798a7b0/13243854/M%C3%B6tley%20Cr%C3%BCe%20-%20Dr_%20Feelgood%2C%20Cover%20art.webp ',
    'Paradise City': ' https://e.snmc.io/i/600/w/039a716a80dab8af32de9b6dcd3fb820/1212432/Guns%20n%20Roses%20-%20Live%20Era%20''93%2C%20Cover%20art.webp ',
    'Lithium': ' https://e.snmc.io/i/600/w/9897668139794df98998dbb82997ba94/7748503/Nirvana%20-%20From%20the%20Muddy%20Banks%20of%20the%20Wishkah%2C%20Cover%20art.webp ',
    'Master of Puppets': ' https://cdn.sonemic.net/i/600/w/280060a11fb6a67d6ac86d54f2e83cc6/3986151/metallica-master-of-puppets-Cover-Art.jpg ',
    'Back in Black': ' https://cdn.sonemic.net/i/600/w/d1283369d34e034a87a9303c93794fc4/14309818/ac_dc-girls-got-rhythm-t_n_t-cover-art.jpg ',
    'Change (In the House of Flies)': ' https://cdn.sonemic.net/i/150/w/119748a8aa656a0f10ec564132c98700/5146207',
    "Sweet Child O' Mine": ' https://e.snmc.io/i/600/w/039a716a80dab8af32de9b6dcd3fb820/1212432/Guns%20n%20Roses%20-%20Live%20Era%20''93%2C%20Cover%20art.webp ',
    'Enter Sandman': ' https://cdn.sonemic.net/i/600/w/282d2361441e9060d9c4b4e46732540c/6902962/metallica-enter-sandman-Cover-Art.jpg ',
    'Heart-Shaped Box': ' https://cdn.sonemic.net/i/600/w/8447b62663fd973da77b0ddf9b06dc28/1631430/nirvana-heart-shaped-box-Cover-Art.jpg ',
    'Highway to Hell': ' https://cdn.sonemic.net/i/600/w/1269aec9b07dc87753c72e8e19341536/1275719/ac_dc-highway-to-hell-Cover-Art.jpg ',

    # MPB
    'Ainda Bem': ' https://e.snmc.io/i/600/w/08614152d937b3f5987d8ad89638707b/3926789/Marisa%20Monte%20-%20O%20que%20voc%C3%AA%20quer%20saber%20de%20verdade%2C%20Cover%20art.webp ',
    'Baby - Gal costa': ' https://e.snmc.io/i/600/w/9e6cf2c2b36b84cd7e1ce51197f720fe/3089291/Gal%20Costa%20-%20Gal%20Costa%2C%20Cover%20art.webp ',
    'Lança Perfume': ' https://cdn.sonemic.net/i/600/w/9cf7eb2c497a4a7bde96d43c95ee83d4/10988921/rita-lee-e-roberto-de-carvalho-rita-lee-e-roberto-de-carvalho-cover-art.jpg ',
    'Oceano': ' https://e.snmc.io/i/600/w/ccb28e14f4940db6ac5a49ed9c86bee1/12176606/Djavan%20-%20Djavan%2C%20Cover%20art.webp ',
    'Mas Que Nada': ' https://e.snmc.io/i/600/w/5c93523cabe48d0eb607590a276967f3/12319633/Jorge%20Ben%20-%20Samba%20esquema%20novo%2C%20Cover%20art.webp ',
    'Velha Infância': ' https://e.snmc.io/i/600/w/1aad40671dc50aa01dbb873e09b76fd1/2138881/Tribalistas%20-%20Tribalistas%2C%20Cover%20art.webp ',
    'Beija Eu': 'https://e.snmc.io/i/600/w/e20b58f090bc64b66b9a05a7e1549041/2739771/Marisa%20Monte%20-%20Mais%2C%20Cover%20art.webp',
    'Lanterna dos Afogados': 'https://e.snmc.io/i/600/w/9e6cf2c2b36b84cd7e1ce51197f720fe/3089291/Gal%20Costa%20-%20Gal%20Costa%2C%20Cover%20art.webp',
    'Mania de Você': 'https://e.snmc.io/i/600/w/ab2f480d032995ae222afe87f3a6248d/10996825/Rita%20Lee%20-%20Rita%20Lee%2C%20Cover%20art.webp',
    'Taj Mahal': 'https://e.snmc.io/i/600/w/7878904bac16d76c7d19e1ac7481b808/8671710/Gil%20e%20Jorge%20-%20Ogum%20Xang%C3%B4%2C%20Cover%20art.webp',

    # Pop
    'The Way I Loved You': 'https://upload.wikimedia.org/wikipedia/en/8/86/Taylor_Swift_-_Fearless.png',
    'Red': 'https://upload.wikimedia.org/wikipedia/en/e/e8/Taylor_Swift_-_Red.png',
    'Champagne Problems': 'https://e.snmc.io/i/600/w/8064a5c42ddb795c67f8c97e0b09e6b2/11472566/Taylor%20Swift%20-%20Evermore%2C%20Cover%20art.webp',
    'New Romantics': 'https://upload.wikimedia.org/wikipedia/en/f/f6/Taylor_Swift_-_1989.png',
    'Drivers License': 'https://e.snmc.io/i/600/w/80ac9e81852c2ffa2c15bd12c5f88fdb/8937386/Olivia%20Rodrigo%20-%20Sour%2C%20Cover%20art.webp',
    'Thank U, Next': 'https://e.snmc.io/i/600/w/f6c304d2bd54aa990cf448a47ad66523/7372303/Ariana%20Grande%20-%20Thank%20U%2C%20Next%2C%20Cover%20art.webp',
    'As It Was': 'https://e.snmc.io/i/600/w/045e073ad2745cc89b2eec52fdac4e7b/11432066/Harry%20Styles%20-%20Harrys%20House%2C%20Cover%20art.webp',
    'What Makes You Beautiful': 'https://e.snmc.io/i/600/w/12cb522433bdd9b0ae52f5d6ebc292d3/3918645/One%20Direction%20-%20Up%20All%20Night%2C%20Cover%20art.webp',
    'Baby': 'https://e.snmc.io/i/600/w/2b0b0e63730abde53d32b1a1ae44cb4f/2999424/Justin%20Bieber%20-%20My%20World%202_0%2C%20Cover%20art.webp',
    'Good 4 U': 'https://e.snmc.io/i/600/w/80ac9e81852c2ffa2c15bd12c5f88fdb/8937386/Olivia%20Rodrigo%20-%20Sour%2C%20Cover%20art.webp',

    # K-Pop
    'Dynamite': 'https://cdn.sonemic.net/i/600/w/9b93f1246c6607e9261e44000e8da8e0/8402287/bts-dynamite-Cover-Art.jpg',
    'DDU-DU DDU-DU': 'https://cdn.sonemic.net/i/600/w/c7428525e58eccff4484d36013a8572e/7091047/blackpink-ddu-du-ddu-du-Cover-Art.png',
    'Hype Boy': 'https://e.snmc.io/i/600/w/20f94342f5dcf0328d6d180e0eb7230d/10143111/NewJeans%20-%20New%20Jeans%2C%20Cover%20art.webp',
    'Fancy': 'https://e.snmc.io/i/600/w/f9ff3c9256c5fd4246656ff0731f3420/13508205/TWICE%20-%20Fancy%20You%2C%20Cover%20art.webp',
    'Fever': 'https://e.snmc.io/i/600/w/0d1c0109ffff353bca8e620c4addec26/8969136/ENHYPEN%20-%20Border%20%3A%20Carnival%2C%20Cover%20art.webp',
    'Butter': 'https://cdn.sonemic.net/i/600/w/7f0810e2d253d1ec9be93cf133d91ac6/9032901/bts-butter-Cover-Art.jpg',
    'How You Like That': 'https://cdn.sonemic.net/i/600/w/99f3d340e388771b2f95948d207c1e4a/8284281/blackpink-how-you-like-that-Cover-Art.jpg',
    'Ditto': 'https://cdn.sonemic.net/i/600/w/a3812f6f610b392631049f6a58d071a5/10524472/newjeans-ditto-Cover-Art.jpg',
    'What Is Love?': 'https://cdn.sonemic.net/i/600/w/a0228c43956c2b740614634325a07bc0/6944003/twice-what-is-love-Cover-Art.jpg',
    'Bite Me': 'https://e.snmc.io/i/600/w/128933bd253bd5d9d5a730f80424a367/10995431/ENHYPEN%20-%20Dark%20Blood%2C%20Cover%20art.webp'
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