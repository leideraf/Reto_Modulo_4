from models.docente  import Docente

class DocenteController:
    def __init__(self, db):
        self.db = db

    def registrar_docente(self, nombre, apellido, correo, telefono, especialidad):
        """
        Registra un docente en la base de datos.

        :param nombre: nombre del docente
        :param apellido: apellido del docente
        :param correo_electronico: correo electr nico del docente
        :param telefono: tel fono del docente
        :param especialidad: especialidad del docente
        """
        sql = """
            INSERT INTO docentes (nombre, apellido, correo_electronico, telefono, especialidad)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (nombre, apellido, correo, telefono, especialidad)
        self.db.execute_query(sql, params)

    def listar_docentes(self):
        """
        Devuelve una lista de objetos Docente que representan a los docentes
        registrados en la base de datos.

        :return: lista de objetos Docente
        """
        sql = """SELECT id_docente, nombre, apellido, correo_electronico, telefono, especialidad FROM docentes"""
        resultados = self.db.execute_select(sql)
        return [Docente(*resultado) for resultado in resultados]

    def obtener_docente_por_id(self, id_docente):
        """
        Obtiene un docente por su ID.

        :param id_docente: ID del docente
        :return: objeto Docente
        """
        sql = """SELECT id_docente, nombre, apellido, correo_electronico, telefono, especialidad FROM docentes WHERE id_docente = %s"""
        params = (id_docente,)
        resultado = self.db.execute_select(sql, params)
        return Docente(*resultado[0]) if resultado else None

    def actualizar_docente(self, id_docente, nombre, apellido, correo, telefono, especialidad):
        """
        Actualiza los datos de un docente existente.

        :param id_docente: ID del docente a actualizar
        :param nombre: nuevo nombre del docente
        :param apellido: nuevo apellido del docente
        :param correo_electronico: nuevo correo electr nico del docente
        :param telefono: nuevo tel fono del docente
        :param especialidad: nueva especialidad del docente
        """
        sql = """
            UPDATE docentes SET nombre = %s, apellido = %s, correo_electronico = %s, telefono = %s, especialidad = %s WHERE id_docente = %s
        """
        params = (nombre, apellido, correo, telefono, especialidad, id_docente)
        self.db.execute_query(sql, params)

    def eliminar_docente(self, id_docente):
        """
        Elimina un docente de la base de datos.

        :param id_docente: ID del docente a eliminar
        """
        sql = """DELETE FROM docentes WHERE id_docente = %s"""
        params = (id_docente,)
        self.db.execute_query(sql, params)