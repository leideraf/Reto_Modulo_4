from models.horario import Horario

class HorarioController:
    def __init__(self, db):
        self.db = db

    def registrar_horario(self, dia_semana, hora_inicio, hora_fin, curso_id):
        """
        Registra un horario en la base de datos.

        :param dia_semana: día de la semana
        :param hora_inicio: hora de inicio
        :param hora_fin: hora de fin
        :param curso_id: ID del curso
        """
        sql = """INSERT INTO horarios (dia_semana, hora_inicio, hora_fin, curso_id) VALUES (%s, %s, %s, %s)"""
        params = (dia_semana, hora_inicio, hora_fin, curso_id)
        self.db.execute_query(sql, params)

    def listar_horarios(self):
        """
        Devuelve una lista de objetos Horario que representan a los horarios
        registrados en la base de datos.

        :return: lista de objetos Horario
        """
        sql = """SELECT h.id_horario, h.dia_semana, h.hora_inicio, h.hora_fin, c.id_curso, c.nombre FROM horarios h JOIN cursos c ON h.curso_id = c.id_curso"""
        return [Horario(*resultado) for resultado in self.db.execute_select(sql)]

    def obtener_horario_por_id(self, id_horario):
        """
        Obtiene un horario por su ID.

        :param id_horario: ID del horario
        :return: objeto Horario
        """
        sql = """SELECT h.id_horario, h.dia_semana, h.hora_inicio, h.hora_fin, c.id_curso, c.nombre FROM horarios h JOIN cursos c ON h.curso_id = c.id_curso WHERE h.id_horario = %s"""
        params = (id_horario,)
        resultado = self.db.execute_select(sql, params)
        return Horario(*resultado[0]) if resultado else None

    def actualizar_horario(self, id_horario, dia_semana, hora_inicio, hora_fin, curso_id):
        """
        Actualiza los datos de un horario existente.

        :param id_horario: ID del horario a actualizar
        :param dia_semana: nuevo día de la semana
        :param hora_inicio: nueva hora de inicio
        :param hora_fin: nueva hora de fin
        :param curso_id: nuevo ID del curso
        """
        sql = """UPDATE horarios SET dia_semana = %s, hora_inicio = %s, hora_fin = %s, curso_id = %s WHERE id_horario = %s"""
        params = (dia_semana, hora_inicio, hora_fin, curso_id, id_horario)
        self.db.execute_query(sql, params)

    def eliminar_horario(self, id_horario):
        """
        Elimina un horario de la base de datos.

        :param id_horario: ID del horario a eliminar
        """
        sql = """DELETE FROM horarios WHERE id_horario = %s"""
        params = (id_horario,)
        self.db.execute_query(sql, params)