-- Active: 1788283864609@@127.0.0.1@5432@discos
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(180) NOT NULL,
    senha VARCHAR(90) NOT NULL
);

CREATE TABLE discos (
    id_discos SERIAL PRIMARY KEY,
    genero VARCHAR(50) NOT NULL,
    artistas VARCHAR(100) NOT NULL,
    ano INTEGER NOT NULL,
    nome_musica VARCHAR(100) NOT NULL
);

CREATE TABLE artistas (
    id_artistas SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade NUMERIC NOT NULL
);

CREATE TABLE generos (
    id_generos SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    qtde_discos NUMERIC NOT NULL
);

CREATE TABLE pedidos (
    id_pedidos SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    quantidade NUMERIC NOT NULL,
    endereco VARCHAR(250) NOT NULL,
    preco DECIMAL NOT NULL,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
