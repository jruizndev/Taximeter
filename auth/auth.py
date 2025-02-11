import bcrypt
from database.connection import DatabaseConnection

# Sistema de autenticación para el taxímetro
class Auth:
    # Inicialización de la conexión a la base de datos
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    # Hash de la contraseña
    def hash_password(self, password):
        # Convertir la contraseña a bytes y generar el hash
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash
