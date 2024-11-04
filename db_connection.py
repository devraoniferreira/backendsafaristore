# db_connection.py
import fdb
import os

class DatabaseConnection:
    def __init__(self, db_path, db_path2, user, password):
        self.db_path = db_path
        self.db_path2 = db_path2
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        if self._connect_to_path(self.db_path):
            return True
        elif self._connect_to_path(self.db_path2):
            return True
        return False

    def _connect_to_path(self, path):
        try:
            if not os.path.isfile(path):
                return False
            self.connection = fdb.connect(dsn='localhost:' + path, user=self.user, password=self.password)
            return True
        except fdb.DatabaseError:
            return False

    def get_records(self):
        if not self.connection:
            return "Conexao com o banco de dados nao estabelecida."
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT dt_mov, VALOR_TOTAL_PRODUTOS, VALOR_TOTAL_NF, DSC_CORTESIA 
                FROM Lojb085 
                WHERE dt_mov > '2024-10-01'
                ORDER BY dt_mov DESC 
                ROWS 15
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            if not resultados:
                return "Tabela Lojb085 vazia."
            return [dict(zip([column[0] for column in cursor.description], resultado)) for resultado in resultados]
        except fdb.Error as e:
            return f"Erro ao listar conteudo: {e}"
