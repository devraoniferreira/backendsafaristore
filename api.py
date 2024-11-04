import os
from flask import Flask, jsonify
from flask_cors import CORS
from db_connection import DatabaseConnection

# Configurações do Banco de Dados a partir de variáveis de ambiente
DB_PATH = os.getenv('DB_PATH', r'/app/scl/dados/Elbrus.IB')
DB_PATH2 = os.getenv('DB_PATH2', r'/app/scl/dados/ELBRUS.IB')
USER = os.getenv('USER', 'sysdba')
PASSWORD = os.getenv('PASSWORD', 'masterkey')

app = Flask(__name__)

# Inicializa o CORS para permitir requisições de diferentes origens
CORS(app)

# Inicializa a conexão com o banco de dados
db_connection = DatabaseConnection(DB_PATH, DB_PATH2, USER, PASSWORD)
db_connection.connect()

@app.route('/get_records', methods=['GET'])
def get_records():
    records = db_connection.get_records()
    return jsonify(records)  # Retorna os registros em formato JSON

if __name__ == '__main__':
    # Configuração para uso no Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
