SELECT * FROM usuarios;

UPDATE usuarios 
SET nome = 'Luiza Terto Da Silva', 
    email = 'tertoluiza@gmail.com', 
    senha = '310708Lu'
WHERE id_usuario = 1;

SELECT * FROM discos;

SELECT * FROM artistas;

SELECT * FROM generos;

DELETE FROM generos WHERE id_generos = 6;

SELECT * FROM pedidos;
