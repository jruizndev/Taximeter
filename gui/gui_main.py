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

        # Variables para los campos de entrada de registro
        self.reg_username_var = tk.StringVar()
        self.reg_password_var = tk.StringVar()
        self.reg_confirm_password_var = tk.StringVar()

    # Crear el frame de autenticación
    def create_auth_frame(self):
        self.auth_frame = ttk.Frame(self.root, padding=20)
        self.auth_frame.pack(expand=True)
        
        # Título
        welcome_label = ttk.Label(
            self.auth_frame, 
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
        # Ocultar frame de autenticación
        self.auth_frame.pack_forget()
        
        # Crear frame de registro
        self.register_frame = ttk.Frame(self.root, padding="20")
        self.register_frame.pack(expand=True)
        
        # Título
        title_label = ttk.Label(
            self.register_frame, 
            text="Registro de Nuevo Usuario",
            font=("Helvetica", 16)
        )
        title_label.pack(pady=20)
        
        # Frame para el formulario
        form_frame = ttk.Frame(self.register_frame)
        form_frame.pack(pady=20)
        
        # Username
        username_label = ttk.Label(form_frame, text="Usuario:")
        username_label.pack(pady=5)
        username_entry = ttk.Entry(form_frame, textvariable=self.reg_username_var)
        username_entry.pack(pady=5)
        
        # Password
        password_label = ttk.Label(form_frame, text="Contraseña:")
        password_label.pack(pady=5)
        password_entry = ttk.Entry(form_frame, textvariable=self.reg_password_var, show="*")
        password_entry.pack(pady=5)
        
        # Confirm Password
        confirm_label = ttk.Label(form_frame, text="Confirmar Contraseña:")
        confirm_label.pack(pady=5)
        confirm_entry = ttk.Entry(form_frame, textvariable=self.reg_confirm_password_var, show="*")
        confirm_entry.pack(pady=5)
        
        # Botones
        button_frame = ttk.Frame(self.register_frame)
        button_frame.pack(pady=20)
        
        register_button = ttk.Button(
            button_frame, 
            text="Registrar",
            command=self.handle_register
        )
        register_button.pack(side=tk.LEFT, padx=10)
        
        back_button = ttk.Button(
            button_frame, 
            text="Volver",
            command=self.show_auth_frame
        )
        back_button.pack(side=tk.LEFT, padx=10)
    
    # Vuelve a mostrar frame de autenticación
    def show_auth_frame(self):
        # Limpiar campos de registro
        self.reg_username_var.set("")
        self.reg_password_var.set("")
        self.reg_confirm_password_var.set("")
        
        # Ocultar frame de registro si existe
        if hasattr(self, 'register_frame'):
            self.register_frame.pack_forget()
            
        # Mostrar frame de autenticación
        self.auth_frame.pack(expand=True)
    
    # Maneja el proceso de registro
    def handle_register(self):
        username = self.reg_username_var.get()
        password = self.reg_password_var.get()
        confirm_password = self.reg_confirm_password_var.get()
        
        # Validaciones básicas
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        # Intentar registro
        success, message = self.auth.register_user(username, password)
        if success:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.show_auth_frame()  
        else:
            messagebox.showerror("Error", message)

    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()

# Si ejecutamos este archivo directamente
if __name__ == "__main__":
    app = TaxiMeterGUI()
    app.run()