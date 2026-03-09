import mysql.connector
from mysql.connector import Error
from mysql.connector.errors import IntegrityError

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="admin",
            database="academia",
            port = 3306
        )
        self.cursor = self.connection.cursor()

    def _execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except IntegrityError as e:
            raise Exception(f"Error de integridad: {e.msg}")
        except Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e.msg}")

    def execute_query(self, query, params=None):
        self._execute(query, params)
        self.connection.commit()

    def execute_select(self, query, params=None):
        self._execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()