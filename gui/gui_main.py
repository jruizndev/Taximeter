import tkinter as tk
from tkinter import ttk, messagebox
from auth.auth import Auth
from config.config import TIME_SLOTS, SPECIAL_CONDITIONS

class TaxiMeterGUI:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Pepe Taxi")
        self.active_condition = None # Variable para almacenar la condición activa
        
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

    # Iniciar un nuevo trayecto
    def start_new_trip(self):
        messagebox.showinfo("Info", "Iniciando nuevo trayecto...")

    # Mostrar tarifas actuales
    def show_current_rates(self):
        # Crear una nueva ventana para las tarifas
        rates_window = tk.Toplevel(self.root)
        rates_window.title("Tarifas Actuales")
        rates_window.geometry("600x500")  # Aumentado el tamaño para mostrar más información
    
        # Frame principal
        main_frame = ttk.Frame(rates_window, padding="20")
        main_frame.pack(expand=True, fill="both")
    
        # Título
        title_label = ttk.Label(
            main_frame,
            text="TARIFAS DEL TAXÍMETRO",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
    
        # Frame para la información de tarifas
        rates_frame = ttk.Frame(main_frame)
        rates_frame.pack(fill="both", expand=True)
    
        # Crear cabeceras
        headers = ["Tipo de Tarifa", "Horario", "En movimiento", "Parado"]
        for col, header in enumerate(headers):
            label = ttk.Label(rates_frame, text=header, font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky="w")
    
        # Añadir tarifas normales
        row = 1
        for slot_name, slot_info in TIME_SLOTS.items():
            # Descripción
            ttk.Label(rates_frame, text=slot_info['description']).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")
        
            # Horario
            if slot_name != 'normal':
                time_range = f"{slot_info['start']} - {slot_info['end']}"
            else:
                time_range = "Resto de horas"
            ttk.Label(rates_frame, text=time_range).grid(
                row=row, column=1, padx=10, pady=5)
        
            # Tarifas
            ttk.Label(rates_frame, text=f"{slot_info['motion_rate']}€/s").grid(
                row=row, column=2, padx=10, pady=5)
            ttk.Label(rates_frame, text=f"{slot_info['stopped_rate']}€/s").grid(
                row=row, column=3, padx=10, pady=5)
        
            row += 1
    
        # Separador
        ttk.Separator(rates_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=4, sticky="ew", pady=10)
        row += 1
    
        # Título condiciones especiales
        special_label = ttk.Label(
            rates_frame,
            text="Condiciones Especiales (Multiplicadores)",
            font=("Helvetica", 10, "bold")
        )
        special_label.grid(row=row, column=0, columnspan=4, pady=10, sticky="w")
        row += 1
    
        # Añadir condiciones especiales
        for condition, multiplier in SPECIAL_CONDITIONS.items():
            condition_name = "Lluvia" if condition == "rain" else "Eventos especiales"
            ttk.Label(rates_frame, text=condition_name).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(rates_frame, text=f"x{multiplier}").grid(
                row=row, column=1, columnspan=3, padx=10, pady=5)
            row += 1
    
        # Botón cerrar
        close_button = ttk.Button(
            main_frame,
            text="Cerrar",
            command=rates_window.destroy,
            width=20
        )
        close_button.pack(pady=20)

    # Gestionar condiciones especiales
    def manage_special_conditions(self):
        # Crear una nueva ventana para gestionar condiciones especiales
        conditions_window = tk.Toplevel(self.root)
        conditions_window.title("Gestionar Condiciones Especiales")
        conditions_window.geometry("400x300")

        # Frame principal
        main_frame = ttk.Frame(conditions_window, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Gestionar Condiciones Especiales",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Variable para rastrear la selección
        selected_condition = tk.StringVar(value=self.active_condition if self.active_condition else "none")

        # Frame para las opciones
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill="both", expand=True)

        # Opción: Sin condiciones especiales
        ttk.Radiobutton(
            options_frame,
            text="Sin condiciones especiales",
            value="none",
            variable=selected_condition
        ) .pack(pady=5, anchor="w")

        # Opciones para cada condición especial
        for condition, multiplier in SPECIAL_CONDITIONS.items():
            condition_name = "Lluvia" if condition == "rain" else "Eventos especiales"
            ttk.Radiobutton(
                options_frame,
                text=f"{condition_name} (x{multiplier})",
                value=condition,
                variable=selected_condition
            ).pack(pady=5, anchor="w")

        # Frame para los botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        def apply_conditions():
            selected = selected_condition.get()
            self.active_condition = None if selected == "none" else selected
            conditions_window.destroy()
            messagebox.showinfo(
                "Éxito",
                "Condiciones especiales aplicadas correctamente" if self.active_condition else "Condiciones especiales desactivadas"
            )

        # Botones
        apply_button = ttk.Button(
            button_frame,
            text="Aplicar",
            command=apply_conditions,
            width= 15
        )
        apply_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(
            button_frame,
            text="Cancelar",
            command=conditions_window.destroy,
            width= 15
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()

# Si ejecutamos este archivo directamente
if __name__ == "__main__":
    app = TaxiMeterGUI()
    app.run()