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

    # Registro de usuario (username, password y role)
    def register_user(self, username, password, role='driver'):
        try:
            self.db.connect()
            cursor = self.db.connection.cursor()

            # Verifica si el usuario ya existe
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False, "El usuario ya existe"

            # Crear nuevo usuario+
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_password, role)
            )
            self.db.connection.commit()
            return True, "Usuario creado correctamente"
        except Exception as e:
            return False, f"Error en registro: {str(e)}"
        finally:
            self.db.disconnect()
