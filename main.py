import time
import logging
from datetime import datetime
from config.config import TIME_SLOTS, SPECIAL_CONDITIONS
from auth.auth import Auth

# Clase principal del taxímetro
class Taximeter:
   def __init__(self):
       self.active_conditions = []
       self.current_trip = None
       self.rate_calculator = RateCalculator()
       self.initialize_logging()
       
    # Configuración del sistema de logs
   def initialize_logging(self):
       logging.basicConfig(
           filename='logs/taximeter.log',
           level=logging.INFO,
           format='%(asctime)s - %(levelname)s - %(message)s',
           datefmt='%d/%m/%Y %H:%M:%S'
       )

    # Inicio de un nuevo viaje
   def start_new_trip(self):
       self.current_trip = Trip(self.rate_calculator)
       logging.info("Nuevo trayecto iniciado")
       return self.current_trip

    # Cambia estado de movimiento
   def toggle_motion(self):
       if self.current_trip:
           self.current_trip.toggle_motion()

    # Finaliza el viaje actual
   def end_trip(self):
       if self.current_trip:
           trip_data = self.current_trip.finalize()
           self.current_trip = None
           return trip_data

# Clase para gestionar viajes
class Trip:
   def __init__(self, rate_calculator):
       self.start_time = time.time()
       self.last_state_change = self.start_time
       self.accumulated_rate = 0
       self.in_motion = False
       self.movements = [(0, self.in_motion)]
       self.rate_calculator = rate_calculator

    # Cambia estado del taxi
   def toggle_motion(self):
       current_time = time.time()
       self.accumulated_rate += self.calculate_segment_rate()
       self.last_state_change = current_time
       self.in_motion = not self.in_motion
       self.movements.append((current_time - self.start_time, self.in_motion))

    # Calcula tarifa del segmento actual
   def calculate_segment_rate(self):
       current_time = time.time()
       segment_time = current_time - self.last_state_change
       return self.rate_calculator.calculate_rate(segment_time, self.in_motion)
    
    # Finaliza el viaje y retorna datos
   def finalize(self):
       current_time = time.time()
       self.accumulated_rate += self.calculate_segment_rate()
       trip_duration = current_time - self.start_time
       self.movements.append((trip_duration, self.in_motion))
       return {
           'duration': trip_duration,
           'total_rate': self.accumulated_rate,
           'movements': self.movements,
           'rate_info': self.rate_calculator.get_current_rate()
       }

    # Obtiene estado actual del viaje
   def get_current_status(self):
       current_time = time.time()
       return {
           'state': 'Movimiento' if self.in_motion else 'Parado',
           'time': current_time - self.start_time,
           'rate': self.accumulated_rate + self.calculate_segment_rate()
       }

# Manejo de cáculos de tarifas según horario y condiciones
class RateCalculator:
   
   @staticmethod
   # Determina tarifa según hora actual
   def get_current_rate():
       current_time = datetime.now().time()
       current_str = current_time.strftime('%H:%M')

       for slot_name, slot_info in TIME_SLOTS.items():
           if slot_name == 'normal':
               continue
           if slot_info['start'] <= current_str <= slot_info['end']:
               return slot_info
       return TIME_SLOTS['normal']

    # Calcula tarifa según estado y condiciones
   @staticmethod
   def calculate_rate(elapsed_time, in_motion, special_condition=None):
       current_rates = RateCalculator.get_current_rate()
       base_rate = current_rates['motion_rate'] if in_motion else current_rates['stopped_rate']
       
       if special_condition in SPECIAL_CONDITIONS:
           base_rate *= SPECIAL_CONDITIONS[special_condition]
       
       return elapsed_time * base_rate

# Clase para interfaz de usuario
class TaxiUI:
    def __init__(self, taximeter):
        self.taximeter = taximeter
        self.auth = Auth()
        self.current_user = None
    
    def show_auth_menu(self):
        print("\nPepe Taxi")
        print("Bienvenido al sistema de taxímetro digital.")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")

        while True:
            option = input("\nSeleccione una opción (1-3): ")
            if option == "1":
                self.handle_login()
                break
            elif option == "2":
                    self.handle_register()
            elif option == "3":
                    print("\n¡Hasta pronto!")
                    exit()
            else:
                    print("Opción no válida. Por favor, seleccione 1-3")

        # Iniciar sesión
    def handle_login(self):
            print("\nIniciar sesión")
            username = input("Usuario: ")
            password = input("Contraseña: ")

            success, result = self.auth.login(username, password)
            if success:
                self.current_user = result
                print(f"\n¡Bienvenido, {username}!")
                return True
            else:
                print(f"Error: {result}")
                return False

        # Registrarse
    def handle_register(self):
            print("\nRegistraro de nuevo Usuario")
            username = input("Usuario: ")
            password = input("Contraseña: ")
            password_confirm = input("Confirmar contraseña: ")
            
            if password != password_confirm:
                print("Las contraseñas no coinciden")
                return False
            
            success, message = self.auth.register_user(username, password)
            if success:
                print(f"\n¡{username} registrado!")
            else:
                print(f"Error: {message}")
        

    def show_welcome_message(self):
        print("Pepe Taxi")
        print("\nBienvenido al sistema de taxímetro digital.")
        print("Este programa permite calcular tarifas de viajes en taxi.\n")
        print("Opciones disponibles:")
        print("1. Iniciar nuevo trayecto")
        print("2. Ver tarifas actuales")
        print("3. Gestionar condiciones especiales")
        print("4. Salir")

    # Mostramos tarifas actuales
    def show_current_rates(self):
        current_rates = self.taximeter.rate_calculator.get_current_rate()
        print("\n TARIFAS DEL TAXIMETRO")
        print("\nTARIFA ACTUAL:")
        print(f"► {current_rates['description']}")
        print(f"  - En movimiento: {current_rates['motion_rate']}€/s")
        print(f"  - Parado: {current_rates['stopped_rate']}€/s")

        if self.taximeter.active_conditions:
            condition = self.taximeter.active_conditions[0]
            multiplier = SPECIAL_CONDITIONS[condition]
            print(f"\nCondición especial activa: {condition.capitalize()} (+{(multiplier-1)*100}%)")

        input("\nPresione Enter para continuar...")

    # Resumen de viaje
    def show_trip_summary(self, trip_data):
       print("\n=== RESUMEN DEL VIAJE ===")
       print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
       print(f"Duración: {trip_data['duration']:.1f}s")
       print(f"Tarifa aplicada: {trip_data['rate_info']['description']}")
       if self.taximeter.active_conditions:
           print(f"Condición especial: {self.taximeter.active_conditions[0].capitalize()}")
       print(f"\nDesglose de estados:")
       for i in range(len(trip_data['movements'])):
           start_time = trip_data['movements'][i][0]
           state = "Movimiento" if trip_data['movements'][i][1] else "Parado"
           if i < len(trip_data['movements']) - 1:
               end_time = trip_data['movements'][i+1][0]
           else:
               end_time = trip_data['movements'][-1][0]
           print(f"- {start_time:.1f}s a {end_time:.1f}s: {state}")
       print(f"\nTarifa total: {trip_data['total_rate']:.2f}€")

    # Gestiona condiciones especiales
    def manage_special_conditions(self):
       print("\n=== CONDICIONES ESPECIALES ===")
       print("Condiciones activas:", self.taximeter.active_conditions if self.taximeter.active_conditions else "Ninguna")
       print("\nSeleccione condición:")
       print("1. Lluvia (+20%)")
       print("2. Eventos (+30%)")
       print("3. Desactivar todas")
       print("4. Volver")

       option = input("\nOpción: ")
       if option == "1":
           self.taximeter.active_conditions = ["rain"]
           print("Activada tarifa por lluvia")
       elif option == "2":
           self.taximeter.active_conditions = ["events"]
           print("Activada tarifa por eventos")
       elif option == "3":
           self.taximeter.active_conditions = []
           print("Condiciones especiales desactivadas")
       elif option == "4":
           return

    # Gestiona un viaje completo
    def handle_trip(self):
       self.taximeter.start_new_trip()
       current_trip = self.taximeter.current_trip
       
       current_rates = current_trip.rate_calculator.get_current_rate()
       condition_info = f" - {self.taximeter.active_conditions[0].capitalize()}" if self.taximeter.active_conditions else ""
       logging.info(f"Nuevo trayecto iniciado - Tarifa: {current_rates['description']}{condition_info}")

       print("\n¡Trayecto iniciado!")
       print(f"Tarifa actual: {current_rates['description']}{condition_info}")
       print("Controles:")
       print("'m' - cambiar movimiento/parado") 
       print("'f' - finalizar trayecto")

       while True:
           current_status = current_trip.get_current_status()
           
           print(f"\rEstado: {current_status['state']} | "
                 f"Tiempo: {current_status['time']:.1f}s | "
                 f"Tarifa: {current_status['rate']:.2f}€", end="", flush=True)
           
           action = input("\nAcción ('m' para cambiar estado, 'f' para finalizar): ").lower()
           
           if action == 'f':
               trip_data = self.taximeter.end_trip()
               logging.info(f"Trayecto finalizado - Duración: {trip_data['duration']:.1f}s - Tarifa: {trip_data['total_rate']:.2f}€")
               self.save_trip_history(trip_data)
               self.show_trip_summary(trip_data)
               
               while True:
                   print("\nOpciones:")
                   print("1. Iniciar nuevo trayecto")
                   print("2. Volver al menú principal")
                   
                   option = input("\nSeleccione una opción: ")
                   if option == "1":
                       return self.handle_trip()
                   elif option == "2":
                       return
                   else:
                       print("Opción no válida. Por favor, seleccione 1 o 2")
               
           elif action == 'm':
               self.taximeter.toggle_motion()
               logging.info(f"Estado cambiado a {current_trip.in_motion}")

    # Guarda historial de viajes
    def save_trip_history(self, trip_data):
       timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
       current_rates = trip_data['rate_info']
       
       with open('history/trips.txt', 'a') as file:
           file.write(f"VIAJE {timestamp}\n")
           file.write(f"Tarifa aplicada: {current_rates['description']}\n")
           if self.taximeter.active_conditions:
               file.write(f"Condición especial: {self.taximeter.active_conditions[0].capitalize()}\n")
           file.write(f"Duración: {trip_data['duration']:.1f}s\n")
           file.write("Estados:\n")
           
           for i in range(len(trip_data['movements'])):
               start_time = trip_data['movements'][i][0]
               state = "Movimiento" if trip_data['movements'][i][1] else "Parado"
               
               if i < len(trip_data['movements']) - 1:
                   end_time = trip_data['movements'][i+1][0]
               else:
                   end_time = trip_data['duration']
                   
               file.write(f"- {start_time:.1f}s a {end_time:.1f}s: {state}\n")
               
           file.write(f"Tarifa total: {trip_data['total_rate']:.2f}€\n")
           file.write("-----------------------------------------\n")

def main():
    logging.info("Programa iniciado")
    taximeter = Taximeter()
    ui = TaxiUI(taximeter)

    # Mostrar menú de autenticación hasta que el usuario inicie sesión
    while not ui.current_user:
        ui.show_auth_menu()
        
    # Una vez autenticado, mostrar el menú principal
    while True:
        ui.show_welcome_message()
        option = input("\nSeleccione una opción (1-4): ")
        
        if option == "1":
            ui.handle_trip()
        elif option == "2":
            ui.show_current_rates()
        elif option == "3":
            ui.manage_special_conditions()
        elif option == "4":
            logging.info("Programa finalizado")
            print("\n¡Gracias por usar el taxímetro!")
            ui.auth.db.disconnect()  
            break
        else:
            logging.warning(f"Opción inválida seleccionada: {option}")
            print("Opción no válida. Por favor, seleccione 1-4")

if __name__ == "__main__":
   main()