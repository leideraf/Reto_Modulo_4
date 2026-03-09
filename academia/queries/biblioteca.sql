-- Tabla Editorial
CREATE TABLE Editorial(
	id_editorial INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    pais VARCHAR(100),
    anio_fundacion INT
);

-- Tabla Autor
CREATE TABLE Autor(
	id_autor INT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE,
    biografia TEXT
);

-- Tabla Libro (Relacion uno a muchos(1:N))
CREATE TABLE Libro(
    id_libro INT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    anio_publicacion INT,
    numero_paginas INT,
    genero VARCHAR(50),
    editorial_id INT,
    FOREIGN KEY (editorial_id) REFERENCES Editorial(id_editorial)
);

-- Table intermedia LibroAutor (Relacion muchos a muchos(N:N))S
CREATE TABLE LibroAutor(
    libro_id INT,
    autor_id INT,
    PRIMARY KEY (libro_id, autor_id),
    FOREIGN KEY (libro_id) REFERENCES Libro(id_libro),
    FOREIGN KEY (autor_id) REFERENCES Autor(id_autor)
);

-- Tabla Usuario
CREATE TABLE Usuario(
    id_usuario INT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla prestamo (Relacion uno a muchos(1:N))
CREATE TABLE Prestamo(
    id_prestamo INT PRIMARY KEY,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE,
    estado VARCHAR(20) DEFAULT 'pendiente', -- 'Pendiente', 'Devuelto', 'cancelado'
    usuario_id INT,
    libro_id INT,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (libro_id) REFERENCES Libro(id_libro)
)

-- Insert de prueba para todas las tablas

-- Editorial
INSERT INTO Editorial(id_editorial, nombre, pais, anio_fundacion)
VALUES
    (1, 'Editorial Planeta', 'España', 1949),
    (2, 'Anagrama', 'México', 1975),
    (3, 'Santillana', 'Argentina', 1960),
    (4, 'Alfaguara', 'Colombia', 1964),
    (5, 'Seix Barral', 'Chile', 1911),
    (6, 'Tusquets', 'España', 1980),
    (7, 'Penguin Random House', 'Estados Unidos', 1927),
    (8, 'HarperCollins', 'Reino Unido', 1989);

-- Autor
INSERT INTO Autor(id_autor, nombre_completo, nacionalidad, fecha_nacimiento, biografia)
VALUES
    (1, 'Laura Esquivel', 'México', '1950-09-30', 'Autora mexicana conocida por su novela "Como agua para chocolate"'),
    (2, 'Eduardo Galeano', 'Uruguay', '1940-09-03', 'Escritor uruguayo, autor de "Las venas abiertas de América Latina"'),
    (3, 'Rosario Castellanos', 'México', '1925-05-25', 'Poeta y novelista mexicana con fuerte enfoque feminista'),
    (4, 'Juan Rulfo', 'México', '1917-05-16', 'Narrador mexicano autor de "Pedro Páramo"'),
    (5, 'Claribel Alegría', 'Nicaragua', '1924-05-12', 'Poeta nicaragüense reconocida por su obra comprometida socialmente'),
    (6, 'César Vallejo', 'Perú', '1892-03-16', 'Poeta peruano innovador en la poesía de vanguardia'),
    (7, 'Horacio Quiroga', 'Uruguay', '1878-12-31', 'Escritor uruguayo maestro del cuento latinoamericano'),
    (8, 'Alfonsina Storni', 'Argentina', '1892-05-29', 'Poetisa argentina, pionera del feminismo en la literatura hispanoamericana');

-- Libro
INSERT INTO Libro(id_libro, titulo, isbn, anio_publicacion, numero_paginas, genero, editorial_id)
VALUES
    (1, 'Como agua para chocolate', '978-607-314-123-0', 1989, 256, 'Romántica', 1),
    (2, 'Las venas abiertas de América Latina', '978-950-07-1416-3', 1971, 360, 'Ensayo', 2),
    (3, 'Balún Canán', '978-968-16-0444-0', 1957, 288, 'Novela', 3),
    (4, 'Pedro Páramo', '978-968-16-1321-3', 1955, 124, 'Novela', 4),
    (5, 'La mujer del río', '978-958-30-2293-4', 1987, 220, 'Poesía', 5),
    (6, 'Trilce', '978-847-51-1162-0', 1922, 140, 'Poesía', 6),
    (7, 'Cuentos de la selva', '978-987-1136-43-7', 1918, 112, 'Cuento', 7),
    (8, 'El dulce daño', '978-950-03-9254-9', 1918, 96, 'Poesía', 8);

-- LibroAutor
INSERT INTO LibroAutor(libro_id, autor_id)
VALUES
    (1, 4),
    (2, 1),
    (3, 5),
    (4, 2),
    (5, 6),
    (6, 3),
    (7, 8),
    (8, 7);

-- Usuario
INSERT INTO Usuario(id_usuario, nombre_completo, correo_electronico, telefono, direccion)
VALUES
    (1, 'Elena Torres', 'etorres@correo.com', '3011234567', 'Carrera 15 # 45-23'),
    (2, 'Ricardo Moreno', 'rmoreno@correo.com', '3027654321', 'Avenida Sur #12-34'),
    (3, 'Valentina Cruz', 'vcruz@correo.com', '3039988776', 'Calle 8 # 9-10'),
    (4, 'Andrés Mejía', 'amejia@correo.com', '3045566778', 'Diagonal 20 #33-21'),
    (5, 'Camila Paredes', 'cparedes@correo.com', '3056677889', 'Transversal 40 #12-09'),
    (6, 'Daniela Ríos', 'drios@correo.com', '3067788990', 'Calle 50 #25-15'),
    (7, 'Santiago Luna', 'sluna@correo.com', '3078899001', 'Carrera 7 # 30-20'),
    (8, 'Manuela Herrera', 'mherrera@correo.com', '3089900112', 'Callejón del Sol #3');

-- Prestamo
INSERT INTO Prestamo(id_prestamo, fecha_prestamo, fecha_devolucion, estado, usuario_id, libro_id)
VALUES
    (1, '2023-06-12', NULL, 'pendiente', 3, 5),
    (2, '2023-05-01', '2023-05-10', 'devuelto', 1, 4),
    (3, '2023-07-20', '2023-08-01', 'devuelto', 2, 6),
    (4, '2024-01-10', NULL, 'pendiente', 4, 1),
    (5, '2024-02-14', NULL, 'cancelado', 5, 2),
    (6, '2024-03-05', '2024-03-12', 'devuelto', 6, 7),
    (7, '2025-04-20', NULL, 'pendiente', 7, 8),
    (8, '2025-04-25', NULL, 'pendiente', 8, 3);

-- Consultar entre tablas (Con JOIN)

-- Mostrar todos los prestamos con informacion de usuario y libro
SELECT
    p.id_prestamo AS id_prestamo,
    U.nombre_completo AS nombre_usuario,
    L.titulo AS titulo_libro,
    P.fecha_prestamo,
    p.fecha_devolucion,
    p.estado,
    CASE
        WHEN p.estado = 'cancelado' THEN 'Prestamo cancelado'
        WHEN p.fecha_devolucion IS NULL THEN 'Libro aun no ha sido devuelto'
        ELSE 'Libro devuelto'
    END AS obsevacion
FROM prestamo P
JOIN usuario U ON P.usuario_id = U.id_usuario
JOIN libro L ON P.libro_id = L.id_libro;

-- Opcion 2

SELECT
    p.id_prestamo AS id_prestamo,
    U.nombre_completo AS nombre_usuario,
    L.titulo AS titulo_libro,
    P.fecha_prestamo,
    CASE
        WHEN p.estado = 'cancelado' THEN 'Prestamo cancelado'
        WHEN p.fecha_devolucion IS NULL THEN 'Libro aun no ha sido devuelto'
        ELSE DATE_FORMAT(p.fecha_devolucion, '%Y-%m-%d')
    END AS fecha_devolucion,
	p.estado

FROM prestamo P
JOIN usuario U ON P.usuario_id = U.id_usuario
JOIN libro L ON P.libro_id = L.id_libro;

-- Opcion sin alias
SELECT
    prestamo.id_prestamo,
    usuario.nombre_completo,
    libro.titulo,
    prestamo.fecha_prestamo,
    CASE
        WHEN prestamo.estado = 'cancelado' THEN 'Prestamo cancelado'
        WHEN prestamo.fecha_devolucion IS NULL THEN 'Libro aun no ha sido devuelto'
        ELSE DATE_FORMAT(prestamo.fecha_devolucion, '%Y-%m-%d')
    END AS fecha_devolucion,
    prestamo.estado

FROM prestamo
JOIN usuario ON prestamo.usuario_id = usuario.id_usuario
JOIN libro ON prestamo.libro_id = libro.id_libro;

-- Obtener todos los libros de un autor
SELECT
    l.titulo AS libro,
    A.nombre_completo AS autor,
    l.isbn
FROM Libro as l
JOIN LibroAutor as LA ON l.id_libro = LA.libro_id
JOIN Autor as A ON LA.autor_id = A.id_autor

-- Listar los libros por editorial
SELECT
    L.titulo AS libro,
    E.nombre AS editorial,
    L.isbn
FROM Libro as L
JOIN Editorial as E ON L.editorial_id = E.id_editorial

-- Consultar los prestasmo realizados en una fecha especifica
SELECT
    p.id_prestamo
FROM Prestamo p
JOIN Usuario u ON p.usuario_id = u.id_usuario
JOIN Libro l ON p.libro_id = l.id_libro
WHERE p.fecha_prestamo = '2020-01-01';