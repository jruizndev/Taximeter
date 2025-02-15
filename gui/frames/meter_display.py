import tkinter as tk
from tkinter import ttk, messagebox
from config.config import TIME_SLOTS, SPECIAL_CONDITIONS
import time
from datetime import datetime

class MeterDisplay(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        self.master = master
        self.active_condition = None

        # Variables de estado
        self.status_var = tk.StringVar(value="LIBRE")
        self.time_var = tk.StringVar(value="00:00")
        self.fare_var = tk.StringVar(value="0.00 €")
        self.message_var = tk.StringVar(value="")
        self.date_var = tk.StringVar()
        self.clock_var = tk.StringVar()

        # Variables de control de viaje
        self.is_moving = False
        self.trip_in_progress = False
        self.start_time = None
        self.accumulated_fare = 0.0
        self.last_update = None
        self.end_trip_confirmation = False

        # Configurar pantalla inicial y actualizar fecha/hora
        self._update_datetime()
        self._create_main_widgets()
        self._start_clock()

    def _update_datetime(self):
        # Actualizar fecha y hora
        now = datetime.now()
        self.date_var.set(now.strftime("%d/%m/%Y"))
        self.clock_var.set(now.strftime("%H:%M:%S"))

    def _start_clock(self):
        # Actualizar hora cada segundo
        self._update_datetime()
        self.after(1000, self._start_clock)

    def _create_main_widgets(self):
        # Limpiar frame anterior si existe
        for widget in self.winfo_children():
            widget.destroy()

        # Frame para fecha y hora
        datetime_frame = ttk.Frame(self)
        datetime_frame.pack(fill='x', padx=10, pady=5)

        # Fecha en la esquina superior izquierda
        date_label = ttk.Label(
            datetime_frame, 
            textvariable=self.date_var, 
            font=("Helvetica", 10)
        )
        date_label.pack(side=tk.LEFT)

        # Hora en la esquina superior derecha
        time_label = ttk.Label(
            datetime_frame, 
            textvariable=self.clock_var, 
            font=("Helvetica", 10)
        )
        time_label.pack(side=tk.RIGHT)

        # Título 
        title_label = ttk.Label(
            self,
            text="TAXÍMETRO DIGITAL",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Área de mensajes
        self.message_label = ttk.Label(
            self, 
            textvariable=self.message_var,
            font=("Helvetica", 12),
            foreground="red"
        )
        self.message_label.pack(pady=10)

        # Labels para estado, tiempo y tarifa
        status_label = ttk.Label(self, text="LIBRE", font=("Arial", 24, "bold"))
        status_label.configure(textvariable=self.status_var)
        status_label.pack(pady=10)

        time_label = ttk.Label(self, text="00:00", font=("Arial", 36, "bold"))  
        time_label.configure(textvariable=self.time_var)  
        time_label.pack(pady=10)

        fare_label = ttk.Label(self, text="0.00 €", font=("Arial", 36, "bold"))
        fare_label.configure(textvariable=self.fare_var)
        fare_label.pack(pady=10)

        # Frame para botones principales
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=20)

        # Botones principales
        self.new_trip_btn = ttk.Button(
            buttons_frame,
            text="Nuevo Trayecto",
            command=self.start_new_trip,
            width=30
        )
        self.new_trip_btn.pack(pady=10)

        # Botones de control de viaje (inicialmente ocultos)
        self.trip_control_btn_frame = ttk.Frame(self)
        self.trip_control_btn_frame.pack(pady=10)
        self.trip_control_btn_frame.pack_forget()

        self.toggle_movement_btn = ttk.Button(
            self.trip_control_btn_frame,
            text="Iniciar Movimiento",
            command=self.toggle_movement,
            width=20
        )
        self.toggle_movement_btn.pack(side=tk.LEFT, padx=5)

        self.end_trip_btn = ttk.Button(
            self.trip_control_btn_frame,
            text="Finalizar Trayecto", 
            command=self.end_trip,
            width=20
        )
        self.end_trip_btn.pack(side=tk.LEFT, padx=5)

        # Botones adicionales
        show_rates_btn = ttk.Button(
            buttons_frame,
            text="Ver Tarifas Actuales", 
            command=self.show_current_rates,
            width=30
        )
        show_rates_btn.pack(pady=10)

        special_conditions_btn = ttk.Button(
            buttons_frame,
            text="Condiciones Especiales",
            command=self.show_special_conditions,
            width=30
        )
        special_conditions_btn.pack(pady=10)

    def _create_special_conditions_widgets(self):
        # Limpiar frame anterior
        for widget in self.winfo_children():
            widget.destroy()

        # Título
        title_label = ttk.Label(
            self,
            text="Condiciones Especiales",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Variable selección
        selected_condition = tk.StringVar(value=self.active_condition or "none")

        # Frame opciones
        options_frame = ttk.Frame(self)
        options_frame.pack(fill="both", expand=True, padx=20)

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
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        def apply_conditions():
            # Aplicar condición seleccionada
            if selected_condition.get() == "none":
                self.active_condition = None
            else:
                self.active_condition = selected_condition.get()
            
            # Volver a la pantalla principal
            self._create_main_widgets()

        def go_back():
            # Volver a la pantalla principal sin cambios
            self._create_main_widgets()

        # Botones
        apply_button = ttk.Button(
            button_frame, 
            text="Aplicar",
            command=apply_conditions,
            width=15 
        )
        apply_button.pack(side=tk.LEFT, padx=5)

        back_button = ttk.Button(
            button_frame,
            text="Volver", 
            command=go_back,
            width=15
        )
        back_button.pack(side=tk.LEFT, padx=5)

    def _create_rates_widgets(self):
        # Limpiar frame anterior
        for widget in self.winfo_children():
            widget.destroy()

        # Título
        title_label = ttk.Label(
            self,
            text="TARIFAS DEL TAXÍMETRO", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Frame info tarifas  
        rates_frame = ttk.Frame(self)
        rates_frame.pack(fill="both", expand=True, padx=20)

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

        # Frame botones
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        # Botón volver
        back_button = ttk.Button(
            button_frame,
            text="Volver", 
            command=self._create_main_widgets,
            width=20
        )
        back_button.pack()

    def show_special_conditions(self):
        # Mostrar pantalla de condiciones especiales
        self._create_special_conditions_widgets()

    def show_current_rates(self):
        # Mostrar pantalla de tarifas
        self._create_rates_widgets()

    def show_message(self, message, duration=3):
        self.message_var.set(message)
        # Borrar mensaje después de duración
        self.after(duration * 1000, lambda: self.message_var.set(""))

    def start_new_trip(self):
        # Reiniciar variables de control
        self.is_moving = False
        self.trip_in_progress = True
        self.start_time = time.time()
        self.accumulated_fare = 0.0
        self.last_update = self.start_time
        self.end_trip_confirmation = False

        # Cambiar estado visual
        self.status_var.set("EN TRAYECTO")
        self.new_trip_btn.pack_forget()
        self.trip_control_btn_frame.pack(pady=10)

        # Mostrar mensaje de inicio
        self.show_message("Trayecto iniciado", 2)

        # Iniciar actualización display
        self.update_display()

    def toggle_movement(self):
        self.is_moving = not self.is_moving
        estado = "EN MOVIMIENTO" if self.is_moving else "PARADO"
        self.show_message(f"Estado: {estado}", 2)
        self.toggle_movement_btn.configure(
            text="Detener Movimiento" if self.is_moving else "Iniciar Movimiento"
        )

    def end_trip(self):
        if not self.end_trip_confirmation:
            # Primera pulsación - solicitar confirmación
            self.show_message("Pulsa de nuevo para confirmar fin de trayecto", 3)
            self.end_trip_confirmation = True
            return

        # Segunda pulsación - confirmar fin de trayecto
        self.trip_in_progress = False
        self.end_trip_confirmation = False

        # Cambiar estado visual
        self.status_var.set("TRAYECTO FINALIZADO")
        
        # Mostrar resumen
        resumen = f"Trayecto finalizado\nTarifa: {self.accumulated_fare:.2f}€\nTiempo: {self.time_var.get()}"
        self.show_message(resumen, 5)
    
        self.trip_control_btn_frame.pack_forget()
        self.new_trip_btn.pack(pady=10)

    def update_display(self):
        if not self.trip_in_progress:
            return

        current_time = time.time()
        elapsed = current_time - self.start_time
    
        # Actualizar tiempo
        minutes, seconds = divmod(int(elapsed), 60)  
        self.time_var.set(f"{minutes}:{seconds:02d}")
    
        # Calcular tarifa
        rate = TIME_SLOTS['normal']  # Tarifa normal por defecto
        rate_multiplier = 1.0
    
        if self.active_condition:
            rate_multiplier = SPECIAL_CONDITIONS[self.active_condition]
    
        current_rate = rate['motion_rate'] if self.is_moving else rate['stopped_rate']
        time_diff = current_time - self.last_update
        self.accumulated_fare += current_rate * rate_multiplier * time_diff
    
        self.fare_var.set(f"{self.accumulated_fare:.2f}€")
        self.last_update = current_time
    
        # Programar próxima actualización
        self.after(1000, self.update_display)