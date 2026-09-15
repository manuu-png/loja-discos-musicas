SELECT * FROM usuarios;

UPDATE usuarios 
SET nome = 'Sarah Muniz', 
    email = 'Sarahmza@gmail.com', 
    senha = '30112009'
WHERE id_usuario = 1;

SELECT * FROM discos;

SELECT * FROM artistas;

SELECT * FROM generos;

DELETE FROM generos WHERE id_generos = 6;

SELECT * FROM pedidos;
