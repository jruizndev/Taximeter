import tkinter as tk
from tkinter import ttk
from auth.auth import Auth
from tkinter import messagebox


class TaxiMeterGUI:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Pepe Taxi")
        
        # Configurar el tamaño de la ventana
        self.root.geometry("800x600")

        # Inicializar la autenticación
        self.auth = Auth()

        # Variables para los campos de entrada
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Crear y mostrar el frame de autenticación
        self.create_auth_frame()

    # Crear el frame de autenticación
    def create_auth_frame(self):
        self.auth_frame = ttk.Frame(self.root, padding=20)
        self.auth_frame.pack(expand=True)
        
        # Título
        welcome_label = ttk.Label(
            self.root, 
            text="Bienvenido al Taxímetro Digital",
            font=("Helvetica", 16)
        )
        welcome_label.pack(pady=20)
        
        # Frame para el formulario
        form_frame = ttk.Frame(self.auth_frame)
        form_frame.pack(pady=20)

        # Username
        username_label = ttk.Label(form_frame, text="Usuario:")
        username_label.pack(pady=5)
        username_entry = ttk.Entry(form_frame, textvariable=self.username_var)
        username_entry.pack(pady=5)
        
        # Password
        password_label = ttk.Label(form_frame, text="Contraseña:")
        password_label.pack(pady=5)
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)
        
        # Botones
        button_frame = ttk.Frame(self.auth_frame)
        button_frame.pack(pady=20)
        
        login_button = ttk.Button(
            button_frame, 
            text="Iniciar Sesión",
            command=self.handle_login
        )
        login_button.pack(side=tk.LEFT, padx=10)
        
        register_button = ttk.Button(
            button_frame, 
            text="Registrarse",
            command=self.show_register_frame
        )
        register_button.pack(side=tk.LEFT, padx=10)

    # Maneja el proceso de inicio de sesión
    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        success, result = self.auth.login(username, password)
        if success:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {username}!")
        else:
            messagebox.showerror("Error", result)
    
    # Muestra frame de registro
    def show_register_frame(self):
        """Muestra el frame de registro"""
        pass

    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()

# Si ejecutamos este archivo directamente
if __name__ == "__main__":
    app = TaxiMeterGUI()
    app.run()