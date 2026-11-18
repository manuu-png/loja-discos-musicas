# loja-discos-musicas
Projeto do Banco de Dados para a Gran Opera Records
🎵 Opera Records — Loja de Discos de Vinil

O Opera Records é uma aplicação web desenvolvida em Python com Flask para uma loja virtual especializada em discos de vinil. O sistema permite que os clientes naveguem pelo catálogo, filtrem músicas e artistas, adicionem discos ao carrinho, calculem o endereço automaticamente via CEP e gerem relatórios de pedidos em PDF.

✨ Funcionalidades

Autenticação de Usuários: Sistema completo de cadastro e login com controle de sessão.

Catálogo Interativo: Exibição de discos com capas personalizadas, preços dinâmicos e barra de pesquisa em tempo real.

Exploração por Categorias: Páginas dedicadas para listagem de Artistas (com tabela interativa via DataTables) e Gêneros Musicais.

Carrinho de Compras: Adição de múltiplos discos, cálculo automático de subtotal e inclusão de taxa fixa de entrega (prazo de até 48 horas).

Checkout Inteligente:

Busca automática de endereço através da API ViaCEP.

Opções de pagamento (Cartão, Dinheiro e Pix com geração automática de QR Code).

Histórico e Relatórios em PDF: Consulta de pedidos realizados e exportação de relatório detalhado em formato .pdf utilizando a biblioteca FPDF.

🛠️ Tecnologias Utilizadas

Back-end: Python 3, Flask

Banco de Dados: PostgreSQL (hospedado no Neon)

Bibliotecas e APIs Externas:

Materialize CSS / Material Icons (ícones e elementos visuais)

DataTables (paginação e busca na tabela de artistas)

FPDF2 (geração de relatórios em PDF)

ViaCEP API (preenchimento automático de endereço)
