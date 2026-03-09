from models.curso import Curso

class CursoController:
    def __init__(self, db):
        self.db = db

    def registrar_curso(self, nombre, descripcion, duracion_horas, docente_id):
        """
        Registra un curso en la base de datos.

        :param nombre: nombre del curso
        :param descripcion: descripción del curso
        :param duracion_horas: duración del curso en horas
        :param docente_id: ID del docente que imparte el curso
        """
        sql = """
            INSERT INTO cursos (nombre, descripcion, duracion_horas, docente_id)
            VALUES (%s, %s, %s, %s)
        """
        params = (nombre, descripcion, duracion_horas, docente_id)
        self.db.execute_query(sql, params)

    def listar_cursos(self):
        """
        Devuelve una lista de objetos Curso que representan a los cursos
        registrados en la base de datos.

        :return: lista de objetos Curso
        """
        sql = """SELECT c.id_curso, c.nombre, c.descripcion , c.duracion_horas, d.id_docente, CONCAT(d.nombre, ' ', d.apellido) AS docente_nombre FROM Cursos c JOIN Docentes d ON c.docente_id = d.id_docente; """
        resultados = self.db.execute_select(sql)
        return [Curso(*resultado) for resultado in resultados]

    def obtener_curso_por_id(self, id_curso):
        """
        Obtiene un curso por su ID.

        :param id_curso: ID del curso
        :return: objeto Curso
        """
        sql = """SELECT c.id_curso, c.nombre, c.descripcion , c.duracion_horas, d.id_docente, CONCAT(d.nombre, ' ', d.apellido) AS docente_nombre FROM Cursos c JOIN Docentes d ON c.docente_id = d.id_docente WHERE c.id_curso = %s"""
        params = (id_curso,)
        resultado = self.db.execute_select(sql, params)
        return Curso(*resultado[0]) if resultado else None

    def actualizar_curso(self, id_curso, nombre, descripcion, duracion_horas, docente_id):
        """
        Actualiza los datos de un curso existente.

        :param id_curso: ID del curso a actualizar
        :param nombre: nuevo nombre del curso
        :param descripcion: nueva descripción del curso
        :param duracion_horas: nueva duración del curso en horas
        :param docente_id: nuevo ID del docente que imparte el curso
        """
        sql = """
            UPDATE cursos SET nombre = %s, descripcion = %s, duracion_horas = %s, docente_id = %s WHERE id_curso = %s
        """
        params = (nombre, descripcion, duracion_horas, docente_id, id_curso)
        self.db.execute_query(sql, params)

    def eliminar_curso(self, id_curso):
        """
        Elimina un curso de la base de datos.

        :param id_curso: ID del curso a eliminar
        """
        sql = """DELETE FROM cursos WHERE id_curso = %s"""
        params = (id_curso,)