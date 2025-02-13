import tkinter as tk
from tkinter import ttk, messagebox
from auth.auth import Auth

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

        # Variables para los campos de entrada de registro
        self.reg_username_var = tk.StringVar()
        self.reg_password_var = tk.StringVar()
        self.reg_confirm_password_var = tk.StringVar()

         # Crear y mostrar el frame de autenticación
        self.create_auth_frame()

    # Crear el frame de autenticación
    def create_auth_frame(self):
        self.auth_frame = ttk.Frame(self.root, padding=20)
        self.auth_frame.pack(expand=True)
        
        # Título
        title_label = ttk.Label(
            self.auth_frame, 
            text="Bienvenido al Taxímetro Digital",
            font=("Helvetica", 16)
        )
        title_label.pack(pady=20)

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
            self.current_user = result
            self.auth_frame.pack_forget()
            self.show_main_window()
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

    # Muestra la ventana principal del taximetro
    def show_main_window(self):
        # Crear el frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(expand=True, fill="both")

        # Header con información del usuario
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))

        # Usuario actual y rol
        user_label = ttk.Label(
            header_frame,
            text=f"Usuario: {self.current_user['username']} | Rol: {self.current_user['role']}",
            font=("Helvetica", 10)
        )
        user_label.pack(side="left")

        # Botón de cerrar sesión
        logout_button = ttk.Button(
            header_frame,
            text="Cerrar Sesión",
            command=self.handle_logout
        )
        logout_button.pack(side="right")

        # Contenedor central
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(expand=True, fill="both")

        # Título
        title_label = ttk.Label(
            content_frame,
            text="Sistema de Taxímetro Digital",
            font=("Helvetica", 16)
        )
        title_label.pack(pady=20)

        # Frame para los botones principales
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(pady=20)

        # Botones principales
        new_trip_btn = ttk.Button(
            buttons_frame,
            text="Nuevo Trayecto",
            command=self.start_new_trip,
            width=30
        )
        new_trip_btn.pack(pady=10)

        show_rates_btn = ttk.Button(
            buttons_frame,
            text="Ver Tarifas Actuales",
            command=self.show_current_rates,
            width=30
        )
        show_rates_btn.pack(pady=10)

        manage_conditions_btn = ttk.Button(
            buttons_frame,
            text="Gestionar Condiciones Especiales",
            command=self.manage_special_conditions,
            width=30
        )
        manage_conditions_btn.pack(pady=10)

    # Maneja el cierre de sesión
    def handle_logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que quieres cerrar sesión?"):
            self.current_user = None
            self.main_frame.destroy()
            self.username_var.set("")
            self.password_var.set("")
            self.show_auth_frame()

    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()

# Si ejecutamos este archivo directamente
if __name__ == "__main__":
    app = TaxiMeterGUI()
    app.run()