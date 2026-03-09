from models.estudiantes import Estudiante

class EstudianteController:
    def __init__(self, db):
        self.db = db

    def registrar_estudiante(self, nombre, apellido, correo, telefono):
        """
        Registra un estudiante en la base de datos.

        :param nombre: nombre del estudiante
        :param apellido: apellido del estudiante
        :param correo: correo electr nico del estudiante
        :param telefono: tel fono del estudiante
        """
        sql = """
            INSERT INTO Estudiantes (nombre, apellido, correo_electronico, telefono)
            VALUES (%s, %s, %s, %s)
        """
        params = (nombre, apellido, correo, telefono)
        self.db.execute_query(sql, params)

    def listar_estudiantes(self):
        """
        Devuelve una lista de objetos Estudiante que representan a los estudiantes
        registrados en la base de datos.
        """
        sql = """SELECT id_estudiante, nombre, apellido, correo_electronico, telefono FROM Estudiantes"""
        resultados = self.db.execute_select(sql)
        return [Estudiante(*resultado) for resultado in resultados]

    def obtener_estudiante_por_id(self, id_estudiante):
        """
        Obtiene un estudiante por su ID.

        :param id_estudiante: ID del estudiante
        :return: objeto Estudiante
        """
        sql = """SELECT id_estudiante, nombre, apellido, correo_electronico, telefono FROM estudiantes WHERE id_estudiante = %s"""
        params = (id_estudiante,)
        resultado = self.db.execute_select(sql, params)
        return Estudiante(*resultado[0]) if resultado else None


    def actualizar_estudiante(self, id_estudiante, nombre, apellido, correo, telefono):
        """
        Actualiza los datos de un estudiante existente.

        :param id_estudiante: ID del estudiante a actualizar
        :param nombre: nuevo nombre del estudiante
        :param apellido: nuevo apellido del estudiante
        :param correo: nuevo correo electr nico del estudiante
        :param telefono: nuevo tel fono del estudiante
        """
        sql = """
            UPDATE estudiantes SET nombre = %s, apellido = %s, correo_electronico = %s, telefono = %s WHERE id_estudiante = %s
        """
        params = (nombre, apellido, correo, telefono, id_estudiante)
        self.db.execute_query(sql, params)

    def eliminar_estudiante(self, id_estudiante):
        """
        Elimina un estudiante de la base de datos.

        :param id_estudiante: ID del estudiante a eliminar
        """
        sql = """DELETE FROM estudiantes WHERE id_estudiante = %s"""
        params = (id_estudiante,)
        self.db.execute_query(sql, params)

