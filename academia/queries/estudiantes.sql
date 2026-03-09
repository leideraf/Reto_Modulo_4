-- Tabla Estudiantes
CREATE TABLE Estudiante(
	id_estudiante INT PRIMARY KEY,
    nombre VARCHAR(50)
);

-- Tabla Curso
CREATE TABLE Curso(
	id_curso INT PRIMARY KEY,
    nombre VARCHAR(50)
);

-- Tabla intermedia: EstudianteCurso
CREATE TABLE EstudianteCurso(
	estudiante_id INT,
    curso_id INT,
    PRIMARY KEY(estudiante_id,curso_id),
    FOREIGN KEY(estudiante_id) REFERENCES Estudiante(id_estudiante),
    FOREIGN KEY(curso_id) REFERENCES Curso(id_curso)
);