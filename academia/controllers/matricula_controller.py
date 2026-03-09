from models.matricula import Matricula

class MatriculaController:
    def __init__(self, db):
        self.db = db

    def registrar_matricula(self, estudiante_id, curso_id, fecha_matricula):
        """
        Registra una nueva matrícula en la base de datos.

        :param estudiante_id: ID del estudiante
        :param curso_id: ID del curso
        :param fecha_matricula: Fecha de la matrícula
        """
        sql = """
            INSERT INTO Matriculas (estudiante_id, curso_id, fecha_matricula)
            VALUES (%s, %s, %s)
        """
        params = (estudiante_id, curso_id, fecha_matricula)
        self.db.execute_query(sql, params)

    def listar_matriculas(self):
        """
        Devuelve una lista de objetos Matricula que representan todas las matriculas
        en la base de datos.
        """
        sql = """
            SELECT * FROM Matriculas
        """
        resultados = self.db.execute_select(sql)
        return [Matricula(*resultado) for resultado in resultados]

    def obtener_matricula_por_id(self, id_matricula):
        """
        Devuelve un objeto Matricula que representa la matrícula con el ID especificado.

        :param id_matricula: ID de la matrícula
        :return: Objeto Matricula
        """
        sql = """
            SELECT * FROM Matriculas WHERE id_matricula = %s
        """
        params = (id_matricula,)
        resultado = self.db.execute_select(sql, params)
        return Matricula(*resultado[0]) if resultado else None

    def actualizar_matricula(self, id_matricula, estudiante_id, curso_id, fecha_matricula):
        """
        Actualiza los datos de una matrícula existente en la base de datos.

        :param id_matricula: ID de la matrícula
        :param estudiante_id: ID del estudiante
        :param curso_id: ID del curso
        :param fecha_matricula: Fecha de la matrícula
        """
        sql = """
            UPDATE Matriculas SET estudiante_id = %s, curso_id = %s, fecha_matricula = %s
            WHERE id_matricula = %s
        """
        params = (estudiante_id, curso_id, fecha_matricula, id_matricula)
        self.db.execute_query(sql, params)

    def eliminar_matricula(self, id_matricula):
        """
        Elimina una matrícula existente en la base de datos.

        :param id_matricula: ID de la matrícula
        """
        sql = """
            DELETE FROM Matriculas WHERE id_matricula = %s
        """
        params = (id_matricula,)
        self.db.execute_query(sql, params)