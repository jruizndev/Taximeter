import tkinter as tk
from tkinter import ttk
from auth.auth import Auth

# Frame de autenticación para el taxímetro.
class AuthFrame(ttk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, padding=20)
        # Inicializamos Auth para la conexión con la base de datos
        self.auth = Auth()
        self.on_login_success = on_login_success
        
        # Variables para los campos de entrada 
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Variables para el registro
        self.reg_username_var = tk.StringVar()
        self.reg_password_var = tk.StringVar()
        self.reg_confirm_password_var = tk.StringVar()

        # Variable para mensajes
        self.message_var = tk.StringVar()

        # Inicialmente mostramos la vista de login
        self._create_login_view()
    
    def _show_message(self, message, is_error=False):
        # Limpiar mensaje anterior
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        
        # Crear etiqueta de mensaje
        color = 'red' if is_error else 'green'
        self.message_label = ttk.Label(
            self, 
            text=message,
            foreground=color,
            font=("Arial", 10)
        )
        self.message_label.pack(pady=10)
        
        # Programar eliminación del mensaje
        self.after(3000, self._clear_message)
    
    def _clear_message(self):
        # Eliminar etiqueta de mensaje si existe
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
    
    # Crea la interfaz de inicio de sesión
    def _create_login_view(self):
        # Limpiamos cualquier widget existente
        for widget in self.winfo_children():
            widget.destroy()
            
        # Título 
        title_label = ttk.Label(
            self, 
            text="SISTEMA DE TAXÍMETRO",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 30))

        # Frame para el formulario
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)

        # Usuario
        username_label = ttk.Label(
            form_frame, 
            text="USUARIO",
            font=("Arial", 12)
        )
        username_label.pack(pady=5)
        username_entry = ttk.Entry(
            form_frame,
            textvariable=self.username_var,
            width=20,
            justify='center'
        )
        username_entry.pack(pady=5)
        
        # Contraseña
        password_label = ttk.Label(
            form_frame, 
            text="CONTRASEÑA",
            font=("Arial", 12)
        )
        password_label.pack(pady=5)
        password_entry = ttk.Entry(
            form_frame,
            textvariable=self.password_var,
            show="•",
            width=20,
            justify='center'
        )
        password_entry.pack(pady=5)

        # Frame para botones
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=30)
        
        # Botones con estilo mejorado
        login_button = ttk.Button(
            button_frame,
            text="INICIAR SESIÓN",
            command=self._handle_login,
            width=20
        )
        login_button.pack(side=tk.LEFT, padx=10)
        
        register_button = ttk.Button(
            button_frame,
            text="REGISTRARSE",
            command=self._show_register_view,
            width=20
        )
        register_button.pack(side=tk.LEFT, padx=10)
    
    # Vista de registro
    def _show_register_view(self):
        # Limpieza de widgets existentes
        for widget in self.winfo_children():
            widget.destroy()
        
        # Título de registro
        title_label = ttk.Label(
            self, 
            text="REGISTRO DE USUARIO",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Frame del formulario
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)
        
        # Campo de usuario
        username_label = ttk.Label(form_frame, text="USUARIO:", font=("Arial", 12))
        username_label.pack(pady=5)
        username_entry = ttk.Entry(
            form_frame,
            textvariable=self.reg_username_var,
            width=20,
            justify='center'
        )
        username_entry.pack(pady=5)
        
        # Campo de contraseña
        password_label = ttk.Label(form_frame, text="CONTRASEÑA:", font=("Arial", 12))
        password_label.pack(pady=5)
        password_entry = ttk.Entry(
            form_frame,
            textvariable=self.reg_password_var,
            show="•",
            width=20,
            justify='center'
        )
        password_entry.pack(pady=5)
        
        # Campo de confirmación de contraseña
        confirm_label = ttk.Label(
            form_frame,
            text="CONFIRMAR CONTRASEÑA:",
            font=("Arial", 12)
        )
        confirm_label.pack(pady=5)
        confirm_entry = ttk.Entry(
            form_frame,
            textvariable=self.reg_confirm_password_var,
            show="•",
            width=20,
            justify='center'
        )
        confirm_entry.pack(pady=5)
        
        # Frame para botones
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=30)
        
        # Botones de acción
        register_button = ttk.Button(
            button_frame,
            text="COMPLETAR REGISTRO",
            command=self._handle_register,
            width=20
        )
        register_button.pack(side=tk.LEFT, padx=10)
        
        back_button = ttk.Button(
            button_frame,
            text="VOLVER",
            command=self._create_login_view,
            width=20
        )
        back_button.pack(side=tk.LEFT, padx=10)

    # Manejo de inicio de sesión
    def _handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        success, result = self.auth.login(username, password)
        if success:
            self.on_login_success(result)
        else:
            self._show_message(result, is_error=True)

    # Proceso de registro de usuario
    def _handle_register(self):
        username = self.reg_username_var.get()
        password = self.reg_password_var.get()
        confirm_password = self.reg_confirm_password_var.get()
        
        # Validaciones
        if not username or not password or not confirm_password:
            self._show_message("Todos los campos son obligatorios", is_error=True)
            return
            
        if password != confirm_password:
            self._show_message("Las contraseñas no coinciden", is_error=True)
            return
            
        # Intento de registro
        success, message = self.auth.register_user(username, password)
        if success:
            self._show_message("Usuario registrado correctamente")
            self._create_login_view()
            self.username_var.set(username)
        else:
            self._show_message(message, is_error=True)

    def reset_fields(self):
        self.username_var.set("")
        self.password_var.set("")
        self.reg_username_var.set("") 
        self.reg_password_var.set("")
        self.reg_confirm_password_var.set("")
        self._create_login_view()
    