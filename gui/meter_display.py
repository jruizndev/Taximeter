import tkinter as tk
from tkinter import ttk, messagebox
from config.config import TIME_SLOTS, SPECIAL_CONDITIONS
import time

class MeterDisplay(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.master = master
        self.active_condition = None

        # Variables de control
        self.is_moving = False
        self.start_time = None
        self.accumulated_fare = 0.0
        self.last_update = None

        self._create_widgets()

    # Crea los widgets del taxímetro
    def _create_widgets(self):
        # Título 
        title_label = ttk.Label(
            self,
            text="Sistema de Taxímetro Digital",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Frame para botones principales
        buttons_frame = ttk.Frame(self)
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

    # Inicia un nuevo trayecto
    def start_new_trip(self):
        # Crear ventana para el nuevo trayecto
        trip_window = tk.Toplevel(self.master)
        trip_window.title("Nuevo Trayecto")
        trip_window.geometry("500x400")

        # Reiniciar variables de control
        self.is_moving = False  
        self.start_time = time.time()
        self.accumulated_fare = 0.0
        self.last_update = self.start_time

        # Frame principal
        main_frame = ttk.Frame(trip_window, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Trayecto en Curso",
            font=("Helvetica", 16, "bold")  
        )
        title_label.pack(pady=(0, 20))

        # Frame info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="both", expand=True)

        # Labels info
        state_var = tk.StringVar(value="PARADO")
        time_var = tk.StringVar(value="0:00")   
        fare_var = tk.StringVar(value="0.00€")

        # Estado actual 
        ttk.Label(info_frame, text="Estado:", font=("Helvetica", 12)).pack(pady=5)
        state_label = ttk.Label(info_frame, textvariable=state_var, font=("Helvetica", 14, "bold"))  
        state_label.pack(pady=5)

        # Tiempo transcurrido
        ttk.Label(info_frame, text="Tiempo:", font=("Helvetica", 12)).pack(pady=5)
        time_label = ttk.Label(info_frame, textvariable=time_var, font=("Helvetica", 14, "bold"))
        time_label.pack(pady=5)

        # Tarifa acumulada  
        ttk.Label(info_frame, text="Tarifa:", font=("Helvetica", 12)).pack(pady=5)
        fare_label = ttk.Label(info_frame, textvariable=fare_var, font=("Helvetica", 14, "bold"))
        fare_label.pack(pady=5)  

        # Frame botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Actualizar estado
        def update_display():
            current_time = time.time()
            elapsed = current_time - self.start_time
        
            # Actualizar tiempo
            minutes, seconds = divmod(int(elapsed), 60)  
            time_var.set(f"{minutes}:{seconds:02d}")
        
            # Calcular tarifa
            rate = TIME_SLOTS['normal']  # Tarifa normal por defecto
            rate_multiplier = 1.0
        
            if self.active_condition:
                rate_multiplier = SPECIAL_CONDITIONS[self.active_condition]
        
            current_rate = rate['motion_rate'] if self.is_moving else rate['stopped_rate']
            time_diff = current_time - self.last_update
            self.accumulated_fare += current_rate * rate_multiplier * time_diff
        
            fare_var.set(f"{self.accumulated_fare:.2f}€")
            self.last_update = current_time
        
            # Programar próxima actualización
            self.after(1000, update_display)

        def toggle_movement():
            self.is_moving = not self.is_moving
            state_var.set("EN MOVIMIENTO" if self.is_moving else "PARADO")

        def end_trip():
            if messagebox.askyesno("Finalizar Trayecto", "¿Desea finalizar el trayecto actual?"):
                trip_window.destroy()
                messagebox.showinfo(
                    "Trayecto Finalizado",
                    f"Tarifa final: {self.accumulated_fare:.2f}€\n"
                    f"Tiempo total: {time_var.get()}"
                )
    
        # Botones control
        toggle_button = ttk.Button(
            button_frame,  
            text="Iniciar Movimiento",
            command=toggle_movement,
            width=20
        )
        toggle_button.pack(side=tk.LEFT, padx=5)

        end_button = ttk.Button(
            button_frame,
            text="Finalizar Trayecto", 
            command=end_trip,
            width=20
        )
        end_button.pack(side=tk.LEFT, padx=5)

        # Iniciar actualización display
        self.after(1000, update_display)

    def show_current_rates(self):
        # Crear ventana para mostrar tarifas
        rates_window = tk.Toplevel(self.master)
        rates_window.title("Tarifas Actuales")
        rates_window.geometry("600x500") 
    
        # Frame principal
        main_frame = ttk.Frame(rates_window, padding=20)
        main_frame.pack(expand=True, fill="both") 

        # Título
        title_label = ttk.Label(
            main_frame,
            text="TARIFAS DEL TAXÍMETRO", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Frame info tarifas  
        rates_frame = ttk.Frame(main_frame)
        rates_frame.pack(fill="both", expand=True)

        # Cabeceras
        headers = ["Tipo de Tarifa", "Horario", "En movimiento", "Parado"] 
        for col, header in enumerate(headers):
            label = ttk.Label(rates_frame, text=header, font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Tarifas normales
        row = 1
        for slot_name, slot_info in TIME_SLOTS.items():
            # Descripción
            ttk.Label(rates_frame, text=slot_info['description']).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")
        
            # Horario  
            time_range = f"{slot_info['start']} - {slot_info['end']}" if slot_name != 'normal' else "Resto de horas"
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

        # Condiciones especiales 
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

    def manage_special_conditions(self):
        # Crear ventana para gestionar condiciones especiales
        conditions_window = tk.Toplevel(self.master)
        conditions_window.title("Gestionar Condiciones Especiales")
        conditions_window.geometry("400x300") 

        # Frame principal
        main_frame = ttk.Frame(conditions_window, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Gestionar Condiciones Especiales",  
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Variable selección
        selected_condition = tk.StringVar(value=self.active_condition or "none")

        # Frame opciones
        options_frame = ttk.Frame(main_frame)  
        options_frame.pack(fill="both", expand=True)

        # Opción sin condiciones especiales
        ttk.Radiobutton( 
            options_frame,
            text="Sin condiciones especiales",
            value="none", 
            variable=selected_condition
        ).pack(pady=5, anchor="w")  

        # Opciones condiciones especiales
        for condition, multiplier in SPECIAL_CONDITIONS.items():
            condition_name = "Lluvia" if condition == "rain" else "Eventos especiales"
            ttk.Radiobutton(
                options_frame,
                text=f"{condition_name} (x{multiplier})", 
                value=condition,
                variable=selected_condition 
            ).pack(pady=5, anchor="w")

        # Frame botones
        button_frame = ttk.Frame(main_frame) 
        button_frame.pack(pady=20)

        def apply_conditions():
            self.active_condition = None if selected_condition.get() == "none" else selected_condition.get()
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
            width=15 
        )
        apply_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button( 
            button_frame,
            text="Cancelar", 
            command=conditions_window.destroy,
            width=15
        )  
        cancel_button.pack(side=tk.LEFT, padx=5)