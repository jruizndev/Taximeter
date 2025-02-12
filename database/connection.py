import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

# Gestión de la conexión a la base de datos
class DatabaseConnection:
    # Inicialización de parámetros de conexión desde variables de entorno
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '3306'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'taximeter')
        }
        self.connection = None

    # Conexión con la base de datos
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    # Cierre de la conexión con la base de datos
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")
