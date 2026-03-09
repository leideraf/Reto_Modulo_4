-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS academia;

-- Usar la base de datos
USE academia;

-- Tabla estudiantes
CREATE TABLE Estudiantes(
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,  -- cada valor en la columna correo_electronico debe ser único.
    telefono VARCHAR(20)
);


-- Tabla Profesores
CREATE TABLE Profesores(
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    especialidad VARCHAR(50)
);

-- Tabla Cursos
CREATE TABLE Cursos(
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)NOT NULL,
    descripcion TEXT,  -- tipo de dato que almacena texto más largo que VARCHAR
    duracion_horas INT,
    profesor_id INT,
    FOREIGN KEY(profesor_id) REFERENCES Profesores(id_profesor)
        ON DELETE -- si se borra un profesor, el campo profesor_id del curso se pondrá en NULL
    SET NULL ON UPDATE CASCADE
);

-- Tabla matriculas
CREATE TABLE Matriculas(
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    curso_id INT,
    fecha_matricula DATE,
    FOREIGN KEY(estudiante_id)REFERENCES Estudiantes(id_estudiante)
            ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES Cursos (id_curso)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla horarios
CREATE TABLE Horarios(
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT,
    dia_semana VARCHAR(50),
    hora_inicio TIME,
    FOREIGN KEY (curso_id)REFERENCES Cursos(id_curso)
        ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Estudiantes (nombre, apellido, correo_electronico, telefono) VALUES
('Laura', 'García', 'laura.garcia@example.com', '3001234567'),
('Carlos', 'Pérez', 'carlos.perez@example.com', '3007654321'),
('Ana', 'Martínez', 'ana.martinez@example.com', '3012345678');


INSERT INTO Profesores (nombre, correo_electronico, telefono, especialidad) VALUES
('Marta Rodríguez', 'marta.rodriguez@example.com', '3112345678', 'Matemáticas'),
('Luis Fernández', 'luis.fernandez@example.com', '3123456789', 'Programación'),
('Sofía Ramírez', 'sofia.ramirez@example.com', '3134567890', 'Inglés');


INSERT INTO Cursos (nombre, descripcion, duracion_horas, profesor_id) VALUES
('Álgebra Básica', 'Curso introductorio al álgebra', 40, 1),
('Python para Principiantes', 'Aprende Python desde cero', 60, 2),
('Inglés Intermedio', 'Refuerza tus habilidades en inglés', 45, 3);


INSERT INTO Matriculas (estudiante_id, curso_id, fecha_matricula) VALUES
(1, 1, '2025-05-01'),
(2, 2, '2025-05-03'),
(3, 3, '2025-05-05'),
(1, 2, '2025-05-07');


INSERT INTO Horarios (curso_id, dia_semana, hora_inicio) VALUES
(1, 'Lunes', '08:00:00'),
(2, 'Martes', '10:00:00'),
(3, 'Miércoles', '09:00:00'),
(2, 'Jueves', '14:00:00');
